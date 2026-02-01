# 🚀 Deployment Guide

## Environment Setup

### 1. Copy Environment Template
```bash
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your actual values:

```env
# Generate a strong secret key
SECRET_KEY=your-super-secret-django-key-here

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### 3. Gmail App Password Setup

1. Enable 2-Step Verification in your Google Account
2. Go to Google Account Settings → Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"
4. Use the 16-character password in your `.env` file

### 4. Database Setup

For production, update `settings.py` to use PostgreSQL:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### 5. Security Settings

For production deployment:

```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-app.herokuapp.com
RATELIMIT_ENABLE=True
```

## Test User Accounts

The system includes these test accounts:

- **Admin**: admin@prodigyauth.com (password: ProdigyAdmin123!)
- **Regular User**: mihirvaghela1811@gmail.com (has 2FA enabled)

## Security Features

- Rate limiting enabled
- JWT token blacklisting
- 2FA with backup codes
- Comprehensive audit logging
- Session management
- Email notifications

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrated
- [ ] Static files collected
- [ ] HTTPS enabled
- [ ] Email SMTP working
- [ ] Rate limiting enabled
- [ ] Security headers configured