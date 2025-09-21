import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
import sqlite3
from werkzeug.security import generate_password_hash

def test_admin_dashboard():
    with app.test_client() as client:
        # Login as admin and follow redirects
        response = client.post('/login', data={
            'username': 'admin', 
            'password': 'adminpass'
        }, follow_redirects=True)
        
        print(f"Login status: {response.status_code}")
        print(f"Final URL: {response.request.url}")
        
        # Try direct access
        response = client.get('/admin/dashboard')
        print(f"Direct admin dashboard: {response.status_code}")
        
        if response.status_code == 200:
            content = response.data.decode('utf-8')
            if 'Administrator Dashboard' in content:
                print("✓ Admin dashboard renders correctly")
                if 'September' in content:
                    print("✓ Current date displays correctly")
                else:
                    print("✗ Date issue detected")
            else:
                print("✗ Admin dashboard content issue")
        else:
            print(f"✗ Admin dashboard failed: {response.status_code}")

if __name__ == '__main__':
    test_admin_dashboard()