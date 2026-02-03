from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from .serializers import (
    RegisterSerializer, 
    CustomTokenObtainPairSerializer, 
    UserProfileSerializer,
    EmailVerificationSerializer,
    ResendVerificationSerializer
)
from .permissions import IsAdminUser
from .email_service import email_service
from .audit import log_audit_event, log_login_attempt, log_admin_action, log_security_event
from .models import UserSession, TwoFactorBackupCode
import pyotp
import qrcode
import io
import base64
import uuid
import logging
import secrets
import string

logger = logging.getLogger(__name__)

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for immediate login after verification
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Registration successful! Please check your email to verify your account.',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'is_verified': user.is_verified,
            },
            'verification_required': True,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            } if user.is_verified else None
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Clean login view with audit logging"""
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    
    # Get IP and user agent for logging
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', '127.0.0.1')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    if serializer.is_valid():
        # Get user and create tokens
        user = serializer.user
        refresh = RefreshToken.for_user(user)
        
        # Update last login info
        user.last_login = timezone.now()
        user.last_login_ip = ip_address
        user.save(update_fields=['last_login', 'last_login_ip'])
        
        # Create user session
        session_key = str(uuid.uuid4())
        UserSession.objects.create(
            user=user,
            session_key=session_key,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Log successful login
        log_login_attempt(
            user=user,
            success=True,
            ip_address=ip_address,
            user_agent=user_agent,
            details={'session_key': session_key}
        )
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'session_key': session_key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'is_verified': user.is_verified,
                'has_2fa': bool(user.otp_secret),
            }
        })
    
    # Log failed login attempt
    email = request.data.get('email')
    user = None
    if email:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
    
    log_login_attempt(
        user=user,
        success=False,
        ip_address=ip_address,
        user_agent=user_agent,
        details={'email': email, 'errors': serializer.errors}
    )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Verify user email with token"""
    try:
        serializer = EmailVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        token = serializer.validated_data['token']
        user = User.objects.get(verification_token=token)
        
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        
        # Send welcome email
        email_service.send_welcome_email(user)
        
        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Email verified successfully! Welcome to Prodigy Auth!',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'is_verified': user.is_verified,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
    except Exception as e:
        return Response({
            'error': f'Verification failed: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification(request):
    """Resend verification email"""
    serializer = ResendVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data['email']
    user = User.objects.get(email=email)
    
    # Regenerate token and send email
    user.regenerate_verification_token()
    
    # Use the professional email service
    email_service.send_verification_email(user, user.verification_token)
    
    return Response({
        'message': 'Verification email sent successfully!'
    })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user with session cleanup and audit logging"""
    try:
        # Get session key and deactivate session
        session_key = request.data.get('session_key')
        if session_key:
            UserSession.objects.filter(
                user=request.user,
                session_key=session_key
            ).update(is_active=False)
        
        # Get the refresh token from request and blacklist it
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                logger.info(f"Blacklisted refresh token for user {request.user.email}")
            except Exception as e:
                logger.error(f"Failed to blacklist refresh token: {e}")
        
        # Also blacklist the current access token from Authorization header
        try:
            # Get the access token from the Authorization header
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token_str = auth_header.split(' ')[1]
                
                # Import the blacklist model directly
                from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
                from rest_framework_simplejwt.tokens import AccessToken
                
                try:
                    # Create an AccessToken object and blacklist it
                    access_token = AccessToken(access_token_str)
                    
                    # Get or create the outstanding token
                    outstanding_token, created = OutstandingToken.objects.get_or_create(
                        token=access_token_str,
                        defaults={
                            'user': request.user,
                            'jti': access_token['jti'],
                            'expires_at': access_token['exp']
                        }
                    )
                    
                    # Blacklist the token
                    BlacklistedToken.objects.get_or_create(token=outstanding_token)
                    logger.info(f"Blacklisted access token for user {request.user.email}")
                    
                except Exception as e:
                    logger.warning(f"Could not blacklist access token: {e}")
        except Exception as e:
            logger.error(f"Error blacklisting access token: {e}")
        
        # Log logout
        log_audit_event(
            action='logout',
            user=request.user,
            request=request,
            details={'session_key': session_key}
        )
        
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        logger.error(f"Logout error: {e}")
        # Still log the logout attempt
        log_audit_event(
            action='logout',
            user=request.user,
            request=request,
            success=False,
            details={'error': str(e)}
        )
        return Response({'message': 'Logged out (token cleanup failed)'})  # Still log out user

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    """Admin dashboard with enhanced statistics"""
    users_count = User.objects.count()
    verified_users = User.objects.filter(is_verified=True).count()
    unverified_users = users_count - verified_users
    admin_users = User.objects.filter(role='admin').count()
    locked_accounts = User.objects.filter(account_locked_until__gt=timezone.now()).count()
    inactive_users = User.objects.filter(is_active=False).count()  # Add inactive users count
    recent_registrations = User.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()
    
    # Get recent users for admin panel
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    return Response({
        'stats': {
            'total_users': users_count,
            'verified_users': verified_users,
            'unverified_users': unverified_users,
            'admin_users': admin_users,
            'locked_accounts': locked_accounts,
            'inactive_users': inactive_users,  # Add to response
            'recent_registrations': recent_registrations,
        },
        'recent_users': [
            {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role,
                'is_verified': user.is_verified,
                'date_joined': user.date_joined,
            } for user in recent_users
        ],
        'message': f'Welcome Admin {request.user.username}!',
        'system_status': {
            'jwt_enabled': True,
            'email_verification': True,
            'account_locking': True,
            'cors_enabled': True,
            'smtp_configured': hasattr(settings, 'EMAIL_HOST_USER') and bool(settings.EMAIL_HOST_USER),
            'email_backend': settings.EMAIL_BACKEND,
        }
    })

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users_list(request):
    """Get all users for admin management"""
    users = User.objects.all().order_by('-date_joined')
    
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'is_verified': user.is_verified,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'failed_login_attempts': user.failed_login_attempts,
            'is_locked': user.is_account_locked(),
            'account_locked_until': user.account_locked_until,
        })
    
    return Response({
        'users': users_data,
        'total_count': len(users_data)
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_send_verification(request):
    """Send verification email to specific user"""
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({
            'error': 'User ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        
        if user.is_verified:
            return Response({
                'error': 'User is already verified'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new token if needed
        if not user.verification_token:
            user.regenerate_verification_token()
        
        success = email_service.send_verification_email(user, user.verification_token)
        
        return Response({
            'message': f'Verification email sent to {user.email}',
            'success': success
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_toggle_user_status(request):
    """Toggle user active status"""
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({
            'error': 'User ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent admin from deactivating themselves
        if user.id == request.user.id:
            return Response({
                'error': 'You cannot deactivate yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        old_status = user.is_active
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        
        action = "activated" if user.is_active else "deactivated"
        
        # Send email notification to user
        try:
            email_service.send_account_status_email(user, user.is_active, request.user)
        except Exception as e:
            # Log email error but don't fail the status change
            print(f"Warning: Failed to send account status email to {user.email}: {e}")
        
        return Response({
            'message': f'User {user.email} has been {action}',
            'user': {
                'id': user.id,
                'email': user.email,
                'is_active': user.is_active
            }
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Status toggle failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_reset_failed_attempts(request):
    """Reset failed login attempts for a user"""
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({
            'error': 'User ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        user.failed_login_attempts = 0
        user.account_locked_until = None
        user.save()
        
        return Response({
            'message': f'Failed login attempts reset for {user.email}'
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_change_user_role(request):
    """Change user role between 'user' and 'admin'"""
    user_id = request.data.get('user_id')
    new_role = request.data.get('role')
    
    if not user_id or not new_role:
        return Response({
            'error': 'User ID and role are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if new_role not in ['user', 'admin']:
        return Response({
            'error': 'Role must be either "user" or "admin"'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent admin from demoting themselves
        if user.id == request.user.id and new_role == 'user':
            return Response({
                'error': 'You cannot demote yourself from admin'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        old_role = user.role
        user.role = new_role
        user.save(update_fields=['role'])
        
        # Send email notification to user
        try:
            email_service.send_role_change_email(user, old_role, new_role, request.user)
        except Exception as e:
            # Log email error but don't fail the role change
            print(f"Warning: Failed to send role change email to {user.email}: {e}")
        
        return Response({
            'message': f'User {user.email} role changed from {old_role} to {new_role}',
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Role change failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_verify_user(request):
    """Manually verify a user's email"""
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response({
            'error': 'User ID is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(id=user_id)
        
        if user.is_verified:
            return Response({
                'error': 'User is already verified'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        
        # Send welcome email
        try:
            email_service.send_welcome_email(user)
        except Exception as e:
            # Log email error but don't fail the verification
            print(f"Warning: Failed to send welcome email to {user.email}: {e}")
        
        return Response({
            'message': f'User {user.email} has been manually verified',
            'user': {
                'id': user.id,
                'email': user.email,
                'is_verified': user.is_verified
            }
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Verification failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Get current user statistics"""
    user = request.user
    return Response({
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'role': user.role,
            'is_verified': user.is_verified,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'last_login_ip': user.last_login_ip,
            'failed_login_attempts': user.failed_login_attempts,
            'is_locked': user.is_account_locked(),
        }
    })

# Password Change and 2FA Views

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not all([current_password, new_password, confirm_password]):
        return Response({
            'error': 'All password fields are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if new_password != confirm_password:
        return Response({
            'error': 'New passwords do not match'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 8:
        return Response({
            'error': 'Password must be at least 8 characters long'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # Verify current password
    if not user.check_password(current_password):
        return Response({
            'error': 'Current password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Set new password
    user.set_password(new_password)
    user.save()
    
    # Send email notification
    try:
        email_service.send_password_change_notification(user)
    except Exception as e:
        print(f"Warning: Failed to send password change notification to {user.email}: {e}")
    
    return Response({
        'message': 'Password changed successfully'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_2fa(request):
    """Setup 2FA for user"""
    user = request.user
    
    if user.otp_secret:
        return Response({
            'error': '2FA is already enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate secret key
    secret = pyotp.random_base32()
    
    # Create TOTP object
    totp = pyotp.TOTP(secret)
    
    # Generate QR code
    provisioning_uri = totp.provisioning_uri(
        name=user.email,
        issuer_name="Prodigy Auth"
    )
    
    # Create QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # Temporarily store secret using cache (will be saved after verification)
    cache_key = f"temp_2fa_secret_{user.id}"
    cache.set(cache_key, secret, timeout=300)  # 5 minutes timeout
    
    return Response({
        'secret': secret,
        'qr_code': f"data:image/png;base64,{qr_code_base64}",
        'manual_entry_key': secret,
        'message': 'Scan the QR code with your authenticator app, then verify with a code to enable 2FA'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa_setup(request):
    """Verify and enable 2FA with backup codes"""
    user = request.user
    verification_code = request.data.get('code')
    
    if not verification_code:
        return Response({
            'error': 'Verification code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get temporary secret from cache
    cache_key = f"temp_2fa_secret_{user.id}"
    temp_secret = cache.get(cache_key)
    if not temp_secret:
        return Response({
            'error': 'No 2FA setup in progress. Please start setup again.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify the code
    totp = pyotp.TOTP(temp_secret)
    if not totp.verify(verification_code, valid_window=1):
        return Response({
            'error': 'Invalid verification code'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Save secret to user
    user.otp_secret = temp_secret
    user.save(update_fields=['otp_secret'])
    
    # Clear temporary secret from cache
    cache.delete(cache_key)
    
    # Generate backup codes
    backup_codes = generate_backup_codes(user)
    
    # Log 2FA enabled
    log_audit_event(
        action='2fa_enable',
        user=user,
        request=request,
        details={'backup_codes_generated': len(backup_codes)}
    )
    
    # Send email notification
    try:
        email_service.send_2fa_enabled_notification(user)
    except Exception as e:
        logger.error(f"Failed to send 2FA notification to {user.email}: {e}")
    
    return Response({
        'message': '2FA has been successfully enabled for your account',
        'backup_codes': backup_codes
    })

def generate_backup_codes(user, count=10):
    """Generate backup codes for 2FA recovery"""
    # Delete existing backup codes
    TwoFactorBackupCode.objects.filter(user=user).delete()
    
    backup_codes = []
    for _ in range(count):
        # Generate 8-character alphanumeric code
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
        TwoFactorBackupCode.objects.create(user=user, code=code)
        backup_codes.append(code)
    
    return backup_codes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_backup_codes(request):
    """Regenerate 2FA backup codes"""
    user = request.user
    
    if not user.otp_secret:
        return Response({
            'error': '2FA is not enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate new backup codes
    backup_codes = generate_backup_codes(user)
    
    # Log backup codes regeneration
    log_audit_event(
        action='2fa_backup_regenerate',
        user=user,
        request=request,
        details={'backup_codes_generated': len(backup_codes)}
    )
    
    return Response({
        'message': 'Backup codes have been regenerated',
        'backup_codes': backup_codes
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_backup_code(request):
    """Verify 2FA using backup code"""
    user = request.user
    backup_code = request.data.get('code', '').upper().strip()
    
    if not backup_code:
        return Response({
            'error': 'Backup code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.otp_secret:
        return Response({
            'error': '2FA is not enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Find and verify backup code
    try:
        backup_code_obj = TwoFactorBackupCode.objects.get(
            user=user,
            code=backup_code,
            used=False
        )
        
        # Mark as used
        backup_code_obj.mark_as_used()
        
        # Log backup code usage
        log_audit_event(
            action='2fa_backup_used',
            user=user,
            request=request,
            details={'backup_code': backup_code}
        )
        
        # Check remaining codes
        remaining_codes = TwoFactorBackupCode.objects.filter(
            user=user,
            used=False
        ).count()
        
        return Response({
            'message': '2FA verification successful using backup code',
            'verified': True,
            'remaining_backup_codes': remaining_codes
        })
        
    except TwoFactorBackupCode.DoesNotExist:
        # Log failed backup code attempt
        log_security_event(
            action='2fa_backup_failed',
            user=user,
            request=request,
            details={'attempted_code': backup_code}
        )
        
        return Response({
            'error': 'Invalid or already used backup code'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def disable_2fa(request):
    """Disable 2FA for user"""
    user = request.user
    current_password = request.data.get('current_password')
    
    if not user.otp_secret:
        return Response({
            'error': '2FA is not enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not current_password:
        return Response({
            'error': 'Current password is required to disable 2FA'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify current password
    if not user.check_password(current_password):
        return Response({
            'error': 'Current password is incorrect'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Disable 2FA
    user.otp_secret = None
    user.save(update_fields=['otp_secret'])
    
    # Send email notification
    try:
        email_service.send_2fa_disabled_notification(user)
    except Exception as e:
        print(f"Warning: Failed to send 2FA notification to {user.email}: {e}")
    
    return Response({
        'message': '2FA has been disabled for your account'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_2fa_status(request):
    """Get 2FA status for user"""
    user = request.user
    return Response({
        'is_2fa_enabled': bool(user.otp_secret),
        'has_2fa_secret': bool(user.otp_secret)
    })
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa_login(request):
    """Verify 2FA code during login process"""
    user = request.user
    verification_code = request.data.get('code')
    backup_code = request.data.get('backup_code')
    
    if not verification_code and not backup_code:
        return Response({
            'error': 'Verification code or backup code is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.otp_secret:
        return Response({
            'error': '2FA is not enabled for this account'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Try backup code first if provided
    if backup_code:
        backup_code = backup_code.upper().strip()
        try:
            backup_code_obj = TwoFactorBackupCode.objects.get(
                user=user,
                code=backup_code,
                used=False
            )
            
            # Mark as used
            backup_code_obj.mark_as_used()
            
            # Log backup code usage
            log_audit_event(
                action='2fa_backup_used',
                user=user,
                request=request,
                details={'backup_code': backup_code}
            )
            
            return Response({
                'message': '2FA verification successful using backup code',
                'verified': True
            })
            
        except TwoFactorBackupCode.DoesNotExist:
            return Response({
                'error': 'Invalid or already used backup code'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify TOTP code
    if verification_code:
        totp = pyotp.TOTP(user.otp_secret)
        if not totp.verify(verification_code, valid_window=1):
            # Log failed 2FA attempt
            log_security_event(
                action='2fa_failed',
                user=user,
                request=request,
                details={'attempted_code': verification_code}
            )
            
            return Response({
                'error': 'Invalid verification code'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log successful 2FA
        log_audit_event(
            action='2fa_verified',
            user=user,
            request=request
        )
        
        return Response({
            'message': '2FA verification successful',
            'verified': True
        })
    
    return Response({
        'error': 'Invalid verification method'
    }, status=status.HTTP_400_BAD_REQUEST)
# Forgot Password Views

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Send password reset email with minimal restrictions"""
    email = request.data.get('email')
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', '127.0.0.1')
    
    if not email:
        return Response({
            'error': 'Email address is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email exists in database
    try:
        user = User.objects.get(email=email)
        
        # Check if user is active
        if not user.is_active:
            return Response({
                'error': 'This account is deactivated. Please contact support.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate reset token
        reset_token = str(uuid.uuid4())
        
        # Store reset token in cache with 1 hour expiration
        cache_key = f"password_reset_{reset_token}"
        cache.set(cache_key, user.id, timeout=3600)  # 1 hour
        
        # Send password reset email
        try:
            email_service.send_password_reset_email(user, reset_token)
            
            # Log password reset request
            log_audit_event(
                action='password_reset',
                user=user,
                request=request,
                details={
                    'email': email, 
                    'reset_token_generated': True,
                    'ip_address': ip_address
                }
            )
            
            return Response({
                'message': 'Password reset email sent successfully. Please check your inbox.',
                'email_sent': True
            })
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return Response({
                'error': 'Failed to send password reset email. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except User.DoesNotExist:
        # Log potential email enumeration attempt
        log_security_event(
            action='email_enumeration_attempt',
            user=None,
            request=request,
            details={
                'attempted_email': email,
                'ip_address': ip_address
            }
        )
        
        # Email does not exist in database
        return Response({
            'error': 'No account found with this email address. Please check your email or register for a new account.',
            'email_exists': False
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    """Reset password using token"""
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not all([token, new_password, confirm_password]):
        return Response({
            'error': 'Token, new password, and confirmation are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if new_password != confirm_password:
        return Response({
            'error': 'Passwords do not match'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 8:
        return Response({
            'error': 'Password must be at least 8 characters long'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get user ID from cache
    cache_key = f"password_reset_{token}"
    user_id = cache.get(cache_key)
    
    if not user_id:
        return Response({
            'error': 'Invalid or expired reset token'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Immediately delete the token to prevent reuse (SECURITY FIX)
    cache.delete(cache_key)
    
    try:
        user = User.objects.get(id=user_id, is_active=True)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Send confirmation email
        try:
            email_service.send_password_reset_confirmation(user)
        except Exception as e:
            logger.error(f"Failed to send password reset confirmation to {user.email}: {e}")
        
        return Response({
            'message': 'Password reset successfully. You can now log in with your new password.'
        })
        
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid reset token'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_sessions(request):
    """Get user's active sessions"""
    sessions = UserSession.objects.filter(
        user=request.user,
        is_active=True
    ).order_by('-last_activity')
    
    sessions_data = []
    for session in sessions:
        sessions_data.append({
            'session_key': session.session_key,
            'ip_address': session.ip_address,
            'user_agent': session.user_agent,
            'created_at': session.created_at,
            'last_activity': session.last_activity,
            'is_current': session.session_key == request.data.get('current_session_key')
        })
    
    return Response({
        'sessions': sessions_data,
        'total_count': len(sessions_data)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def terminate_session(request):
    """Terminate a specific session"""
    session_key = request.data.get('session_key')
    
    if not session_key:
        return Response({
            'error': 'Session key is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        session = UserSession.objects.get(
            user=request.user,
            session_key=session_key,
            is_active=True
        )
        
        session.is_active = False
        session.save()
        
        # Log session termination
        log_audit_event(
            action='session_terminated',
            user=request.user,
            request=request,
            details={'terminated_session': session_key}
        )
        
        return Response({
            'message': 'Session terminated successfully'
        })
        
    except UserSession.DoesNotExist:
        return Response({
            'error': 'Session not found or already terminated'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def terminate_all_sessions(request):
    """Terminate all user sessions except current"""
    current_session_key = request.data.get('current_session_key')
    
    # Terminate all sessions except current
    if current_session_key:
        terminated_count = UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).exclude(session_key=current_session_key).update(is_active=False)
    else:
        terminated_count = UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).update(is_active=False)
    
    # Log session termination
    log_audit_event(
        action='all_sessions_terminated',
        user=request.user,
        request=request,
        details={'terminated_count': terminated_count}
    )
    
    return Response({
        'message': f'Terminated {terminated_count} sessions successfully'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_password_reset_activity(request):
    """Get recent password reset activity for the user"""
    user = request.user
    
    # Check if there's a recent reset request
    recent_reset_key = f"recent_reset_{user.id}"
    has_recent_reset = cache.get(recent_reset_key, False)
    
    # Get rate limiting info
    email_rate_key = f"forgot_password_email_{user.email.lower()}"
    email_attempts = cache.get(email_rate_key, 0)
    
    return Response({
        'has_recent_reset': bool(has_recent_reset),
        'email_attempts_today': email_attempts,
        'max_attempts_per_hour': 2,
        'cooldown_minutes': 15,
        'security_info': {
            'rate_limit_per_email': '2 requests per hour',
            'cooldown_period': '15 minutes between requests',
            'ip_protection': 'Maximum 3 different emails per IP per hour'
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_suspicious_reset_activity(request):
    """Allow users to report if they received unexpected password reset emails"""
    user = request.user
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or request.META.get('REMOTE_ADDR', '127.0.0.1')
    
    details = request.data.get('details', '')
    
    # Log the report
    log_security_event(
        action='user_reported_suspicious_reset',
        user=user,
        request=request,
        details={
            'user_report': details,
            'ip_address': ip_address,
            'timestamp': timezone.now().isoformat()
        }
    )
    
    # Temporarily increase security for this user
    security_key = f"enhanced_security_{user.id}"
    cache.set(security_key, True, timeout=86400)  # 24 hours
    
    return Response({
        'message': 'Thank you for reporting. We have enhanced security monitoring for your account.',
        'enhanced_security_duration': '24 hours'
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_alternative(request):
    """Alternative password reset method using security questions or username"""
    email = request.data.get('email')
    username = request.data.get('username')
    security_answer = request.data.get('security_answer', '')
    
    if not email and not username:
        return Response({
            'error': 'Email address or username is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find user by email or username
        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(username=username)
        
        # Check if user is active
        if not user.is_active:
            return Response({
                'error': 'This account is deactivated. Please contact support.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # For now, we'll use a simple security question approach
        # In production, you might want more sophisticated security questions
        expected_answer = user.username.lower()  # Simple: username as security answer
        
        if security_answer.lower() == expected_answer:
            # Generate temporary password
            temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
            
            # Set temporary password
            user.set_password(temp_password)
            user.save()
            
            # Send temporary password via email
            try:
                email_service.send_temporary_password_email(user, temp_password)
                
                # Log alternative password reset
                log_audit_event(
                    action='alternative_password_reset',
                    user=user,
                    request=request,
                    details={
                        'method': 'security_question',
                        'temp_password_sent': True
                    }
                )
                
                return Response({
                    'message': 'Temporary password sent to your email. Please login and change your password immediately.',
                    'temp_password_sent': True,
                    'security_notice': 'Please change your password after logging in for security.'
                })
            except Exception as e:
                logger.error(f"Failed to send temporary password to {user.email}: {e}")
                return Response({
                    'error': 'Failed to send temporary password. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'error': 'Security answer is incorrect. Please try again.',
                'hint': 'Hint: Your username'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except User.DoesNotExist:
        return Response({
            'error': 'No account found with this email or username.',
            'suggestion': 'Please check your credentials or register for a new account.'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_username_only(request):
    """Reset password using only username - generates new temporary password"""
    username = request.data.get('username')
    
    if not username:
        return Response({
            'error': 'Username is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
        
        # Check if user is active
        if not user.is_active:
            return Response({
                'error': 'This account is deactivated. Please contact support.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new temporary password
        temp_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
        
        # Set temporary password
        user.set_password(temp_password)
        user.save()
        
        # Send temporary password via email
        try:
            email_service.send_temporary_password_email(user, temp_password)
            
            # Log username-based password reset
            log_audit_event(
                action='username_password_reset',
                user=user,
                request=request,
                details={
                    'method': 'username_only',
                    'temp_password_sent': True
                }
            )
            
            return Response({
                'message': f'New temporary password sent to {user.email}. Please login and change your password immediately.',
                'email_hint': f'{user.email[:3]}***@{user.email.split("@")[1]}',
                'temp_password_sent': True,
                'security_notice': 'Please change your password after logging in for security.'
            })
        except Exception as e:
            logger.error(f"Failed to send temporary password to {user.email}: {e}")
            return Response({
                'error': 'Failed to send temporary password. Please try again.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except User.DoesNotExist:
        return Response({
            'error': 'No account found with this username.',
            'suggestion': 'Please check your username or register for a new account.'
        }, status=status.HTTP_404_NOT_FOUND)
    """Validate if reset token is valid"""
    cache_key = f"password_reset_{token}"
    user_id = cache.get(cache_key)
    
    if user_id:
        try:
            user = User.objects.get(id=user_id, is_active=True)
            return Response({
                'valid': True,
                'email': user.email
            })
        except User.DoesNotExist:
            pass
    
    return Response({
        'valid': False,
        'error': 'Invalid or expired reset token'
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def validate_reset_token(request, token):
    """Validate if reset token is valid"""
    cache_key = f"password_reset_{token}"
    user_id = cache.get(cache_key)
    
    if user_id:
        try:
            user = User.objects.get(id=user_id, is_active=True)
            return Response({
                'valid': True,
                'email': user.email
            })
        except User.DoesNotExist:
            pass
    
    return Response({
        'valid': False,
        'error': 'Invalid or expired reset token'
    }, status=status.HTTP_400_BAD_REQUEST)