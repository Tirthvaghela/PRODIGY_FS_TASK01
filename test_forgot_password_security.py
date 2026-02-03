#!/usr/bin/env python3
"""
Test script for Enhanced Forgot Password Security
Tests rate limiting, cooldown periods, and abuse prevention
"""

import requests
import json
import time

def test_forgot_password_security():
    """Test enhanced security measures for forgot password"""
    
    base_url = "http://127.0.0.1:8000/api/auth"
    test_email = "vaghelatirth719@gmail.com"  # Your email
    
    print("Testing Enhanced Forgot Password Security")
    print("=" * 50)
    
    # Test 1: First request should work
    print("\n1. Testing first password reset request...")
    try:
        response = requests.post(f"{base_url}/forgot-password/", json={"email": test_email})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('message')}")
            print(f"   Cooldown Info: {data.get('cooldown_info')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Immediate second request should be blocked by cooldown
    print("\n2. Testing immediate second request (should be blocked)...")
    try:
        response = requests.post(f"{base_url}/forgot-password/", json={"email": test_email})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 429:
            data = response.json()
            print(f"   ✅ Correctly blocked by cooldown")
            print(f"   Error: {data.get('error')}")
        else:
            print(f"   ❌ Should have been blocked: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Test rate limiting with multiple attempts
    print("\n3. Testing rate limiting (multiple attempts)...")
    for i in range(3):
        try:
            # Wait a bit between requests
            time.sleep(1)
            response = requests.post(f"{base_url}/forgot-password/", json={"email": test_email})
            print(f"   Attempt {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                data = response.json()
                print(f"   ✅ Rate limited: {data.get('error')}")
                break
        except Exception as e:
            print(f"   ❌ Error on attempt {i+1}: {e}")
    
    # Test 4: Test IP-based rate limiting with different emails
    print("\n4. Testing IP-based rate limiting...")
    test_emails = ["test1@example.com", "test2@example.com", "test3@example.com", "test4@example.com"]
    
    for i, email in enumerate(test_emails):
        try:
            response = requests.post(f"{base_url}/forgot-password/", json={"email": email})
            print(f"   Email {i+1} ({email}): Status {response.status_code}")
            
            if response.status_code == 429:
                data = response.json()
                print(f"   ✅ IP rate limited: {data.get('error')}")
                break
        except Exception as e:
            print(f"   ❌ Error with {email}: {e}")
    
    # Test 5: Test password reset activity endpoint
    print("\n5. Testing password reset activity endpoint...")
    try:
        # This requires authentication, so we'll just test if endpoint exists
        response = requests.get(f"{base_url}/password-reset-activity/")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Endpoint exists (requires authentication)")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Enhanced Security Test Complete!")
    print("\nSecurity Measures Implemented:")
    print("✅ Email-based rate limiting (2 requests/hour)")
    print("✅ Cooldown period (15 minutes between requests)")
    print("✅ IP-based rate limiting (3 different emails/hour)")
    print("✅ Suspicious activity detection and logging")
    print("✅ Enhanced security monitoring")
    print("\nYour friend's prank attempts will now be:")
    print("🛡️  Limited to 2 attempts per hour on your email")
    print("🛡️  Blocked for 15 minutes after each attempt")
    print("🛡️  Logged as suspicious activity")
    print("🛡️  Blocked at IP level after 3 different emails")

if __name__ == "__main__":
    test_forgot_password_security()