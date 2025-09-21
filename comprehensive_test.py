import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db
import sqlite3
from werkzeug.security import generate_password_hash

def comprehensive_test():
    # Initialize database
    init_db()
    
    # Create test student
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Clean up any existing test user
    cursor.execute('DELETE FROM students WHERE student_id = ?', ('TEST123',))
    cursor.execute('DELETE FROM users WHERE username = ?', ('testuser',))
    conn.commit()
    
    # Create new test user
    password_hash = generate_password_hash('testpass')
    cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)', 
                   ('testuser', password_hash, 'student', 'test@example.com'))
    user_id = cursor.lastrowid
    
    cursor.execute('INSERT INTO students (user_id, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, 'TEST123', 'Test', 'User', '10', 'A', 'Science', 'Math', 'Engineering'))
    conn.commit()
    conn.close()
    
    print("Test user created successfully")
    
    # Test the flow with Flask test client
    with app.test_client() as client:
        # Test login page access
        response = client.get('/login')
        print(f"1. Login page access: {response.status_code}")
        
        # Test login with correct credentials
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        print(f"2. Login POST status: {response.status_code}")
        print(f"   Login response headers: {dict(response.headers)}")
        
        # Follow the redirect if there is one
        if response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            print(f"   Redirecting to: {location}")
            
            # Follow redirect manually
            response = client.get(location)
            print(f"3. After redirect status: {response.status_code}")
            
            # If redirected to dashboard, try to follow that redirect too
            if response.status_code in [301, 302]:
                next_location = response.headers.get('Location', '')
                print(f"   Second redirect to: {next_location}")
                response = client.get(next_location)
                print(f"4. Final page status: {response.status_code}")
        
        # Test direct access to student dashboard
        print("\n--- Testing direct dashboard access ---")
        response = client.get('/student/dashboard')
        print(f"5. Direct dashboard access: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: Student dashboard accessible!")
            content = response.data.decode('utf-8')
            if 'Welcome, Test User' in content:
                print("SUCCESS: Dashboard shows correct student name")
            else:
                print("WARNING: Dashboard doesn't show expected content")
                print(f"First 500 chars: {content[:500]}")
        else:
            print(f"ERROR: Dashboard returned {response.status_code}")
            if response.status_code in [301, 302]:
                print(f"Redirecting to: {response.headers.get('Location', 'Unknown')}")
            else:
                print(f"Response content: {response.data.decode('utf-8')[:500]}")

if __name__ == '__main__':
    comprehensive_test()