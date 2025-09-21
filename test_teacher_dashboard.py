import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db
import sqlite3
from werkzeug.security import generate_password_hash

def test_teacher_dashboard():
    # Initialize database
    init_db()
    
    # Create test teacher
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Clean up any existing test teacher
    cursor.execute('DELETE FROM teachers WHERE teacher_id = ?', ('TEST_TEACHER',))
    cursor.execute('DELETE FROM users WHERE username = ?', ('testteacher',))
    conn.commit()
    
    # Create new test teacher user
    password_hash = generate_password_hash('teacherpass')
    cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)', 
                   ('testteacher', password_hash, 'teacher', 'teacher@example.com'))
    user_id = cursor.lastrowid
    
    cursor.execute('INSERT INTO teachers (user_id, teacher_id, first_name, last_name, subject, class_name, section) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (user_id, 'TEST_TEACHER', 'Jane', 'Smith', 'Mathematics', '10', 'A'))
    conn.commit()
    conn.close()
    
    print("Test teacher created successfully")
    
    # Test the teacher dashboard flow
    with app.test_client() as client:
        # Test login page access
        response = client.get('/login')
        print(f"1. Login page access: {response.status_code}")
        
        # Test login with teacher credentials
        response = client.post('/login', data={
            'username': 'testteacher',
            'password': 'teacherpass'
        })
        print(f"2. Teacher login POST status: {response.status_code}")
        
        # Follow redirects
        if response.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            print(f"   Redirecting to: {location}")
            
            # Follow redirect to dashboard
            response = client.get(location)
            print(f"3. After redirect status: {response.status_code}")
            
            if response.status_code in [301, 302]:
                next_location = response.headers.get('Location', '')
                print(f"   Second redirect to: {next_location}")
                response = client.get(next_location)
                print(f"4. Final page status: {response.status_code}")
        
        # Test direct access to teacher dashboard
        print("\n--- Testing direct teacher dashboard access ---")
        response = client.get('/teacher/dashboard')
        print(f"5. Direct teacher dashboard access: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            print("=== TEACHER DASHBOARD ANALYSIS ===")
            
            # Check for key elements
            checks = [
                ('Dashboard renders', True),
                ('Welcome message', 'Welcome,' in content),
                ('Teacher name', 'Jane Smith' in content or ('Jane' in content and 'Smith' in content)),
                ('Dashboard title', 'Teacher Dashboard' in content),
                ('Calendar icon', 'fa-calendar' in content),
                ('Teacher icon', 'fa-chalkboard-teacher' in content),
                ('Navigation', 'navbar' in content),
                ('Stats cards', 'card bg-primary' in content),
                ('Current date', 'September' in content or 'Saturday' in content),
            ]
            
            for check_name, result in checks:
                status = "✓" if result else "✗"
                print(f"{status} {check_name}")
            
            # Look for the welcome section
            if 'Welcome,' in content:
                start = content.find('Welcome,')
                end = content.find('</h1>', start) if content.find('</h1>', start) != -1 else start + 100
                welcome_section = content[start:end]
                print(f"\nWelcome section: {welcome_section}")
                
            # Check for any unrendered template variables
            if '{{' in content or '}}' in content:
                print("\n⚠ WARNING: Found unrendered template variables")
                import re
                variables = re.findall(r'\{\{[^}]+\}\}', content)
                for var in variables[:3]:  # Show first 3
                    print(f"  {var}")
            else:
                print("\n✓ All template variables rendered correctly")
                
        else:
            print(f"✗ Teacher dashboard access failed with status: {response.status_code}")
            if response.status_code in [301, 302]:
                print(f"Redirecting to: {response.headers.get('Location', 'Unknown')}")

if __name__ == '__main__':
    test_teacher_dashboard()