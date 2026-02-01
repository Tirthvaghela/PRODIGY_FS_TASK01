"""
Django management command to test email system
Usage: python manage.py test_email [email_address]
"""

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from accounts.email_service import email_service
from accounts.models import CustomUser
import uuid

class Command(BaseCommand):
    help = 'Test the email system configuration and templates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email address to send test emails to'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['all', 'simple', 'verification', 'welcome', 'reset'],
            default='all',
            help='Type of email test to run'
        )

    def handle(self, *args, **options):
        email_address = options['email']
        test_type = options['type']
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Testing Prodigy Auth Email System')
        )
        self.stdout.write('=' * 50)
        
        # Show configuration
        self.stdout.write(f"📧 Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"📧 SMTP Host: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
        self.stdout.write(f"📧 From Email: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"📧 Test Email: {email_address}")
        self.stdout.write('')
        
        # Run tests based on type
        if test_type in ['all', 'simple']:
            self.test_simple_email(email_address)
        
        if test_type in ['all', 'verification']:
            self.test_verification_email(email_address)
        
        if test_type in ['all', 'welcome']:
            self.test_welcome_email(email_address)
        
        if test_type in ['all', 'reset']:
            self.test_reset_email(email_address)
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('✅ Email testing completed!')
        )
        
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
            self.stdout.write(f"📧 Check {email_address} for test emails")
        else:
            self.stdout.write("📁 Check 'sent_emails' folder for email files")

    def test_simple_email(self, email_address):
        """Test simple email sending"""
        self.stdout.write("📨 Testing simple email...")
        try:
            send_mail(
                subject='🧪 Prodigy Auth Test Email',
                message='This is a test email from Prodigy Auth management command.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_address],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS('✅ Simple email sent successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Simple email failed: {e}')
            )

    def test_verification_email(self, email_address):
        """Test verification email template"""
        self.stdout.write("📨 Testing verification email...")
        try:
            test_user = CustomUser(
                username='testuser',
                email=email_address,
                first_name='Test',
                last_name='User'
            )
            
            verification_token = str(uuid.uuid4())
            success = email_service.send_verification_email(test_user, verification_token)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Verification email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Verification email failed!')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Verification email failed: {e}')
            )

    def test_welcome_email(self, email_address):
        """Test welcome email template"""
        self.stdout.write("📨 Testing welcome email...")
        try:
            test_user = CustomUser(
                username='testuser',
                email=email_address,
                first_name='Test',
                last_name='User',
                is_verified=True
            )
            
            success = email_service.send_welcome_email(test_user)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Welcome email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Welcome email failed!')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Welcome email failed: {e}')
            )

    def test_reset_email(self, email_address):
        """Test password reset email template"""
        self.stdout.write("📨 Testing password reset email...")
        try:
            test_user = CustomUser(
                username='testuser',
                email=email_address,
                first_name='Test',
                last_name='User'
            )
            
            reset_token = str(uuid.uuid4())
            success = email_service.send_password_reset_email(test_user, reset_token)
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS('✅ Password reset email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('❌ Password reset email failed!')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Password reset email failed: {e}')
            )