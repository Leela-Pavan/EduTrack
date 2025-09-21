import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db
import sqlite3
from werkzeug.security import generate_password_hash

def final_test():
    # Test with Flask test client
    with app.test_client() as client:
        # Login with our test user
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        
        # Access student dashboard
        response = client.get('/student/dashboard')
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            print("=== FINAL TEST RESULTS ===")
            
            # Look for the specific welcome section
            if 'Welcome,' in content:
                start = content.find('Welcome,')
                end = content.find('</h1>', start) if content.find('</h1>', start) != -1 else start + 100
                welcome_section = content[start:end]
                print(f"Welcome section: {welcome_section}")
                
                if 'Welcome, Test User' in content:
                    print("✓ SUCCESS: Student dashboard shows correct name!")
                elif 'Test' in welcome_section and 'User' in welcome_section:
                    print("✓ SUCCESS: Student dashboard shows student name correctly!")
                else:
                    print("⚠ WARNING: Student name display needs checking")
            else:
                print("✗ FAIL: No welcome section found")
                
            # Additional checks
            checks = [
                ('Dashboard renders', True),
                ('Contains navigation', 'navbar' in content),
                ('Contains stats cards', 'card bg-primary' in content),
                ('Contains attendance data', 'Present Days' in content),
                ('Contains calendar', 'fa-calendar' in content),
            ]
            
            for check_name, result in checks:
                status = "✓" if result else "✗"
                print(f"{status} {check_name}")
                
        else:
            print(f"✗ FAIL: Dashboard access failed with status: {response.status_code}")

if __name__ == '__main__':
    final_test()