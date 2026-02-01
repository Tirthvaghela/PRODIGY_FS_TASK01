# Email Provider Configurations for Prodigy Auth

# Gmail Configuration (Recommended for Development)
GMAIL_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'prodigyauth.system@gmail.com',
    'EMAIL_HOST_PASSWORD': 'your-app-password',
    'DEFAULT_FROM_EMAIL': 'Prodigy Auth System <prodigyauth.system@gmail.com>',
}

# Outlook/Hotmail Configuration
OUTLOOK_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp-mail.outlook.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'prodigyauth@outlook.com',
    'EMAIL_HOST_PASSWORD': 'your-password',
    'DEFAULT_FROM_EMAIL': 'Prodigy Auth <prodigyauth@outlook.com>',
}

# SendGrid Configuration (Production)
SENDGRID_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.sendgrid.net',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'apikey',
    'EMAIL_HOST_PASSWORD': 'your-sendgrid-api-key',
    'DEFAULT_FROM_EMAIL': 'Prodigy Auth <noreply@prodigyauth.com>',
}

# Mailgun Configuration (Production)
MAILGUN_CONFIG = {
    'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
    'EMAIL_HOST': 'smtp.mailgun.org',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'postmaster@mg.prodigyauth.com',
    'EMAIL_HOST_PASSWORD': 'your-mailgun-password',
    'DEFAULT_FROM_EMAIL': 'Prodigy Auth <noreply@prodigyauth.com>',
}

# Professional Email Suggestions
PROFESSIONAL_EMAILS = [
    'system@prodigyauth.com',
    'noreply@prodigyauth.dev',
    'auth@prodigyauth.io',
    'notifications@prodigyauth.app',
    'support@prodigyauth.platform',
    'admin@prodigyauth.system',
    'security@prodigyauth.secure',
    'verify@prodigyauth.verify',
]