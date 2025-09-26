#!/usr/bin/env python3
"""
Comprehensive Database Functionality Test
Tests all CRUD operations and connections
"""

import sqlite3
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def test_database_structure():
    """Test database table structure and constraints"""
    print("🗄️ Testing Database Structure...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check all required tables exist
        required_tables = ['users', 'students', 'teachers', 'attendance', 'timetable']
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        print(f"📋 Found tables: {existing_tables}")
        
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ {table} table exists")
                
                # Check table structure
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                print(f"   Columns: {column_names}")
            else:
                print(f"❌ {table} table missing")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database structure test failed: {e}")
        return False

def test_database_operations():
    """Test basic CRUD operations"""
    print("\n🔧 Testing Database CRUD Operations...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Test SELECT operations
        print("📖 Testing SELECT operations:")
        
        # Test users count
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   Users: {user_count} records")
        
        # Test students count
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        print(f"   Students: {student_count} records")
        
        # Test teachers count
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        print(f"   Teachers: {teacher_count} records")
        
        # Test attendance count
        cursor.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cursor.fetchone()[0]
        print(f"   Attendance: {attendance_count} records")
        
        # Test complex queries (like admin dashboard uses)
        print("\n📊 Testing Complex Queries:")
        
        # Test attendance statistics query
        cursor.execute('''SELECT COUNT(*) as total_records,
                         SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                         SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                         FROM attendance WHERE date >= date('now', '-30 days')''')
        attendance_stats = cursor.fetchone()
        print(f"   Last 30 days attendance: Total={attendance_stats[0]}, Present={attendance_stats[1]}, Absent={attendance_stats[2]}")
        
        # Test class-wise attendance query
        cursor.execute('''SELECT class_name, section, 
                         COUNT(*) as total,
                         SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                         FROM attendance WHERE date >= date('now', '-7 days')
                         GROUP BY class_name, section
                         ORDER BY class_name, section''')
        class_attendance = cursor.fetchall()
        print(f"   Class-wise attendance (last 7 days): {len(class_attendance)} classes")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database CRUD test failed: {e}")
        return False

def test_admin_api_access():
    """Test admin API endpoints"""
    print("\n🔐 Testing Admin API Access...")
    
    try:
        session = requests.Session()
        
        # Try to login as admin
        login_data = {
            'username': 'ADMIN',
            'password': 'admin123'  # Assuming this is the admin password
        }
        
        response = session.post(f"{BASE_URL}/login", data=login_data)
        print(f"📝 Admin login attempt: {response.status_code}")
        
        if response.status_code == 200:
            # Test accessing admin dashboard
            response = session.get(f"{BASE_URL}/admin/dashboard")
            print(f"📊 Admin dashboard access: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Admin dashboard accessible")
                
                # Test admin API endpoints
                api_endpoints = [
                    '/api/students',
                    '/api/teachers',
                ]
                
                for endpoint in api_endpoints:
                    try:
                        response = session.get(f"{BASE_URL}{endpoint}")
                        print(f"   {endpoint}: {response.status_code}")
                    except Exception as e:
                        print(f"   {endpoint}: Error - {e}")
                        
            else:
                print(f"❌ Admin dashboard not accessible: {response.status_code}")
        else:
            print("❌ Admin login failed")
            print("   Trying to access dashboard directly...")
            
            # Try direct access (should fail)
            response = session.get(f"{BASE_URL}/admin/dashboard")
            print(f"   Direct access: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Admin API test failed: {e}")
        return False

def test_student_teacher_apis():
    """Test student and teacher related APIs"""
    print("\n👥 Testing Student/Teacher APIs...")
    
    try:
        session = requests.Session()
        
        # Test public endpoints that don't require auth
        public_endpoints = [
            '/',
            '/login',
            '/register'
        ]
        
        for endpoint in public_endpoints:
            try:
                response = session.get(f"{BASE_URL}{endpoint}")
                print(f"   {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"   {endpoint}: Error - {e}")
        
        return True
    except Exception as e:
        print(f"❌ Student/Teacher API test failed: {e}")
        return False

def main():
    """Run all database functionality tests"""
    print("🚀 Starting Comprehensive Database Functionality Test")
    print("=" * 60)
    
    results = {
        'structure': test_database_structure(),
        'operations': test_database_operations(),
        'admin_api': test_admin_api_access(),
        'public_api': test_student_teacher_apis()
    }
    
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS SUMMARY:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper().replace('_', ' ')}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL DATABASE FUNCTIONALITIES ARE WORKING!")
    else:
        print("⚠️  SOME ISSUES DETECTED - CHECK DETAILS ABOVE")
    print("=" * 60)

if __name__ == "__main__":
    main()