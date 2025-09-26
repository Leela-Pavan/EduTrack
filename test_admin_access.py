#!/usr/bin/env python3
"""
Test admin dashboard access and debug any issues
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_admin_dashboard_access():
    print("🔍 Testing Admin Dashboard Access...")
    
    session = requests.Session()
    
    # Step 1: Try to access admin dashboard without login
    print("\n1. Testing unauthorized access:")
    response = session.get(f"{BASE_URL}/admin/dashboard")
    print(f"   Status: {response.status_code}")
    print(f"   Redirected to: {response.url}")
    
    # Step 2: Login as admin
    print("\n2. Testing admin login:")
    login_data = {
        'username': 'ADMIN',
        'password': 'admin123'
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data)
    print(f"   Login status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    
    if response.status_code == 200:
        # Step 3: Try to access admin dashboard after login
        print("\n3. Testing authorized admin dashboard access:")
        response = session.get(f"{BASE_URL}/admin/dashboard")
        print(f"   Status: {response.status_code}")
        print(f"   Content length: {len(response.text)}")
        
        if response.status_code == 200:
            # Check if the page contains expected data
            content = response.text
            if "Total Students" in content:
                print("   ✅ Dashboard contains student data")
            else:
                print("   ❌ Dashboard missing student data")
                
            if "Total Teachers" in content:
                print("   ✅ Dashboard contains teacher data")
            else:
                print("   ❌ Dashboard missing teacher data")
                
            if "attendance_stats" in content or "Present" in content:
                print("   ✅ Dashboard contains attendance data")
            else:
                print("   ❌ Dashboard missing attendance data")
                
            # Check for any JavaScript errors in the page
            if "error" in content.lower():
                print("   ⚠️  Page might contain errors")
            
            print(f"   Page title: {'Admin Dashboard' if 'Admin Dashboard' in content else 'Unknown'}")
            
        else:
            print(f"   ❌ Failed to access dashboard: {response.status_code}")
            
        # Step 4: Test API endpoints
        print("\n4. Testing admin API endpoints:")
        api_endpoints = [
            '/api/students',
            '/api/teachers',
            '/api/attendance_stats'
        ]
        
        for endpoint in api_endpoints:
            try:
                response = session.get(f"{BASE_URL}{endpoint}")
                print(f"   {endpoint}: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"      Data count: {len(data)}")
                        elif isinstance(data, dict):
                            print(f"      Data keys: {list(data.keys())}")
                    except:
                        print(f"      Content length: {len(response.text)}")
            except Exception as e:
                print(f"   {endpoint}: Error - {e}")
    else:
        print("   ❌ Admin login failed")
        
        # Try alternative login attempts
        print("\n   Trying alternative admin credentials...")
        alt_credentials = [
            {'username': 'admin', 'password': 'admin'},
            {'username': 'admin', 'password': 'admin123'},
            {'username': 'ADMIN', 'password': 'ADMIN'},
        ]
        
        for creds in alt_credentials:
            response = session.post(f"{BASE_URL}/login", data=creds)
            print(f"      {creds['username']}/{creds['password']}: {response.status_code}")

def test_database_data_directly():
    print("\n📊 Testing Database Data Directly:")
    
    import sqlite3
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Test the exact queries from admin dashboard
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        print(f"   Total Students: {total_students}")
        
        cursor.execute('SELECT COUNT(*) FROM teachers')
        total_teachers = cursor.fetchone()[0]
        print(f"   Total Teachers: {total_teachers}")
        
        cursor.execute('''SELECT COUNT(*) as total_records,
                         SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                         SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                         FROM attendance WHERE date >= date('now', '-30 days')''')
        attendance_stats = cursor.fetchone()
        print(f"   Attendance Stats: Total={attendance_stats[0]}, Present={attendance_stats[1]}, Absent={attendance_stats[2]}")
        
        cursor.execute('''SELECT class_name, section, 
                         COUNT(*) as total,
                         SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                         FROM attendance WHERE date >= date('now', '-7 days')
                         GROUP BY class_name, section
                         ORDER BY class_name, section''')
        class_attendance = cursor.fetchall()
        print(f"   Class Attendance Records: {len(class_attendance)}")
        
        conn.close()
        
        print("   ✅ All database queries successful")
        
    except Exception as e:
        print(f"   ❌ Database query error: {e}")

if __name__ == "__main__":
    test_admin_dashboard_access()
    test_database_data_directly()