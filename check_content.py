import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, init_db
import sqlite3
from werkzeug.security import generate_password_hash

def check_dashboard_content():
    # Initialize database  
    init_db()
    
    # Test the flow with Flask test client
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
            print("=== DASHBOARD CONTENT ANALYSIS ===")
            print(f"Response length: {len(content)} characters")
            
            # Check for key elements
            checks = [
                ('Welcome message', 'Welcome, Test User' in content),
                ('Student name individual parts', 'Test' in content and 'User' in content),
                ('Dashboard title', 'Student Dashboard' in content),
                ('Calendar icon', 'fa-calendar' in content),
                ('User icon', 'fa-user-graduate' in content),
                ('Bootstrap classes', 'container-fluid' in content),
                ('Current date', 'September' in content or 'Saturday' in content),
            ]
            
            for check_name, result in checks:
                status = "✓ PASS" if result else "✗ FAIL"
                print(f"{status}: {check_name}")
            
            # Look for the specific welcome section
            if 'Welcome,' in content:
                start = content.find('Welcome,')
                end = content.find('</h1>', start) if content.find('</h1>', start) != -1 else start + 100
                welcome_section = content[start:end]
                print(f"\nWelcome section found: {welcome_section}")
            else:
                print("\nNo welcome section found")
                
            # Look for template variables that might not be rendered
            if '{{' in content or '}}' in content:
                print("\nWARNING: Found unrendered template variables:")
                import re
                variables = re.findall(r'\{\{[^}]+\}\}', content)
                for var in variables[:5]:  # Show first 5
                    print(f"  {var}")
                    
            # Show the header section specifically
            if '<h1' in content:
                start = content.find('<h1')
                end = content.find('</h1>', start) + 5
                header_section = content[start:end]
                print(f"\nHeader section: {header_section}")
        else:
            print(f"Dashboard access failed with status: {response.status_code}")

if __name__ == '__main__':
    check_dashboard_content()