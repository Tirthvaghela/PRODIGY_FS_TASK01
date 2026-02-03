#!/usr/bin/env python3
"""
Test script for the updated Forgot Password functionality
Tests email validation and appropriate responses
"""

import requests
import json

def test_forgot_password_validation():
    """Test forgot password with email validation"""
    
    base_url = "http://127.0.0.1:8000/api/auth"
    
    print("Testing Updated Forgot Password Functionality")
    print("=" * 50)
    
    # Test 1: Valid existing email
    print("\n1. Testing with existing email (admin@prodigyauth.com)...")
    existing_email_data = {
        "email": "admin@prodigyauth.com"
    }
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json=existing_email_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data.get('message')}")
            print(f"   Email Sent: {data.get('email_sent', False)}")
        else:
            print(f"   ❌ Failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Non-existing email
    print("\n2. Testing with non-existing email...")
    non_existing_email_data = {
        "email": "nonexistent@example.com"
    }
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json=non_existing_email_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 404:
            data = response.json()
            print(f"   ✅ Correctly identified non-existing email")
            print(f"   Error Message: {data.get('error')}")
            print(f"   Email Exists: {data.get('email_exists', 'Not specified')}")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Empty email
    print("\n3. Testing with empty email...")
    empty_email_data = {
        "email": ""
    }
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json=empty_email_data)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Correctly rejected empty email")
            print(f"   Error Message: {data.get('error')}")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Invalid email format
    print("\n4. Testing with invalid email format...")
    invalid_email_data = {
        "email": "invalid-email-format"
    }
    
    try:
        response = requests.post(f"{base_url}/forgot-password/", json=invalid_email_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("Forgot Password Validation Test Complete!")
    print("\nExpected Behavior:")
    print("✅ Existing email → 200 status, reset email sent")
    print("✅ Non-existing email → 404 status, clear error message")
    print("✅ Empty email → 400 status, validation error")
    print("✅ Invalid format → Handled by email validation")

if __name__ == "__main__":
    test_forgot_password_validation()