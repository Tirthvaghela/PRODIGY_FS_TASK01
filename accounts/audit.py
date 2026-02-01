"""
Audit Logging Utility for Prodigy Auth
Provides easy-to-use functions for logging security events
"""

from .models import AuditLog
import logging

logger = logging.getLogger(__name__)

def log_audit_event(action, user=None, ip_address=None, user_agent=None, 
                   details=None, success=True, admin_user=None, request=None):
    """
    Log an audit event for compliance and security monitoring
    
    Args:
        action: Action type (from AuditLog.ACTION_CHOICES)
        user: User object (optional)
        ip_address: IP address (optional, will extract from request if provided)
        user_agent: User agent string (optional, will extract from request if provided)
        details: Additional details as dict (optional)
        success: Whether the action was successful (default: True)
        admin_user: Admin user who performed the action (optional)
        request: Django request object (optional, for auto-extracting IP/UA)
    """
    
    # Extract IP and user agent from request if provided
    if request:
        if not ip_address:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0].strip()
            else:
                ip_address = request.META.get('REMOTE_ADDR', '127.0.0.1')
        
        if not user_agent:
            user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Default values
    if not ip_address:
        ip_address = '127.0.0.1'
    if not user_agent:
        user_agent = ''
    if not details:
        details = {}
    
    try:
        audit_log = AuditLog.objects.create(
            user=user,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details,
            success=success,
            admin_user=admin_user
        )
        
        logger.info(f"Audit log created: {action} for user {user} from {ip_address}")
        return audit_log
        
    except Exception as e:
        logger.error(f"Failed to create audit log: {e}")
        return None

def log_login_attempt(user, success, ip_address, user_agent, details=None):
    """Log a login attempt"""
    action = 'login' if success else 'failed_login'
    return log_audit_event(
        action=action,
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details or {},
        success=success
    )

def log_admin_action(admin_user, action, target_user=None, ip_address=None, 
                    user_agent=None, details=None, request=None):
    """Log an admin action"""
    return log_audit_event(
        action=action,
        user=target_user,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details or {},
        success=True,
        admin_user=admin_user,
        request=request
    )

def log_security_event(action, user=None, ip_address=None, details=None, request=None):
    """Log a security-related event"""
    return log_audit_event(
        action=action,
        user=user,
        ip_address=ip_address,
        details=details or {},
        success=False,  # Security events are typically failures
        request=request
    )

def get_user_audit_logs(user, limit=50):
    """Get recent audit logs for a user"""
    return AuditLog.objects.filter(user=user).order_by('-timestamp')[:limit]

def get_admin_audit_logs(admin_user, limit=50):
    """Get recent audit logs for admin actions"""
    return AuditLog.objects.filter(admin_user=admin_user).order_by('-timestamp')[:limit]

def get_security_audit_logs(hours=24, limit=100):
    """Get recent security-related audit logs"""
    from django.utils import timezone
    from datetime import timedelta
    
    since = timezone.now() - timedelta(hours=hours)
    security_actions = ['failed_login', 'account_locked', 'suspicious_activity']
    
    return AuditLog.objects.filter(
        action__in=security_actions,
        timestamp__gte=since
    ).order_by('-timestamp')[:limit]