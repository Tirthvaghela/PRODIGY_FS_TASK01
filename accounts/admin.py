from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import CustomUser
from .email_service import email_service
import uuid

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'role_badge', 'verification_status', 
        'is_active', 'date_joined', 'admin_actions'
    )
    list_filter = ('role', 'is_verified', 'is_active', 'date_joined', 'account_locked_until')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    list_per_page = 25
    
    fieldsets = UserAdmin.fieldsets + (
        ('Prodigy Auth Settings', {
            'fields': ('role', 'is_verified', 'verification_token', 'otp_secret'),
            'classes': ('collapse',)
        }),
        ('Security Settings', {
            'fields': ('failed_login_attempts', 'account_locked_until'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Prodigy Auth Settings', {
            'fields': ('email', 'role', 'is_verified')
        }),
    )
    
    readonly_fields = ('verification_token', 'failed_login_attempts', 'account_locked_until')
    
    actions = ['send_verification_email', 'verify_users', 'make_admin', 'make_user', 'reset_failed_attempts']
    
    def role_badge(self, obj):
        """Display role with colored badge"""
        if obj.role == 'admin':
            return format_html(
                '<span style="background: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">ADMIN</span>'
            )
        else:
            return format_html(
                '<span style="background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">USER</span>'
            )
    role_badge.short_description = 'Role'
    
    def verification_status(self, obj):
        """Display verification status with icon"""
        if obj.is_verified:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">Verified</span>'
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">Unverified</span>'
            )
    verification_status.short_description = 'Email Status'
    
    def admin_actions(self, obj):
        """Quick action buttons"""
        actions = []
        
        if not obj.is_verified:
            actions.append(
                f'<a href="#" onclick="sendVerificationEmail({obj.id})" style="color: #007bff; text-decoration: none; margin-right: 10px;">Send Verification</a>'
            )
        
        if obj.failed_login_attempts > 0:
            actions.append(
                f'<a href="#" onclick="resetFailedAttempts({obj.id})" style="color: #ffc107; text-decoration: none; margin-right: 10px;">Reset Attempts</a>'
            )
        
        return format_html(' | '.join(actions)) if actions else '-'
    admin_actions.short_description = 'Quick Actions'
    
    def send_verification_email(self, request, queryset):
        """Send verification email to selected users"""
        count = 0
        for user in queryset:
            if not user.is_verified:
                if not user.verification_token:
                    user.verification_token = str(uuid.uuid4())
                    user.save()
                
                success = email_service.send_verification_email(user, user.verification_token)
                if success:
                    count += 1
        
        self.message_user(request, f'Verification emails sent to {count} users.')
    send_verification_email.short_description = "Send verification emails"
    
    def verify_users(self, request, queryset):
        """Manually verify selected users"""
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} users verified successfully.')
    verify_users.short_description = "Verify selected users"
    
    def make_admin(self, request, queryset):
        """Make selected users admins"""
        count = queryset.update(role='admin')
        self.message_user(request, f'{count} users promoted to admin.')
    make_admin.short_description = "Make admin"
    
    def make_user(self, request, queryset):
        """Make selected users regular users"""
        count = queryset.update(role='user')
        self.message_user(request, f'{count} users changed to regular user.')
    make_user.short_description = "Make regular user"
    
    def reset_failed_attempts(self, request, queryset):
        """Reset failed login attempts"""
        count = queryset.update(failed_login_attempts=0, account_locked_until=None)
        self.message_user(request, f'Failed login attempts reset for {count} users.')
    reset_failed_attempts.short_description = "Reset failed attempts"

# Customize admin site
admin.site.site_header = "Prodigy Auth Administration"
admin.site.site_title = "Prodigy Auth Admin"
admin.site.index_title = "Welcome to Prodigy Auth Administration"