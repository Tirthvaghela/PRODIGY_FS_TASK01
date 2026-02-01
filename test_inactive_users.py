"""
Test script to check inactive users count
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api/auth"

def test_inactive_users_count():
    print("🧪 Testing Inactive Users Count")
    print("=" * 40)
    
    # Login as admin
    login_data = {"email": "prodigyauth.system@gmail.com", "password": "123"}
    
    try:
        response = requests.post(f"{BASE_URL}/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get('access')
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get dashboard stats
            dashboard_response = requests.get(f"{BASE_URL}/admin/dashboard/", headers=headers)
            if dashboard_response.status_code == 200:
                stats = dashboard_response.json().get('stats', {})
                
                print("📊 Current Dashboard Statistics:")
                print(f"   📊 Total Users: {stats.get('total_users', 0)}")
                print(f"   ✅ Verified Users: {stats.get('verified_users', 0)}")
                print(f"   ❌ Unverified Users: {stats.get('unverified_users', 0)}")
                print(f"   👑 Admin Users: {stats.get('admin_users', 0)}")
                print(f"   🔴 Inactive Users: {stats.get('inactive_users', 0)} (Admin deactivated)")
                print(f"   🔒 Locked Accounts: {stats.get('locked_accounts', 0)} (Failed login attempts)")
                print(f"   📅 Recent Registrations: {stats.get('recent_registrations', 0)}")
                
                print("\n🔍 Explanation:")
                print("   🔴 Inactive Users = Users deactivated by admin (is_active=False)")
                print("   🔒 Locked Accounts = Users locked due to failed login attempts")
                print("   📝 These are two different security mechanisms!")
                
                if stats.get('inactive_users', 0) > 0:
                    print(f"\n✅ You have {stats.get('inactive_users')} inactive user(s)")
                    print("   This includes mihirvaghela1811@gmail.com that you deactivated!")
                else:
                    print(f"\n❓ No inactive users found. The user might have been reactivated.")
                    
            else:
                print(f"❌ Dashboard request failed: {dashboard_response.text}")
        else:
            print(f"❌ Login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_inactive_users_count()