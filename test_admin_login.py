#!/usr/bin/env python3
"""
Script to test admin login flow.
"""

import requests
import json

def test_admin_login():
    """Test admin login and dashboard access."""
    base_url = "http://127.0.0.1:5000"
    
    print("Testing admin login flow...")
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    try:
        # 1. Test login page access
        print("\n1. Accessing login page...")
        response = session.get(f"{base_url}/login")
        print(f"   Status: {response.status_code}")
        
        # 2. Test admin login
        print("\n2. Attempting admin login...")
        login_data = {
            'username': 'ADMIN',
            'password': 'ADMIN'
        }
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location', '')
            print(f"   Redirect to: {redirect_url}")
            
            # 3. Follow redirect to dashboard
            print("\n3. Following redirect to dashboard...")
            response = session.get(redirect_url, allow_redirects=False)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 302:
                final_url = response.headers.get('Location', '')
                print(f"   Final redirect to: {final_url}")
                
                # 4. Access final admin dashboard
                print("\n4. Accessing admin dashboard...")
                response = session.get(final_url)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ Admin dashboard loaded successfully!")
                    print(f"   Content length: {len(response.text)} characters")
                    
                    # Check if it contains admin dashboard content
                    if "Administrator Dashboard" in response.text:
                        print("   ✅ Admin dashboard content found!")
                    else:
                        print("   ❌ Admin dashboard content not found")
                        print("   First 500 characters of response:")
                        print(response.text[:500])
                else:
                    print(f"   ❌ Error accessing admin dashboard: {response.status_code}")
                    print(f"   Response: {response.text[:500]}")
            else:
                print(f"   ❌ Dashboard redirect failed: {response.status_code}")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_admin_login()