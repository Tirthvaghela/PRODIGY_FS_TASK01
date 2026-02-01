from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .email_service import email_service

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        # Validate password strength
        validate_password(attrs['password'])
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        
        # Send professional verification email
        email_service.send_verification_email(user, user.verification_token)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD
    
    def validate(self, attrs):
        # Get user first to check account status
        email = attrs.get(self.username_field)
        try:
            user = User.objects.get(email=email)
            
            # Check if account is locked
            if user.is_account_locked():
                raise serializers.ValidationError("Account temporarily locked due to multiple failed login attempts. Please try again later.")
            
        except User.DoesNotExist:
            pass
        
        try:
            data = super().validate(attrs)
            
            # Reset failed login attempts on successful login
            if hasattr(self, 'user'):
                self.user.unlock_account()
                
                # Add custom claims
                data['user'] = {
                    'id': self.user.id,
                    'email': self.user.email,
                    'username': self.user.username,
                    'role': self.user.role,
                    'is_verified': self.user.is_verified,
                }
            
            return data
            
        except Exception as e:
            # Increment failed login attempts
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.failed_login_attempts += 1
                    if user.failed_login_attempts >= 5:
                        user.lock_account()
                    else:
                        user.save(update_fields=['failed_login_attempts'])
                except User.DoesNotExist:
                    pass
            raise e

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role', 'is_verified', 'date_joined', 'last_login']
        read_only_fields = ['id', 'email', 'date_joined', 'last_login']

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    
    def validate_token(self, value):
        try:
            user = User.objects.get(verification_token=value)
            if user.is_verified:
                raise serializers.ValidationError("Email already verified")
            if not user.is_verification_token_valid():
                raise serializers.ValidationError("Verification token has expired")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token")

class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_verified:
                raise serializers.ValidationError("Email already verified")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")