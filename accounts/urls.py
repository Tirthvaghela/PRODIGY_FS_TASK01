from django.urls import path
from .views import (
    RegisterView, 
    login_view, 
    UserProfileView,
    logout_view,
    admin_dashboard,
    admin_users_list,
    admin_send_verification,
    admin_toggle_user_status,
    admin_reset_failed_attempts,
    admin_change_user_role,
    admin_verify_user,
    verify_email,
    resend_verification,
    user_stats,
    change_password,
    setup_2fa,
    verify_2fa_setup,
    disable_2fa,
    get_2fa_status,
    verify_2fa_login,
    forgot_password,
    reset_password,
    validate_reset_token,
    regenerate_backup_codes,
    verify_backup_code,
    get_active_sessions,
    terminate_session,
    terminate_all_sessions
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify-email/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('user-stats/', user_stats, name='user_stats'),
    
    # Password and 2FA endpoints
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
    path('validate-reset-token/<str:token>/', validate_reset_token, name='validate_reset_token'),
    path('setup-2fa/', setup_2fa, name='setup_2fa'),
    path('verify-2fa-setup/', verify_2fa_setup, name='verify_2fa_setup'),
    path('verify-2fa-login/', verify_2fa_login, name='verify_2fa_login'),
    path('disable-2fa/', disable_2fa, name='disable_2fa'),
    path('2fa-status/', get_2fa_status, name='get_2fa_status'),
    path('regenerate-backup-codes/', regenerate_backup_codes, name='regenerate_backup_codes'),
    path('verify-backup-code/', verify_backup_code, name='verify_backup_code'),
    
    # Session management endpoints
    path('sessions/', get_active_sessions, name='get_active_sessions'),
    path('terminate-session/', terminate_session, name='terminate_session'),
    path('terminate-all-sessions/', terminate_all_sessions, name='terminate_all_sessions'),
    
    # Admin endpoints
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/users/', admin_users_list, name='admin_users_list'),
    path('admin/send-verification/', admin_send_verification, name='admin_send_verification'),
    path('admin/toggle-user-status/', admin_toggle_user_status, name='admin_toggle_user_status'),
    path('admin/reset-failed-attempts/', admin_reset_failed_attempts, name='admin_reset_failed_attempts'),
    path('admin/change-user-role/', admin_change_user_role, name='admin_change_user_role'),
    path('admin/verify-user/', admin_verify_user, name='admin_verify_user'),
]