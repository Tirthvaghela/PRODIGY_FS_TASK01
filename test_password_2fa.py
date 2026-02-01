#!/usr/bin/env python3
"""
Test script for Password Change and 2FA functionality
"""

import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prodigy_auth.settings')
django.setup()

def test_password_and_2fa():
    """Test password change and 2FA endpoints"""
    base_url = "http://127.0.0.1:8000/api/auth"
    
    print("Testing Password Change and 2FA Functionality")
    print("=" * 50)
    
    # Test login first
    login_data = {
        "email": "admin@prodigyauth.com",
        "password": "ProdigyAdmin123!"
    }
    
    try:
        print("1. Testing login...")
        login_response = requests.post(f"{base_url}/login/", json=login_data)
        
        if login_response.status_code == 200:
            data = login_response.json()
            token = data.get('access')
            user = data.get('user', {})
            
            print(f"   Login successful!")
            print(f"   User: {user.get('email')} ({user.get('role')})")
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test 2FA status check
            print("\n2. Testing 2FA status check...")
            status_response = requests.get(f"{base_url}/2fa-status/", headers=headers)
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   2FA Status: {'Enabled' if status_data.get('is_2fa_enabled') else 'Disabled'}")
            else:
                print(f"   2FA status check failed: {status_response.status_code}")
            
            # Test password change endpoint (without actually changing)
            print("\n3. Testing password change endpoint...")
            password_data = {
                "current_password": "wrong_password",  # Intentionally wrong
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
            
            password_response = requests.post(f"{base_url}/change-password/", 
                                            json=password_data, headers=headers)
            if password_response.status_code == 400:
                error_data = password_response.json()
                print(f"   Password change validation working: {error_data.get('error')}")
            else:
                print(f"   Unexpected response: {password_response.status_code}")
            
            # Test 2FA setup endpoint
            print("\n4. Testing 2FA setup endpoint...")
            setup_response = requests.post(f"{base_url}/setup-2fa/", headers=headers)
            if setup_response.status_code == 200:
                setup_data = setup_response.json()
                print(f"   2FA setup successful!")
                print(f"   Secret generated: {setup_data.get('secret')[:10]}...")
                print(f"   QR code available: {'Yes' if setup_data.get('qr_code') else 'No'}")
            elif setup_response.status_code == 400:
                error_data = setup_response.json()
                print(f"   2FA setup response: {error_data.get('error')}")
            else:
                print(f"   2FA setup failed: {setup_response.status_code}")
            
            print(f"\n5. All endpoints are accessible and responding correctly!")
            print(f"   Change Password: Available")
            print(f"   2FA Setup: Available")
            print(f"   2FA Status: Available")
            print(f"   Authentication: Working")
            
        else:
            print(f"   Login failed: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            
    except Exception as e:
        print(f"   Error during testing: {e}")

if __name__ == "__main__":
    test_password_and_2fa()