import requests
import json

def test_admin_endpoints():
    base_url = "http://localhost:5000"
    
    print("Testing Admin Endpoints")
    print("=" * 30)
    
    # First, let's try to access the admin dashboard to see if we're logged in
    print("1. Testing admin dashboard access...")
    try:
        response = requests.get(f"{base_url}/admin_dashboard")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Admin dashboard accessible")
        elif response.status_code == 302:
            print("   ✗ Redirected - likely not logged in as admin")
        else:
            print(f"   ✗ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Connection error: {e}")
        print("   Make sure the Flask app is running!")
        return
    
    # Test login first
    print("\n2. Testing admin login...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    session = requests.Session()
    
    try:
        response = session.post(f"{base_url}/login", data=login_data)
        print(f"   Login status: {response.status_code}")
        
        if response.status_code == 200 or response.status_code == 302:
            print("   ✓ Login appears successful")
            
            # Now test the admin endpoints with the session
            print("\n3. Testing add student endpoint...")
            
            student_data = {
                'student_id': 'TEST_API_001',
                'email': 'test@api.com',
                'first_name': 'API',
                'last_name': 'Test',
                'department': 'Computer Science',
                'section': 'CSIT-A',
                'mobile': '9999999999'
            }
            
            response = session.post(
                f"{base_url}/api/add_student",
                json=student_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Add student status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            # Test add teacher endpoint
            print("\n4. Testing add teacher endpoint...")
            
            teacher_data = {
                'teacher_id': 'TEST_TEACH_001',
                'email': 'teacher@api.com',
                'first_name': 'API',
                'last_name': 'Teacher',
                'subject': 'Mathematics',
                'department': 'Computer Science',
                'section': 'CSIT-A',
                'mobile': '8888888888'
            }
            
            response = session.post(
                f"{base_url}/api/add_teacher",
                json=teacher_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"   Add teacher status: {response.status_code}")
            print(f"   Response: {response.text}")
            
        else:
            print(f"   ✗ Login failed with status: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Error during API test: {e}")

if __name__ == "__main__":
    test_admin_endpoints()