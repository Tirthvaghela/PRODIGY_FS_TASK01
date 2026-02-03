#!/usr/bin/env python3
"""
Test script for Updated Forgot Password functionality
Tests no rate limiting and alternative password reset methods
"""

import requests
import json

def test_updated_forgot_password():
    """Test updated forgot password with no rate limiting and alternative methods"""
    
    base_url = "http://127.0.0.1:8000/api/auth"
    
    print("Testing Updated Forgot Password Functionality (No Rate Limiting)")
    print("=" * 65)
    
    # Test 1: Regular email reset (should work multiple times now)
    print("\n1. Testing regular email reset (no rate limiting)...")
    test_email = "admin@prodigyauth.com"
    
    for i in range(3):
        try:
            response = requests.post(f"{base_url}/forgot-password/", json={"email": test_email})
            print(f"   Attempt {i+1}: Status {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('message')}")
            else:
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error on attempt {i+1}: {e}")
    
    # Test 2: Username-only reset
    print("\n2. Testing username-only reset...")
    try:
        response = requests.post(f"{base_url}/forgot-password-username/", json={"username": "admin"})
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('message')}")
            print(f"   Email Hint: {data.get('email_hint', 'Not provided')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Alternative reset with security question
    print("\n3. Testing alternative reset with security question...")
    try:
        response = requests.post(f"{base_url}/forgot-password-alternative/", json={
            "email": "admin@prodigyauth.com",
            "username": "admin", 
            "security_answer": "admin"
        })
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('message')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Alternative reset with wrong security answer
    print("\n4. Testing alternative reset with wrong security answer...")
    try:
        response = requests.post(f"{base_url}/forgot-password-alternative/", json={
            "email": "admin@prodigyauth.com",
            "username": "admin", 
            "security_answer": "wronganswer"
        })
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Correctly rejected: {data.get('error')}")
            print(f"   Hint provided: {data.get('hint', 'None')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Non-existing user tests
    print("\n5. Testing with non-existing users...")
    
    # Email method
    try:
        response = requests.post(f"{base_url}/forgot-password/", json={"email": "nonexistent@example.com"})
        print(f"   Email method - Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly identified non-existing email")
    except Exception as e:
        print(f"   ❌ Email method error: {e}")
    
    # Username method
    try:
        response = requests.post(f"{base_url}/forgot-password-username/", json={"username": "nonexistentuser"})
        print(f"   Username method - Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly identified non-existing username")
    except Exception as e:
        print(f"   ❌ Username method error: {e}")
    
    print("\n" + "=" * 65)
    print("Updated Forgot Password Test Complete!")
    print("\nChanges Made:")
    print("✅ REMOVED: 2-hour rate limiting")
    print("✅ REMOVED: 15-minute cooldown periods")
    print("✅ REMOVED: IP-based rate limiting")
    print("✅ ADDED: Username-only password reset")
    print("✅ ADDED: Security question alternative reset")
    print("✅ ADDED: Temporary password generation")
    print("✅ UPDATED: Frontend with multiple reset methods")
    print("\nNew Reset Methods Available:")
    print("📧 Email Reset: Traditional reset link via email")
    print("👤 Username Reset: Temporary password via username")
    print("🔐 Security Question: Temporary password via security answer")
    print("\nSecurity Features:")
    print("🔒 Temporary passwords must be changed after login")
    print("📝 All reset attempts are still logged for audit")
    print("✉️ Professional email templates for all methods")

if __name__ == "__main__":
    test_updated_forgot_password()