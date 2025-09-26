#!/usr/bin/env python3
"""
Check admin users and database data for debugging
"""

import sqlite3

def check_admin_data():
    print("🔍 Checking Admin Data Access...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check if there are any admin users
        print("\n1. Checking Admin Users:")
        cursor.execute("SELECT id, username, email, role FROM users WHERE role = 'admin'")
        admins = cursor.fetchall()
        
        if admins:
            print(f"✅ Found {len(admins)} admin user(s):")
            for admin in admins:
                print(f"   - ID: {admin[0]}, Username: {admin[1]}, Email: {admin[2]}, Role: {admin[3]}")
        else:
            print("❌ No admin users found!")
            print("   Creating an admin user...")
            
            # Create an admin user
            cursor.execute('''INSERT INTO users (username, email, password, role) 
                             VALUES (?, ?, ?, ?)''',
                          ('admin', 'admin@edutrack.com', 'pbkdf2:sha256:600000$salt$hash', 'admin'))
            conn.commit()
            print("✅ Admin user created: username='admin', email='admin@edutrack.com'")
        
        # Check students data
        print("\n2. Checking Students Data:")
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        print(f"   Total Students: {student_count}")
        
        if student_count > 0:
            cursor.execute("SELECT * FROM students LIMIT 3")
            sample_students = cursor.fetchall()
            print("   Sample students:")
            for student in sample_students:
                print(f"   - {student}")
        
        # Check teachers data
        print("\n3. Checking Teachers Data:")
        cursor.execute("SELECT COUNT(*) FROM teachers")
        teacher_count = cursor.fetchone()[0]
        print(f"   Total Teachers: {teacher_count}")
        
        if teacher_count > 0:
            cursor.execute("SELECT * FROM teachers LIMIT 3")
            sample_teachers = cursor.fetchall()
            print("   Sample teachers:")
            for teacher in sample_teachers:
                print(f"   - {teacher}")
        
        # Check attendance data
        print("\n4. Checking Attendance Data:")
        cursor.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cursor.fetchone()[0]
        print(f"   Total Attendance Records: {attendance_count}")
        
        if attendance_count > 0:
            cursor.execute("SELECT * FROM attendance LIMIT 3")
            sample_attendance = cursor.fetchall()
            print("   Sample attendance:")
            for attendance in sample_attendance:
                print(f"   - {attendance}")
        
        # Check table structure
        print("\n5. Checking Database Tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("   Available tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error checking admin data: {e}")

if __name__ == "__main__":
    check_admin_data()