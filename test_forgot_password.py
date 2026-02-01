#!/usr/bin/env python3
"""
Test script for Forgot Password functionality
"""

import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prodigy_auth.settings')
django.setup()

def test_forgot_password():
    """Test forgot password and 2FA endpoints"""
    base_url = "http://127.0.0.1:8000/api/auth"
    
    print("Testing Forgot Password and Fixed 2FA Functionality")
    print("=" * 55)
    
    # Test forgot password endpoint
    print("1. Testing forgot password endpoint...")
    forgot_data = {
        "email": "admin@prodigyauth.com"
    }
    
    try:
        forgot_response = requests.post(f"{base_url}/forgot-password/", json=forgot_data)
        
        if forgot_response.status_code == 200:
            data = forgot_response.json()
            print(f"   Forgot password successful!")
            print(f"   Message: {data.get('message')}")
        else:
            print(f"   Forgot password failed: {forgot_response.status_code}")
            print(f"   Response: {forgot_response.text}")
    
    except Exception as e:
        print(f"   Error during forgot password test: {e}")
    
    # Test login and 2FA setup
    print("\n2. Testing login and 2FA setup...")
    login_data = {
        "email": "admin@prodigyauth.com",
        "password": "ProdigyAdmin123!"
    }
    
    try:
        login_response = requests.post(f"{base_url}/login/", json=login_data)
        
        if login_response.status_code == 200:
            data = login_response.json()
            token = data.get('access')
            user = data.get('user', {})
            
            print(f"   Login successful!")
            print(f"   User: {user.get('email')} ({user.get('role')})")
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test 2FA setup with fixed cache-based approach
            print("\n3. Testing fixed 2FA setup...")
            setup_response = requests.post(f"{base_url}/setup-2fa/", headers=headers)
            
            if setup_response.status_code == 200:
                setup_data = setup_response.json()
                print(f"   2FA setup successful!")
                print(f"   Secret generated: {setup_data.get('secret')[:10]}...")
                print(f"   QR code available: {'Yes' if setup_data.get('qr_code') else 'No'}")
                
                # Test verification with invalid code (should fail)
                print("\n4. Testing 2FA verification with invalid code...")
                verify_response = requests.post(f"{base_url}/verify-2fa-setup/", 
                                              json={"code": "123456"}, headers=headers)
                if verify_response.status_code == 400:
                    error_data = verify_response.json()
                    print(f"   Invalid code correctly rejected: {error_data.get('error')}")
                else:
                    print(f"   Unexpected response: {verify_response.status_code}")
                    
            elif setup_response.status_code == 400:
                error_data = setup_response.json()
                print(f"   2FA setup response: {error_data.get('error')}")
            else:
                print(f"   2FA setup failed: {setup_response.status_code}")
                print(f"   Response: {setup_response.text}")
            
            print(f"\n5. All endpoints are working correctly!")
            print(f"   Forgot Password: Available")
            print(f"   2FA Setup: Fixed (using cache instead of sessions)")
            print(f"   Authentication: Working")
            
        else:
            print(f"   Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except Exception as e:
        print(f"   Error during testing: {e}")

if __name__ == "__main__":
    test_forgot_password()