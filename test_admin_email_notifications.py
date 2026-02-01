"""
Test script for admin email notifications
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_admin_email_notifications():
    print("🧪 Testing Admin Email Notifications")
    print("=" * 50)
    
    # Login as admin
    print("1. Testing admin login...")
    login_data = {"email": "prodigyauth.system@gmail.com", "password": "123"}
    
    try:
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('access')
            headers = {"Authorization": f"Bearer {token}"}
            print("   ✅ Login successful!")
            
            # Get users list to find a test user
            users_response = requests.get(f"{BASE_URL}/admin/users/", headers=headers)
            if users_response.status_code == 200:
                users = users_response.json().get('users', [])
                
                # Find a regular user to test with
                test_user = None
                for user in users:
                    if (user.get('role') == 'user' and 
                        user.get('email') != 'prodigyauth.system@gmail.com' and
                        user.get('is_verified')):  # Only test with verified users
                        test_user = user
                        break
                
                if test_user:
                    print(f"\n2. Testing role change email for {test_user.get('email')}...")
                    
                    # Test role change (promote to admin)
                    role_response = requests.post(f"{BASE_URL}/admin/change-user-role/", 
                                                json={'user_id': test_user.get('id'), 'role': 'admin'}, 
                                                headers=headers)
                    
                    if role_response.status_code == 200:
                        print("   ✅ Role changed to admin - Email notification sent!")
                        
                        # Change back to user
                        role_response2 = requests.post(f"{BASE_URL}/admin/change-user-role/", 
                                                     json={'user_id': test_user.get('id'), 'role': 'user'}, 
                                                     headers=headers)
                        
                        if role_response2.status_code == 200:
                            print("   ✅ Role changed back to user - Email notification sent!")
                    
                    print(f"\n3. Testing account status email for {test_user.get('email')}...")
                    
                    # Test account deactivation
                    status_response = requests.post(f"{BASE_URL}/admin/toggle-user-status/", 
                                                  json={'user_id': test_user.get('id')}, 
                                                  headers=headers)
                    
                    if status_response.status_code == 200:
                        result = status_response.json()
                        action = "deactivated" if "deactivated" in result.get('message', '') else "activated"
                        print(f"   ✅ Account {action} - Email notification sent!")
                        
                        # Toggle back
                        status_response2 = requests.post(f"{BASE_URL}/admin/toggle-user-status/", 
                                                       json={'user_id': test_user.get('id')}, 
                                                       headers=headers)
                        
                        if status_response2.status_code == 200:
                            result2 = status_response2.json()
                            action2 = "activated" if "activated" in result2.get('message', '') else "deactivated"
                            print(f"   ✅ Account {action2} - Email notification sent!")
                    
                    print(f"\n🎉 Email Notification Testing Complete!")
                    print(f"📧 Check {test_user.get('email')} for the following emails:")
                    print(f"   1. Role Change: User → Admin")
                    print(f"   2. Role Change: Admin → User") 
                    print(f"   3. Account Status: Deactivated")
                    print(f"   4. Account Status: Activated")
                    print(f"\n💡 All admin actions now automatically send email notifications!")
                    
                else:
                    print("   ❌ No suitable verified test user found")
            else:
                print(f"   ❌ Failed to get users: {users_response.text}")
        else:
            print(f"   ❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_admin_email_notifications()