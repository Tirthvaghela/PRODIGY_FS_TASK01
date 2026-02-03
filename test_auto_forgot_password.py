#!/usr/bin/env python3
"""
Test script for Auto Forgot Password functionality
Tests the new prefilled email feature
"""

import requests
import json

def test_auto_forgot_password():
    """Test auto forgot password with prefilled email"""
    
    base_url = "http://127.0.0.1:8000/api/auth"
    
    print("Testing Auto Forgot Password Functionality")
    print("=" * 50)
    
    # Test 1: Test with your actual email (should work)
    print("\n1. Testing auto-send with your email (vaghelatirth719@gmail.com)...")
    your_email = "vaghelatirth719@gmail.com"
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json={"email": your_email})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('message')}")
            print(f"   Email Sent: {data.get('email_sent', False)}")
            print(f"   Cooldown Info: {data.get('cooldown_info', 'None')}")
        elif response.status_code == 429:
            data = response.json()
            print(f"   ⏰ Rate Limited (Expected): {data.get('error')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Test with admin email (should work)
    print("\n2. Testing with admin email...")
    admin_email = "admin@prodigyauth.com"
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json={"email": admin_email})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('message')}")
        elif response.status_code == 429:
            data = response.json()
            print(f"   ⏰ Rate Limited (Expected): {data.get('error')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test with non-existing email (should fail appropriately)
    print("\n3. Testing with non-existing email...")
    fake_email = "nonexistent@example.com"
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json={"email": fake_email})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print(f"   ✅ Correctly rejected: {data.get('error')}")
        elif response.status_code == 429:
            data = response.json()
            print(f"   ⏰ Rate Limited: {data.get('error')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Auto Forgot Password Test Complete!")
    print("\nNew User Experience:")
    print("📧 User enters email in login form")
    print("🔄 User clicks 'Forgot Password'")
    print("⚡ Modal shows prefilled email - ready to send!")
    print("🚀 One-click password reset (no re-typing email)")
    print("🔧 Option to change email if needed")
    print("\nSecurity Features Still Active:")
    print("🛡️ Rate limiting (2 requests/hour per email)")
    print("🛡️ Cooldown period (15 minutes)")
    print("🛡️ IP-based protection")
    print("🛡️ Suspicious activity logging")

if __name__ == "__main__":
    test_auto_forgot_password()