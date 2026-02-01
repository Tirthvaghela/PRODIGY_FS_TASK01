from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20, 
        choices=[('user', 'User'), ('admin', 'Admin')], 
        default='user'
    )
    otp_secret = models.CharField(max_length=100, blank=True, null=True)
    verification_token = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    verification_token_created = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def is_verification_token_valid(self):
        """Check if verification token is still valid (24 hours)"""
        if not self.verification_token_created:
            return False
        
        from django.conf import settings
        timeout = getattr(settings, 'EMAIL_VERIFICATION_TIMEOUT', 24 * 60 * 60)
        return (timezone.now() - self.verification_token_created).total_seconds() < timeout
    
    def regenerate_verification_token(self):
        """Generate a new verification token"""
        self.verification_token = uuid.uuid4()
        self.verification_token_created = timezone.now()
        self.save(update_fields=['verification_token', 'verification_token_created'])
    
    def is_account_locked(self):
        """Check if account is temporarily locked due to failed login attempts"""
        if self.account_locked_until:
            return timezone.now() < self.account_locked_until
        return False
    
    def lock_account(self, duration_minutes=30):
        """Lock account for specified duration"""
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])
    
    def unlock_account(self):
        """Unlock account and reset failed attempts"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class AuditLog(models.Model):
    """Audit logging for compliance and security monitoring"""
    
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('register', 'User Registration'),
        ('password_change', 'Password Change'),
        ('password_reset', 'Password Reset'),
        ('2fa_enable', '2FA Enabled'),
        ('2fa_disable', '2FA Disabled'),
        ('email_verify', 'Email Verification'),
        ('admin_role_change', 'Admin Role Change'),
        ('admin_user_activate', 'Admin User Activation'),
        ('admin_user_deactivate', 'Admin User Deactivation'),
        ('admin_user_verify', 'Admin User Verification'),
        ('admin_reset_attempts', 'Admin Reset Failed Attempts'),
        ('account_locked', 'Account Locked'),
        ('account_unlocked', 'Account Unlocked'),
        ('failed_login', 'Failed Login Attempt'),
        ('suspicious_activity', 'Suspicious Activity'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    details = models.JSONField(default=dict, blank=True)
    success = models.BooleanField(default=True)
    
    # Admin action tracking
    admin_user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='admin_actions'
    )
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

class UserSession(models.Model):
    """Track active user sessions for security"""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.ip_address} - {self.created_at}"

class TwoFactorBackupCode(models.Model):
    """Backup codes for 2FA recovery"""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'code']
        indexes = [
            models.Index(fields=['user', 'used']),
        ]
    
    def mark_as_used(self):
        """Mark backup code as used"""
        self.used = True
        self.used_at = timezone.now()
        self.save(update_fields=['used', 'used_at'])