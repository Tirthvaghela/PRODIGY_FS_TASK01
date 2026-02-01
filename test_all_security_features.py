#!/usr/bin/env python3
"""
Comprehensive Security Features Test Suite
Tests all newly implemented security features for Prodigy Auth
"""

import os
import sys
import django
import requests
import json
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prodigy_auth.settings')
django.setup()

from accounts.models import AuditLog, UserSession, TwoFactorBackupCode
from django.contrib.auth import get_user_model

User = get_user_model()

class SecurityTestSuite:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/api/auth"
        self.admin_credentials = {
            "email": "admin@prodigyauth.com",
            "password": "ProdigyAdmin123!"
        }
        self.test_results = []
        
    def log_test(self, test_name, status, message):
        """Log test results"""
        icon = "✅" if status else "❌"
        print(f"{icon} {test_name}: {message}")
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message
        })
    
    def test_1_login_endpoint(self):
        """Test 1: Login Endpoint Functionality"""
        print("\n🔐 Test 1: Login Endpoint")
        
        try:
            response = requests.post(f"{self.base_url}/login/", 
                                   json=self.admin_credentials,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                if 'access' in data and 'refresh' in data and 'session_key' in data:
                    self.access_token = data['access']
                    self.refresh_token = data['refresh']
                    self.session_key = data['session_key']
                    self.log_test("Login Endpoint", True, "Login successful with tokens and session")
                    return True
                else:
                    self.log_test("Login Endpoint", False, "Missing tokens or session key in response")
            else:
                self.log_test("Login Endpoint", False, f"Login failed with status {response.status_code}")
                
        except Exception as e:
            self.log_test("Login Endpoint", False, f"Login request failed: {e}")
        
        return False
    
    def test_2_audit_logging(self):
        """Test 2: Audit Logging System"""
        print("\n📝 Test 2: Audit Logging")
        
        try:
            # Check if login was logged
            login_logs = AuditLog.objects.filter(action='login').order_by('-timestamp')[:1]
            
            if login_logs.exists():
                log = login_logs.first()
                if log.user and log.ip_address and log.success:
                    self.log_test("Audit Logging", True, f"Login logged: User {log.user.email}, IP {log.ip_address}")
                else:
                    self.log_test("Audit Logging", False, "Login log missing required fields")
            else:
                self.log_test("Audit Logging", False, "No login audit logs found")
                
        except Exception as e:
            self.log_test("Audit Logging", False, f"Audit log check failed: {e}")
    
    def test_3_session_management(self):
        """Test 3: Session Management"""
        print("\n🔗 Test 3: Session Management")
        
        if not hasattr(self, 'access_token'):
            self.log_test("Session Management", False, "No access token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Test get active sessions
            response = requests.get(f"{self.base_url}/sessions/", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'sessions' in data and len(data['sessions']) > 0:
                    session = data['sessions'][0]
                    if 'session_key' in session and 'ip_address' in session:
                        self.log_test("Session Management", True, f"Found {len(data['sessions'])} active sessions")
                    else:
                        self.log_test("Session Management", False, "Session data missing required fields")
                else:
                    self.log_test("Session Management", False, "No active sessions found")
            else:
                self.log_test("Session Management", False, f"Session endpoint failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Session Management", False, f"Session test failed: {e}")
    
    def test_4_rate_limiting(self):
        """Test 4: Rate Limiting Middleware"""
        print("\n🚦 Test 4: Rate Limiting")
        
        try:
            # Test multiple rapid requests to trigger rate limiting
            rate_limited = False
            
            for i in range(7):  # Try 7 requests (limit is 5)
                response = requests.post(f"{self.base_url}/login/", 
                                       json={"email": "test@test.com", "password": "wrong"},
                                       headers={'Content-Type': 'application/json'})
                
                if response.status_code == 429:
                    rate_limited = True
                    self.log_test("Rate Limiting", True, f"Rate limiting triggered after {i+1} requests")
                    break
                    
                time.sleep(0.1)  # Small delay between requests
            
            if not rate_limited:
                self.log_test("Rate Limiting", False, "Rate limiting not triggered (may be disabled)")
                
        except Exception as e:
            self.log_test("Rate Limiting", False, f"Rate limiting test failed: {e}")
    
    def test_5_2fa_backup_codes(self):
        """Test 5: 2FA Backup Codes"""
        print("\n🔑 Test 5: 2FA Backup Codes")
        
        if not hasattr(self, 'access_token'):
            self.log_test("2FA Backup Codes", False, "No access token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            # Check if user has 2FA enabled
            user = User.objects.get(email=self.admin_credentials['email'])
            
            if user.otp_secret:
                # Test regenerate backup codes
                response = requests.post(f"{self.base_url}/regenerate-backup-codes/", 
                                       headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'backup_codes' in data and len(data['backup_codes']) == 10:
                        self.log_test("2FA Backup Codes", True, f"Generated {len(data['backup_codes'])} backup codes")
                        
                        # Test backup code verification with invalid code
                        verify_response = requests.post(f"{self.base_url}/verify-backup-code/",
                                                      json={"code": "INVALID123"},
                                                      headers=headers)
                        
                        if verify_response.status_code == 400:
                            self.log_test("2FA Backup Code Validation", True, "Invalid backup code properly rejected")
                        else:
                            self.log_test("2FA Backup Code Validation", False, "Invalid backup code not rejected")
                    else:
                        self.log_test("2FA Backup Codes", False, "Incorrect number of backup codes generated")
                else:
                    self.log_test("2FA Backup Codes", False, f"Backup code generation failed: {response.status_code}")
            else:
                self.log_test("2FA Backup Codes", False, "User doesn't have 2FA enabled")
                
        except Exception as e:
            self.log_test("2FA Backup Codes", False, f"2FA backup codes test failed: {e}")
    
    def test_6_enhanced_logout(self):
        """Test 6: Enhanced Logout with Session Cleanup"""
        print("\n🚪 Test 6: Enhanced Logout")
        
        if not hasattr(self, 'access_token'):
            self.log_test("Enhanced Logout", False, "No access token available")
            return
            
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            logout_data = {
                "refresh_token": self.refresh_token,
                "session_key": self.session_key
            }
            
            response = requests.post(f"{self.base_url}/logout/", 
                                   json=logout_data,
                                   headers=headers)
            
            if response.status_code == 200:
                # Test if token is blacklisted
                test_response = requests.get(f"{self.base_url}/user-stats/", headers=headers)
                
                if test_response.status_code == 401:
                    self.log_test("Enhanced Logout", True, "Token properly blacklisted after logout")
                else:
                    self.log_test("Enhanced Logout", False, "Token still valid after logout")
            else:
                self.log_test("Enhanced Logout", False, f"Logout failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Enhanced Logout", False, f"Logout test failed: {e}")
    
    def test_7_database_models(self):
        """Test 7: New Database Models"""
        print("\n🗄️ Test 7: Database Models")
        
        try:
            # Test AuditLog model
            audit_count = AuditLog.objects.count()
            if audit_count > 0:
                self.log_test("AuditLog Model", True, f"Found {audit_count} audit log entries")
            else:
                self.log_test("AuditLog Model", False, "No audit log entries found")
            
            # Test UserSession model
            session_count = UserSession.objects.count()
            if session_count > 0:
                self.log_test("UserSession Model", True, f"Found {session_count} user sessions")
            else:
                self.log_test("UserSession Model", False, "No user sessions found")
            
            # Test TwoFactorBackupCode model
            backup_count = TwoFactorBackupCode.objects.count()
            self.log_test("TwoFactorBackupCode Model", True, f"Found {backup_count} backup codes")
            
        except Exception as e:
            self.log_test("Database Models", False, f"Database model test failed: {e}")
    
    def test_8_security_headers(self):
        """Test 8: Security Headers"""
        print("\n🛡️ Test 8: Security Headers")
        
        try:
            response = requests.get("http://127.0.0.1:8000/")
            headers = response.headers
            
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME type sniffing protection',
            }
            
            found_headers = 0
            for header, description in security_headers.items():
                if header in headers:
                    found_headers += 1
                    self.log_test(f"Security Header: {header}", True, f"{description}: {headers[header]}")
                else:
                    self.log_test(f"Security Header: {header}", False, f"Missing {description}")
            
            if found_headers > 0:
                self.log_test("Security Headers", True, f"Found {found_headers}/{len(security_headers)} security headers")
            else:
                self.log_test("Security Headers", False, "No security headers found")
                
        except Exception as e:
            self.log_test("Security Headers", False, f"Security headers test failed: {e}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🔒 COMPREHENSIVE SECURITY FEATURES TEST SUITE")
        print("=" * 60)
        
        # Run tests in order
        login_success = self.test_1_login_endpoint()
        self.test_2_audit_logging()
        self.test_3_session_management()
        self.test_4_rate_limiting()
        self.test_5_2fa_backup_codes()
        
        if login_success:
            self.test_6_enhanced_logout()
        
        self.test_7_database_models()
        self.test_8_security_headers()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("🔒 SECURITY TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['status'])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Security features are working correctly.")
        elif passed >= total * 0.8:
            print("✅ MOST TESTS PASSED! Minor issues to address.")
        else:
            print("⚠️ SEVERAL TESTS FAILED! Critical issues need attention.")
        
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            icon = "✅" if result['status'] else "❌"
            print(f"{icon} {result['test']}: {result['message']}")
        
        print("\n💡 NEXT STEPS:")
        failed_tests = [r for r in self.test_results if not r['status']]
        
        if failed_tests:
            print("Fix the following issues:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        else:
            print("  - All security features are working correctly!")
            print("  - System is ready for production deployment")
            print("  - Consider running load tests and penetration testing")

def main():
    """Main test runner"""
    print("Starting Prodigy Auth Security Test Suite...")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    
    # Wait for user confirmation
    input("Press Enter to start testing...")
    
    test_suite = SecurityTestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()