#!/usr/bin/env python3
"""
Script to test admin dashboard queries.
"""

import sqlite3
from datetime import datetime

def test_admin_queries():
    """Test the exact queries used in admin_dashboard."""
    print("Testing admin dashboard queries...")
    
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    try:
        # Test query 1: Count students
        print("\n1. Testing student count...")
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        print(f"   ✅ Total students: {total_students}")
        
        # Test query 2: Count teachers
        print("\n2. Testing teacher count...")
        cursor.execute('SELECT COUNT(*) FROM teachers')
        total_teachers = cursor.fetchone()[0]
        print(f"   ✅ Total teachers: {total_teachers}")
        
        # Test query 3: Attendance statistics
        print("\n3. Testing attendance statistics...")
        cursor.execute('''SELECT COUNT(*) as total_records,
                         SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                         SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                         FROM attendance WHERE date >= date('now', '-30 days')''')
        attendance_stats = cursor.fetchone()
        print(f"   ✅ Attendance stats: total={attendance_stats[0]}, present={attendance_stats[1]}, absent={attendance_stats[2]}")
        
        # Test query 4: Class-wise attendance
        print("\n4. Testing class-wise attendance...")
        cursor.execute('''SELECT class_name, section, 
                         COUNT(*) as total,
                         SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                         FROM attendance WHERE date >= date('now', '-7 days')
                         GROUP BY class_name, section
                         ORDER BY class_name, section''')
        class_attendance = cursor.fetchall()
        print(f"   ✅ Class attendance records: {len(class_attendance)}")
        for record in class_attendance:
            print(f"      - {record[0]}-{record[1]}: {record[3]}/{record[2]} present")
        
        # Test date formatting
        print("\n5. Testing date formatting...")
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        print(f"   ✅ Current date: {current_date}")
        
        conn.close()
        print("\n🎉 All queries executed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in queries: {e}")
        import traceback
        traceback.print_exc()
        conn.close()

if __name__ == "__main__":
    test_admin_queries()