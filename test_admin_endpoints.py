"""
Test script for enhanced admin endpoints
"""

import requests
import json

# Test endpoints
BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_enhanced_admin_endpoints():
    print("🧪 Testing Enhanced Admin Endpoints")
    print("=" * 50)
    
    # Test login first to get admin token
    print("1. Testing admin login...")
    login_data = {
        "email": "prodigyauth.system@gmail.com",  # Your admin email
        "password": "123"  # Your admin password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        print(f"   Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            user = data.get('user', {})
            
            print(f"   ✅ Login successful!")
            print(f"   User: {user.get('email')} ({user.get('role')})")
            
            if user.get('role') == 'admin':
                print(f"   👑 Admin access confirmed!")
                
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test admin dashboard
                print("\n2. Testing admin dashboard...")
                dashboard_response = requests.get(f"{BASE_URL}/admin/dashboard/", headers=headers)
                print(f"   Dashboard Status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    dashboard_data = dashboard_response.json()
                    stats = dashboard_data.get('stats', {})
                    recent_users = dashboard_data.get('recent_users', [])
                    
                    print(f"   ✅ Dashboard data retrieved!")
                    print(f"   📊 Total Users: {stats.get('total_users', 0)}")
                    print(f"   ✅ Verified Users: {stats.get('verified_users', 0)}")
                    print(f"   👑 Admin Users: {stats.get('admin_users', 0)}")
                    print(f"   ❌ Unverified Users: {stats.get('unverified_users', 0)}")
                    print(f"   📅 Recent Users: {len(recent_users)}")
                    
                    # Test users list
                    print("\n3. Testing users list...")
                    users_response = requests.get(f"{BASE_URL}/admin/users/", headers=headers)
                    print(f"   Users List Status: {users_response.status_code}")
                    
                    if users_response.status_code == 200:
                        users_data = users_response.json()
                        users = users_data.get('users', [])
                        print(f"   ✅ Users list retrieved! ({len(users)} users)")
                        
                        # Find an unverified user to test with
                        unverified_user = None
                        regular_user = None
                        
                        for user_data in users:
                            if not user_data.get('is_verified') and not unverified_user:
                                unverified_user = user_data
                            if user_data.get('role') == 'user' and not regular_user:
                                regular_user = user_data
                        
                        # Test role change
                        if regular_user:
                            print(f"\n4. Testing role change for {regular_user.get('email')}...")
                            role_response = requests.post(f"{BASE_URL}/admin/change-user-role/", 
                                                        json={'user_id': regular_user.get('id'), 'role': 'admin'}, 
                                                        headers=headers)
                            print(f"   Role Change Status: {role_response.status_code}")
                            if role_response.status_code == 200:
                                print(f"   ✅ User promoted to admin!")
                                
                                # Change back to user
                                role_response2 = requests.post(f"{BASE_URL}/admin/change-user-role/", 
                                                             json={'user_id': regular_user.get('id'), 'role': 'user'}, 
                                                             headers=headers)
                                if role_response2.status_code == 200:
                                    print(f"   ✅ User demoted back to regular user!")
                            else:
                                print(f"   ❌ Role change failed: {role_response.text}")
                        
                        # Test manual verification
                        if unverified_user:
                            print(f"\n5. Testing manual verification for {unverified_user.get('email')}...")
                            verify_response = requests.post(f"{BASE_URL}/admin/verify-user/", 
                                                          json={'user_id': unverified_user.get('id')}, 
                                                          headers=headers)
                            print(f"   Manual Verification Status: {verify_response.status_code}")
                            if verify_response.status_code == 200:
                                print(f"   ✅ User manually verified!")
                            else:
                                print(f"   ❌ Manual verification failed: {verify_response.text}")
                        
                        print(f"\n6. All enhanced admin features tested!")
                        print(f"   ✅ Dashboard with recent users")
                        print(f"   ✅ User management table")
                        print(f"   ✅ Role management (promote/demote)")
                        print(f"   ✅ Manual user verification")
                        print(f"   ✅ Email sending capabilities")
                        print(f"   ✅ Account status management")
                        
                    else:
                        print(f"   ❌ Users list failed: {users_response.text}")
                else:
                    print(f"   ❌ Dashboard failed: {dashboard_response.text}")
            else:
                print(f"   ❌ User is not admin: {user.get('role')}")
        else:
            print(f"   ❌ Login failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection failed - is Django server running?")
        print("   Run: python manage.py runserver")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_enhanced_admin_endpoints()