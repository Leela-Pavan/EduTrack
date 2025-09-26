#!/usr/bin/env python3
"""
Simple test to verify teacher API data structure
"""
import requests
import json

def test_teacher_api():
    print("🧪 Testing Teacher API Data Structure...")
    
    session = requests.Session()
    base_url = "http://localhost:5000"
    
    try:
        # Test login with proper data
        print("\n1. Testing admin login...")
        login_data = {
            'email': 'admin@school.com',
            'password': 'admin123'
        }
        
        # First try to access login page
        login_page = session.get(f"{base_url}/login")
        if login_page.status_code != 200:
            print(f"❌ Cannot access login page - Status: {login_page.status_code}")
            return
            
        login_response = session.post(f"{base_url}/login", data=login_data)
        
        if login_response.status_code == 200 and ("admin" in login_response.text.lower() or "dashboard" in login_response.text.lower()):
            print("✅ Admin logged in successfully")
        else:
            print(f"❌ Login failed - Status: {login_response.status_code}")
            print("Response preview:", login_response.text[:200])
            return
        
        # Test teachers API directly
        print("\n2. Testing teachers API...")
        api_response = session.get(f"{base_url}/api/teachers")
        
        print(f"API Response Status: {api_response.status_code}")
        
        if api_response.status_code == 200:
            teachers_data = api_response.json()
            print(f"✅ Teachers API working - Found {len(teachers_data)} teachers")
            
            if teachers_data:
                print(f"\n3. First teacher data:")
                teacher = teachers_data[0]
                for key, value in teacher.items():
                    if key == 'password':
                        display_value = "••••••••" if value and value != 'Not set' else value
                    else:
                        display_value = value
                    print(f"   {key}: {display_value}")
                    
                # Check the specific fix
                username = teacher.get('username')
                password = teacher.get('password')
                
                print(f"\n4. Fix verification:")
                if 'username' in teacher and 'password' in teacher:
                    print(f"   ✅ Both username and password fields present")
                    if username != password:
                        print(f"   ✅ Username and password are different (fix successful)")
                    else:
                        print(f"   ⚠️  Username and password are the same")
                else:
                    print(f"   ❌ Missing username or password field")
            else:
                print("⚠️  No teachers found in database")
                
        else:
            print(f"❌ Teachers API failed - Status: {api_response.status_code}")
            print("Response:", api_response.text[:300])
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_teacher_api()