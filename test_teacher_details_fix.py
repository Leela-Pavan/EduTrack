#!/usr/bin/env python3
"""
Test script to verify teacher details display fix
"""
import requests
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def test_teacher_details():
    print("🧪 Testing Teacher Details Display Fix...")
    
    # Set up session with retries
    session = requests.Session()
    
    base_url = "http://localhost:5000"
    
    try:
        # Test login first
        print("\n1. Testing admin login...")
        login_data = {
            'email': 'admin@school.com',
            'password': 'admin123'
        }
        
        login_response = session.post(f"{base_url}/login", data=login_data, timeout=10)
        
        if login_response.status_code == 200 and "admin" in login_response.text.lower():
            print("✅ Admin logged in successfully")
        else:
            print(f"❌ Login failed - Status: {login_response.status_code}")
            return
        
        # Test teachers API
        print("\n2. Testing teachers API...")
        api_response = session.get(f"{base_url}/api/teachers", timeout=10)
        
        if api_response.status_code == 200:
            print("✅ Teachers API accessible")
            
            teachers_data = api_response.json()
            print(f"✅ Found {len(teachers_data)} teachers")
            
            # Check data structure
            if teachers_data:
                sample_teacher = teachers_data[0]
                print(f"\n3. Sample teacher data structure:")
                
                required_fields = ['teacher_id', 'name', 'subject', 'department', 'section', 'email', 'username', 'password']
                
                for field in required_fields:
                    if field in sample_teacher:
                        value = sample_teacher[field]
                        if field == 'password':
                            display_value = "••••••••" if value and value != 'Not set' else value
                        else:
                            display_value = value
                        print(f"   ✅ {field}: {display_value}")
                    else:
                        print(f"   ❌ Missing field: {field}")
                
                # Check for the specific issue
                print(f"\n4. Checking for username/password issue:")
                
                username = sample_teacher.get('username', '')
                password = sample_teacher.get('password', '')
                
                if username and password and username != password:
                    print(f"   ✅ Username and password are properly separated")
                    print(f"   ✅ Username: {username}")
                    print(f"   ✅ Password: {'••••••••' if password != 'Not set' else 'Not set'}")
                elif username == password:
                    print(f"   ❌ Username and password are the same: {username}")
                else:
                    print(f"   ⚠️  Username: {username or 'Not set'}")
                    print(f"   ⚠️  Password: {password or 'Not set'}")
                
        else:
            print(f"❌ Teachers API failed - Status: {api_response.status_code}")
            print(f"Response: {api_response.text[:200]}...")
            return
        
        # Test admin dashboard page
        print(f"\n5. Testing admin dashboard page...")
        dashboard_response = session.get(f"{base_url}/admin_dashboard", timeout=10)
        
        if dashboard_response.status_code == 200:
            print("✅ Admin dashboard accessible")
            
            # Check if the updated template has both username and password columns
            page_content = dashboard_response.text
            if "<th>Username</th>" in page_content and "<th>Password</th>" in page_content:
                print("✅ Template updated with separate Username and Password columns")
            else:
                print("❌ Template still missing proper Username/Password columns")
                
        else:
            print(f"❌ Dashboard failed - Status: {dashboard_response.status_code}")
        
        print(f"\n" + "="*50)
        print(f"🎉 TEACHER DETAILS DISPLAY TEST COMPLETED!")
        print(f"="*50)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("Make sure the Flask app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_teacher_details()