import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db
from werkzeug.test import Client
import sqlite3
from werkzeug.security import generate_password_hash

def test_student_login():
    # Ensure database is initialized
    init_db()
    
    # Create a test client
    with app.test_client() as client:
        # Test that we can access the login page
        response = client.get('/login')
        print(f"Login page status: {response.status_code}")
        
        # Create test student if doesn't exist
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('teststudent',))
        if cursor.fetchone()[0] == 0:
            password_hash = generate_password_hash('password123')
            cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)', 
                           ('teststudent', password_hash, 'student', 'test@test.com'))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO students (user_id, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           (user_id, 'TST001', 'Test', 'Student', '10', 'A', 'Science', 'Math', 'Engineer'))
            conn.commit()
        conn.close()
        
        # Try to login
        response = client.post('/login', data={
            'username': 'teststudent',
            'password': 'password123'
        }, follow_redirects=True)
        
        print(f"Login response status: {response.status_code}")
        print(f"Final URL: {response.request.url}")
        
        # Check if we're redirected to student dashboard
        if '/student/dashboard' in response.request.url:
            print("SUCCESS: Login redirected to student dashboard")
            
            # Try to access student dashboard directly
            response = client.get('/student/dashboard')
            print(f"Student dashboard status: {response.status_code}")
            
            if response.status_code == 200:
                print("SUCCESS: Student dashboard loaded successfully")
                # Check if the response contains expected elements
                if b'Welcome' in response.data:
                    print("SUCCESS: Dashboard contains welcome message")
                else:
                    print("WARNING: Dashboard doesn't contain welcome message")
            else:
                print(f"ERROR: Student dashboard returned status {response.status_code}")
                print(f"Response data: {response.data[:500]}")
        else:
            print(f"ERROR: Login did not redirect to student dashboard")
            print(f"Response data: {response.data[:500]}")

if __name__ == '__main__':
    test_student_login()