"""
Comprehensive Email System Test for Prodigy Auth
Tests SMTP configuration and email templates
"""

import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prodigy_auth.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from accounts.email_service import email_service
from accounts.models import CustomUser
import uuid

def test_email_configuration():
    """Test email configuration and SMTP connection"""
    print("🔧 Testing Email Configuration...")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    
    if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER:
        print(f"✅ SMTP User: {settings.EMAIL_HOST_USER}")
        print(f"✅ SMTP Host: {settings.EMAIL_HOST}")
        print(f"✅ SMTP Port: {settings.EMAIL_PORT}")
        print(f"✅ Use TLS: {settings.EMAIL_USE_TLS}")
        return True
    else:
        print("❌ No SMTP credentials found - using file backend")
        return False

def test_simple_email():
    """Test basic email sending"""
    print("\n� Testing Simple Email...")
    try:
        send_mail(
            subject='🧪 Prodigy Auth Test Email',
            message='This is a test email from Prodigy Auth system.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['test@example.com'],  # This will be saved to file or sent via SMTP
            fail_silently=False,
        )
        print("✅ Simple email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Simple email failed: {e}")
        return False

def test_html_email():
    """Test HTML email with professional template"""
    print("\n🎨 Testing HTML Email...")
    try:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Email</title></head>
        <body style="font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
                <h1 style="color: #4979fe;">🧪 Prodigy Auth Test</h1>
                <p>This is a <strong>professional HTML email</strong> test from Prodigy Auth!</p>
                <div style="background: linear-gradient(135deg, #4979fe, #f7931e); color: white; padding: 20px; border-radius: 8px; text-align: center;">
                    <h2>Email System Working! ✅</h2>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = "This is a test email from Prodigy Auth system. Email system is working!"
        
        msg = EmailMultiAlternatives(
            subject='🎨 Prodigy Auth HTML Test Email',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['test@example.com']
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        print("✅ HTML email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ HTML email failed: {e}")
        return False

def test_email_service():
    """Test the professional email service"""
    print("\n🏢 Testing Professional Email Service...")
    
    # Create a test user (don't save to database)
    test_user = CustomUser(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    
    try:
        # Test verification email
        verification_token = str(uuid.uuid4())
        result1 = email_service.send_verification_email(test_user, verification_token)
        print(f"✅ Verification email: {'Success' if result1 else 'Failed'}")
        
        # Test welcome email
        result2 = email_service.send_welcome_email(test_user)
        print(f"✅ Welcome email: {'Success' if result2 else 'Failed'}")
        
        # Test password reset email
        reset_token = str(uuid.uuid4())
        result3 = email_service.send_password_reset_email(test_user, reset_token)
        print(f"✅ Password reset email: {'Success' if result3 else 'Failed'}")
        
        return result1 and result2 and result3
    except Exception as e:
        print(f"❌ Email service test failed: {e}")
        return False

def check_sent_emails():
    """Check sent emails directory if using file backend"""
    print("\n📁 Checking Sent Emails...")
    
    if settings.EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
        sent_emails_dir = Path('sent_emails')
        if sent_emails_dir.exists():
            email_files = list(sent_emails_dir.glob('*.log'))
            print(f"� Found {len(email_files)} email files:")
            for email_file in email_files[-5:]:  # Show last 5
                print(f"   - {email_file.name}")
            
            if email_files:
                print(f"\n📖 Latest email content preview:")
                latest_email = email_files[-1]
                with open(latest_email, 'r', encoding='utf-8') as f:
                    content = f.read()[:500]  # First 500 chars
                    print(content)
                    if len(content) == 500:
                        print("... (truncated)")
        else:
            print("❌ No sent_emails directory found")
    else:
        print("📧 Using SMTP - emails sent to actual recipients")

def main():
    """Run all email tests"""
    print("🚀 Prodigy Auth Email System Test")
    print("=" * 50)
    
    # Test configuration
    smtp_configured = test_email_configuration()
    
    # Test basic functionality
    simple_test = test_simple_email()
    html_test = test_html_email()
    service_test = test_email_service()
    
    # Check results
    check_sent_emails()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"✅ SMTP Configuration: {'Configured' if smtp_configured else 'File Backend'}")
    print(f"✅ Simple Email: {'Pass' if simple_test else 'Fail'}")
    print(f"✅ HTML Email: {'Pass' if html_test else 'Fail'}")
    print(f"✅ Email Service: {'Pass' if service_test else 'Fail'}")
    
    if smtp_configured and simple_test and html_test and service_test:
        print("\n🎉 All email tests passed! Your email system is ready!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("\n💡 Next Steps:")
    if smtp_configured:
        print("   - Your SMTP is configured and working")
        print("   - Test registration to receive real emails")
        print("   - Check your Gmail inbox for test emails")
    else:
        print("   - Emails are being saved to 'sent_emails' folder")
        print("   - Add Gmail credentials to .env to enable SMTP")
    
    print("   - Register a new user to test the full flow")
    print("   - Check the email verification process")

if __name__ == "__main__":
    main()