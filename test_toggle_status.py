"""
Test script for toggle user status functionality
"""

import requests
import json

# Test endpoints
BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_toggle_user_status():
    print("🧪 Testing Toggle User Status")
    print("=" * 40)
    
    # Test login first to get admin token
    print("1. Testing admin login...")
    login_data = {
        "email": "prodigyauth.system@gmail.com",
        "password": "123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            headers = {"Authorization": f"Bearer {token}"}
            
            print("   ✅ Login successful!")
            
            # Get users list
            users_response = requests.get(f"{BASE_URL}/admin/users/", headers=headers)
            if users_response.status_code == 200:
                users_data = users_response.json()
                users = users_data.get('users', [])
                
                # Find a regular user to test with
                test_user = None
                for user in users:
                    if user.get('role') == 'user' and user.get('email') != 'prodigyauth.system@gmail.com':
                        test_user = user
                        break
                
                if test_user:
                    print(f"\n2. Testing toggle status for {test_user.get('email')}...")
                    print(f"   Current status: {'Active' if test_user.get('is_active') else 'Inactive'}")
                    
                    # Toggle status
                    toggle_response = requests.post(f"{BASE_URL}/admin/toggle-user-status/", 
                                                  json={'user_id': test_user.get('id')}, 
                                                  headers=headers)
                    
                    print(f"   Toggle Status Code: {toggle_response.status_code}")
                    
                    if toggle_response.status_code == 200:
                        result = toggle_response.json()
                        print(f"   ✅ {result.get('message')}")
                        
                        # Toggle back
                        toggle_back_response = requests.post(f"{BASE_URL}/admin/toggle-user-status/", 
                                                           json={'user_id': test_user.get('id')}, 
                                                           headers=headers)
                        
                        if toggle_back_response.status_code == 200:
                            result2 = toggle_back_response.json()
                            print(f"   ✅ {result2.get('message')}")
                            print("   ✅ Toggle functionality working perfectly!")
                        else:
                            print(f"   ❌ Toggle back failed: {toggle_back_response.text}")
                    else:
                        print(f"   ❌ Toggle failed: {toggle_response.text}")
                else:
                    print("   ❌ No suitable test user found")
            else:
                print(f"   ❌ Failed to get users: {users_response.text}")
        else:
            print(f"   ❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_toggle_user_status()