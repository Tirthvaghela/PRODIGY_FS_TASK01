"""
Professional Email Service for Prodigy Auth
Handles all email communications with beautiful templates
"""

from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ProdigyEmailService:
    """Professional email service with multiple templates"""
    
    def __init__(self):
        self.from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Prodigy Auth <noreply@prodigyauth.com>')
        self.base_url = 'http://localhost:5173'  # Change for production
    
    def send_verification_email(self, user, verification_token):
        """Send beautiful email verification with professional template"""
        try:
            subject = 'Verify Your Prodigy Auth Account'
            verification_url = f"{self.base_url}/verify-email/{verification_token}/"
            
            # Create professional HTML email
            html_content = self._create_verification_html(user, verification_url)
            text_content = self._create_verification_text(user, verification_url)
            
            # Send email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Verification email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {e}")
            return False
    
    def send_welcome_email(self, user):
        """Send welcome email after successful verification"""
        try:
            subject = 'Welcome to Prodigy Auth!'
            
            html_content = self._create_welcome_html(user)
            text_content = self._create_welcome_text(user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Welcome email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {e}")
            return False
    
    def send_password_reset_email(self, user, reset_token):
        """Send password reset email"""
        try:
            subject = 'Reset Your Prodigy Auth Password'
            reset_url = f"{self.base_url}/reset-password/{reset_token}/"
            
            html_content = self._create_password_reset_html(user, reset_url)
            text_content = self._create_password_reset_text(user, reset_url)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Password reset email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {e}")
            return False
    
    def send_role_change_email(self, user, old_role, new_role, admin_user):
        """Send email notification when user role is changed"""
        try:
            subject = f'Your Prodigy Auth Role Has Been Updated'
            
            html_content = self._create_role_change_html(user, old_role, new_role, admin_user)
            text_content = self._create_role_change_text(user, old_role, new_role, admin_user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Role change email sent to {user.email} (changed from {old_role} to {new_role})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send role change email to {user.email}: {e}")
            return False
    
    def send_account_status_email(self, user, is_active, admin_user):
        """Send email notification when account is activated/deactivated"""
        try:
            action = "activated" if is_active else "deactivated"
            subject = f'Your Prodigy Auth Account Has Been {action.title()}'
            
            html_content = self._create_account_status_html(user, is_active, admin_user)
            text_content = self._create_account_status_text(user, is_active, admin_user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Account status email sent to {user.email} (account {action})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send account status email to {user.email}: {e}")
            return False
    
    def _create_verification_html(self, user, verification_url):
        """Create beautiful HTML verification email"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Account</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f5f5f5;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #4979fe 0%, #f7931e 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px; font-weight: 700;">Prodigy Auth</h1>
                    <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">Secure Authentication Platform</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin: 0 0 20px 0; font-size: 24px;">Welcome {user.username}!</h2>
                    
                    <p style="color: #666; line-height: 1.6; font-size: 16px; margin-bottom: 25px;">
                        Thank you for joining <strong>Prodigy Auth</strong>! To complete your registration and secure your account, 
                        please verify your email address by clicking the button below.
                    </p>
                    
                    <!-- CTA Button -->
                    <div style="text-align: center; margin: 35px 0;">
                        <a href="{verification_url}" 
                           style="background: linear-gradient(135deg, #4979fe, #6366f1); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;
                                  box-shadow: 0 4px 12px rgba(73, 121, 254, 0.3);
                                  transition: all 0.3s ease;">
                            Verify Email Address
                        </a>
                    </div>
                    
                    <!-- Alternative Link -->
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0 0 10px 0;">
                            <strong>Button not working?</strong> Copy and paste this link into your browser:
                        </p>
                        <p style="color: #4979fe; font-size: 14px; word-break: break-all; margin: 0;">
                            {verification_url}
                        </p>
                    </div>
                    
                    <!-- Security Info -->
                    <div style="border-left: 4px solid #f7931e; padding-left: 20px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            <strong>Security Note:</strong> This verification link will expire in 24 hours for your security.
                        </p>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e9ecef;">
                    <p style="color: #666; font-size: 14px; margin: 0 0 10px 0;">
                        This email was sent by <strong>Prodigy Auth System</strong>
                    </p>
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        If you didn't create an account, please ignore this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_verification_text(self, user, verification_url):
        """Create plain text verification email"""
        return f"""
        Welcome {user.username}!
        
        Thank you for joining Prodigy Auth! To complete your registration, please verify your email address.
        
        Click this link to verify: {verification_url}
        
        This link will expire in 24 hours for security.
        
        If you didn't create an account, please ignore this email.
        
        ---
        Prodigy Auth System
        """
    
    def _create_welcome_html(self, user):
        """Create welcome email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to Prodigy Auth!</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Welcome to Prodigy Auth!</h1>
                </div>
                <div style="padding: 40px 30px; text-align: center;">
                    <h2 style="color: #333; margin-bottom: 20px;">Account Verified Successfully!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Congratulations {user.username}! Your account has been verified and you're all set to use Prodigy Auth.
                    </p>
                    <div style="margin: 30px 0;">
                        <a href="{self.base_url}/dashboard" 
                           style="background: #10b981; color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600;">
                            Go to Dashboard
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_welcome_text(self, user):
        """Create welcome email text"""
        return f"""
        Welcome to Prodigy Auth, {user.username}!
        
        Your account has been verified successfully! You can now access all features.
        
        Visit your dashboard: {self.base_url}/dashboard
        
        Thank you for choosing Prodigy Auth!
        """
    
    def _create_password_reset_html(self, user, reset_url):
        """Create password reset email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Reset Your Password</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Password Reset</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Reset Your Password</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Hi {user.username}, we received a request to reset your password. Click the button below to create a new password.
                    </p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_url}" 
                           style="background: #ef4444; color: white; padding: 16px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: 600;">
                            Reset Password
                        </a>
                    </div>
                    <p style="color: #999; font-size: 14px;">
                        This link will expire in 1 hour. If you didn't request this, please ignore this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_password_reset_text(self, user, reset_url):
        """Create password reset email text"""
        return f"""
        Password Reset Request
        
        Hi {user.username},
        
        We received a request to reset your password. Click this link to reset it:
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        
        ---
        Prodigy Auth System
        """
    
    def _create_role_change_html(self, user, old_role, new_role, admin_user):
        """Create role change notification email HTML"""
        role_color = "#dc2626" if new_role == "admin" else "#10b981"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Role Updated</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #4979fe 0%, #f7931e 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Role Updated</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Your account role has been updated by an administrator.
                    </p>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                        <div style="margin-bottom: 15px;">
                            <span style="color: #666; font-size: 14px;">Previous Role:</span><br>
                            <span style="font-size: 18px; font-weight: bold; color: #666;">
                                {old_role.upper()}
                            </span>
                        </div>
                        <div style="font-size: 24px; margin: 10px 0;">↓</div>
                        <div>
                            <span style="color: #666; font-size: 14px;">New Role:</span><br>
                            <span style="font-size: 20px; font-weight: bold; color: {role_color};">
                                {new_role.upper()}
                            </span>
                        </div>
                    </div>
                    
                    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #1976d2; font-size: 14px; margin: 0;">
                            <strong>What this means:</strong><br>
                            {'You now have administrative privileges and can manage other users.' if new_role == 'admin' else 'You are now a regular user with standard access privileges.'}
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/dashboard" 
                           style="background: linear-gradient(135deg, #4979fe, #6366f1); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Go to Dashboard
                        </a>
                    </div>
                    
                    <p style="color: #999; font-size: 14px; text-align: center;">
                        This change was made by: <strong>{admin_user.username}</strong>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_role_change_text(self, user, old_role, new_role, admin_user):
        """Create role change notification email text"""
        return f"""
        Role Updated - Prodigy Auth
        
        Hello {user.username},
        
        Your account role has been updated by an administrator.
        
        Previous Role: {old_role.upper()}
        New Role: {new_role.upper()}
        
        {'You now have administrative privileges.' if new_role == 'admin' else 'You are now a regular user.'}
        
        Visit your dashboard: {self.base_url}/dashboard
        
        This change was made by: {admin_user.username}
        
        ---
        Prodigy Auth System
        """
    
    def _create_account_status_html(self, user, is_active, admin_user):
        """Create account status change email HTML"""
        action = "Activated" if is_active else "Deactivated"
        action_color = "#10b981" if is_active else "#dc2626"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Account {action}</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, {action_color} 0%, {'#059669' if is_active else '#b91c1c'} 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Account {action}</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Your Prodigy Auth account has been <strong>{action.lower()}</strong> by an administrator.
                    </p>
                    
                    <div style="background: {'#f0fdf4' if is_active else '#fef2f2'}; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                        <div style="font-size: 20px; font-weight: bold; color: {action_color};">
                            Account {action}
                        </div>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            <strong>What this means:</strong><br>
                            {f'Your account is now active and you can log in and use all features.' if is_active else 'Your account has been temporarily disabled. You will not be able to log in until it is reactivated.'}
                        </p>
                    </div>
                    
                    {f'''
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/login" 
                           style="background: linear-gradient(135deg, #10b981, #059669); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Login to Your Account
                        </a>
                    </div>
                    ''' if is_active else ''}
                    
                    <p style="color: #999; font-size: 14px; text-align: center;">
                        This change was made by: <strong>{admin_user.username}</strong>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_account_status_text(self, user, is_active, admin_user):
        """Create account status change email text"""
        action = "activated" if is_active else "deactivated"
        
        return f"""
        Account {action.title()} - Prodigy Auth
        
        Hello {user.username},
        
        Your Prodigy Auth account has been {action} by an administrator.
        
        {f'Your account is now active and you can log in.' if is_active else 'Your account has been disabled and you cannot log in until reactivated.'}
        
        {f'Login here: {self.base_url}/login' if is_active else ''}
        
        This change was made by: {admin_user.username}
        
        ---
        Prodigy Auth System
        """
    
    def send_password_change_notification(self, user):
        """Send email notification when password is changed"""
        try:
            subject = 'Password Changed - Prodigy Auth'
            
            html_content = self._create_password_change_html(user)
            text_content = self._create_password_change_text(user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Password change notification sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password change notification to {user.email}: {e}")
            return False
    
    def send_2fa_enabled_notification(self, user):
        """Send email notification when 2FA is enabled"""
        try:
            subject = '2FA Enabled - Prodigy Auth'
            
            html_content = self._create_2fa_enabled_html(user)
            text_content = self._create_2fa_enabled_text(user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"2FA enabled notification sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send 2FA enabled notification to {user.email}: {e}")
            return False
    
    def send_2fa_disabled_notification(self, user):
        """Send email notification when 2FA is disabled"""
        try:
            subject = '2FA Disabled - Prodigy Auth'
            
            html_content = self._create_2fa_disabled_html(user)
            text_content = self._create_2fa_disabled_text(user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"2FA disabled notification sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send 2FA disabled notification to {user.email}: {e}")
            return False
    
    def _create_password_change_html(self, user):
        """Create password change notification email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Password Changed</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Password Changed</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Your Prodigy Auth account password has been successfully changed.
                    </p>
                    
                    <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                        <div style="font-size: 20px; font-weight: bold; color: #10b981; margin-bottom: 10px;">
                            Password Updated
                        </div>
                        <div style="color: #666; font-size: 14px;">
                            Changed on: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}
                        </div>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            <strong>Security Note:</strong><br>
                            If you did not make this change, please contact support immediately and consider enabling 2FA for additional security.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/dashboard" 
                           style="background: linear-gradient(135deg, #10b981, #059669); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Go to Dashboard
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_password_change_text(self, user):
        """Create password change notification email text"""
        return f"""
        Password Changed - Prodigy Auth
        
        Hello {user.username},
        
        Your Prodigy Auth account password has been successfully changed.
        
        Changed on: {timezone.now().strftime('%B %d, %Y at %I:%M %p')}
        
        If you did not make this change, please contact support immediately.
        
        Visit your dashboard: {self.base_url}/dashboard
        
        ---
        Prodigy Auth System
        """
    
    def _create_2fa_enabled_html(self, user):
        """Create 2FA enabled notification email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>2FA Enabled</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #4979fe 0%, #f7931e 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">2FA Enabled</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Two-Factor Authentication (2FA) has been successfully enabled for your Prodigy Auth account.
                    </p>
                    
                    <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                        <div style="font-size: 20px; font-weight: bold; color: #4979fe; margin-bottom: 10px;">
                            Enhanced Security Active
                        </div>
                        <div style="color: #666; font-size: 14px;">
                            Your account is now protected with 2FA
                        </div>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            <strong>What this means:</strong><br>
                            You'll now need to enter a code from your authenticator app when logging in, providing an extra layer of security for your account.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/dashboard" 
                           style="background: linear-gradient(135deg, #4979fe, #6366f1); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Go to Dashboard
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_2fa_enabled_text(self, user):
        """Create 2FA enabled notification email text"""
        return f"""
        2FA Enabled - Prodigy Auth
        
        Hello {user.username},
        
        Two-Factor Authentication (2FA) has been successfully enabled for your account.
        
        Your account now has enhanced security protection. You'll need to enter a code from your authenticator app when logging in.
        
        Visit your dashboard: {self.base_url}/dashboard
        
        ---
        Prodigy Auth System
        """
    
    def _create_2fa_disabled_html(self, user):
        """Create 2FA disabled notification email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>2FA Disabled</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">2FA Disabled</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Two-Factor Authentication (2FA) has been disabled for your Prodigy Auth account.
                    </p>
                    
                    <div style="background: #fef2f2; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                        <div style="font-size: 20px; font-weight: bold; color: #ef4444; margin-bottom: 10px;">
                            2FA Disabled
                        </div>
                        <div style="color: #666; font-size: 14px;">
                            Your account security has been reduced
                        </div>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            <strong>Security Recommendation:</strong><br>
                            Consider re-enabling 2FA for enhanced account security. If you did not make this change, please contact support immediately.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/dashboard" 
                           style="background: linear-gradient(135deg, #ef4444, #dc2626); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Go to Dashboard
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_2fa_disabled_text(self, user):
        """Create 2FA disabled notification email text"""
        return f"""
        2FA Disabled - Prodigy Auth
        
        Hello {user.username},
        
        Two-Factor Authentication (2FA) has been disabled for your account.
        
        If you did not make this change, please contact support immediately.
        
        Consider re-enabling 2FA for enhanced security.
        
        Visit your dashboard: {self.base_url}/dashboard
        
        ---
        Prodigy Auth System
        """
    
    def send_password_reset_confirmation(self, user):
        """Send email confirmation after password reset"""
        try:
            subject = 'Password Reset Successful - Prodigy Auth'
            
            html_content = self._create_password_reset_confirmation_html(user)
            text_content = self._create_password_reset_confirmation_text(user)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Password reset confirmation sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset confirmation to {user.email}: {e}")
            return False
    
    def _create_password_reset_confirmation_html(self, user):
        """Create password reset confirmation email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Password Reset Successful</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Password Reset Successful</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        Your Prodigy Auth account password has been successfully reset.
                    </p>
                    
                    <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center;">
                        <div style="font-size: 20px; font-weight: bold; color: #10b981; margin-bottom: 10px;">
                            Password Reset Complete
                        </div>
                        <div style="color: #666; font-size: 14px;">
                            You can now log in with your new password
                        </div>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #666; font-size: 14px; margin: 0;">
                            <strong>Security Note:</strong><br>
                            If you did not request this password reset, please contact support immediately and consider enabling 2FA for additional security.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/login" 
                           style="background: linear-gradient(135deg, #10b981, #059669); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Login to Your Account
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_password_reset_confirmation_text(self, user):
        """Create password reset confirmation email text"""
        return f"""
        Password Reset Successful - Prodigy Auth
        
        Hello {user.username},
        
        Your Prodigy Auth account password has been successfully reset.
        
        You can now log in with your new password.
        
        If you did not request this password reset, please contact support immediately.
        
        Login here: {self.base_url}/login
        
        ---
        Prodigy Auth System
        """

    def send_temporary_password_email(self, user, temp_password):
        """Send temporary password email"""
        try:
            subject = 'Temporary Password - Prodigy Auth'
            
            html_content = self._create_temporary_password_html(user, temp_password)
            text_content = self._create_temporary_password_text(user, temp_password)
            
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=self.from_email,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Temporary password email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send temporary password email to {user.email}: {e}")
            return False
    
    def _create_temporary_password_html(self, user, temp_password):
        """Create temporary password email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Temporary Password</title>
        </head>
        <body style="font-family: 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 40px 20px; text-align: center;">
                    <h1 style="color: white; margin: 0; font-size: 28px;">Temporary Password</h1>
                </div>
                <div style="padding: 40px 30px;">
                    <h2 style="color: #333; margin-bottom: 20px;">Hello {user.username}!</h2>
                    <p style="color: #666; line-height: 1.6; font-size: 16px;">
                        A temporary password has been generated for your Prodigy Auth account.
                    </p>
                    
                    <div style="background: #fef3c7; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center; border: 2px solid #f59e0b;">
                        <div style="font-size: 16px; font-weight: bold; color: #92400e; margin-bottom: 10px;">
                            Your Temporary Password:
                        </div>
                        <div style="font-size: 24px; font-weight: bold; color: #92400e; font-family: 'Courier New', monospace; letter-spacing: 2px; background: white; padding: 15px; border-radius: 6px; margin: 10px 0;">
                            {temp_password}
                        </div>
                        <div style="color: #92400e; font-size: 14px; margin-top: 10px;">
                            Please copy this password carefully
                        </div>
                    </div>
                    
                    <div style="background: #fef2f2; padding: 20px; border-radius: 8px; margin: 25px 0; border-left: 4px solid #ef4444;">
                        <p style="color: #dc2626; font-size: 14px; margin: 0; font-weight: 600;">
                            <strong>IMPORTANT SECURITY NOTICE:</strong><br>
                            • This is a temporary password - change it immediately after logging in<br>
                            • Do not share this password with anyone<br>
                            • This email should be deleted after use<br>
                            • Enable 2FA for enhanced security
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{self.base_url}/login" 
                           style="background: linear-gradient(135deg, #f59e0b, #d97706); 
                                  color: white; 
                                  padding: 16px 32px; 
                                  text-decoration: none; 
                                  border-radius: 8px; 
                                  display: inline-block; 
                                  font-weight: 600; 
                                  font-size: 16px;">
                            Login Now
                        </a>
                    </div>
                    
                    <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 25px 0;">
                        <p style="color: #1e40af; font-size: 14px; margin: 0;">
                            <strong>Next Steps:</strong><br>
                            1. Login with this temporary password<br>
                            2. Go to Settings → Change Password<br>
                            3. Set a strong, unique password<br>
                            4. Consider enabling 2FA for extra security
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_temporary_password_text(self, user, temp_password):
        """Create temporary password email text"""
        return f"""
        Temporary Password - Prodigy Auth
        
        Hello {user.username},
        
        A temporary password has been generated for your account.
        
        TEMPORARY PASSWORD: {temp_password}
        
        IMPORTANT SECURITY NOTICE:
        - This is a temporary password - change it immediately after logging in
        - Do not share this password with anyone
        - Delete this email after use
        - Enable 2FA for enhanced security
        
        Next Steps:
        1. Login with this temporary password
        2. Go to Settings → Change Password
        3. Set a strong, unique password
        4. Consider enabling 2FA
        
        Login here: {self.base_url}/login
        
        ---
        Prodigy Auth System
        """

# Global instance
email_service = ProdigyEmailService()