#!/usr/bin/env python3
"""
Check database structure and sample data for schedule implementation
"""
import sqlite3

def check_database_structure():
    print("📋 Checking Database Structure and Data...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check students table structure
        print("\n🎓 Students Table Structure:")
        cursor.execute('PRAGMA table_info(students)')
        student_columns = cursor.fetchall()
        for row in student_columns:
            print(f"   {row[1]} ({row[2]})")
        
        # Check sample student data
        print("\n🎓 Sample Students Data:")
        cursor.execute('SELECT student_id, first_name, last_name, class_name, section FROM students LIMIT 3')
        students = cursor.fetchall()
        for s in students:
            print(f"   ID: {s[0]}, Name: {s[1]} {s[2]}, Class: {s[3]}-{s[4]}")
        
        # Check timetable table structure
        print("\n📅 Timetable Table Structure:")
        cursor.execute('PRAGMA table_info(timetable)')
        timetable_columns = cursor.fetchall()
        for row in timetable_columns:
            print(f"   {row[1]} ({row[2]})")
        
        # Check existing schedules
        print("\n📅 Sample Schedule Data:")
        cursor.execute('''
            SELECT class_name, section, day_of_week, period_number, subject, start_time, end_time 
            FROM timetable 
            ORDER BY class_name, section, day_of_week, period_number 
            LIMIT 5
        ''')
        schedules = cursor.fetchall()
        for sch in schedules:
            print(f"   {sch[0]}-{sch[1]} {sch[2]} P{sch[3]}: {sch[4]} ({sch[5]}-{sch[6]})")
        
        # Check department mapping (the current department structure)
        print("\n🏫 Current Class/Department Structure:")
        cursor.execute('SELECT DISTINCT class_name, section FROM students ORDER BY class_name, section')
        departments = cursor.fetchall()
        for dept in departments:
            print(f"   {dept[0]}-{dept[1]}")
        
        # Check schedule data for CSIT-A specifically
        print("\n🔍 CSIT-A Schedule Example:")
        cursor.execute('''
            SELECT day_of_week, period_number, subject, start_time, end_time 
            FROM timetable 
            WHERE class_name = 'CSIT' AND section = 'A'
            ORDER BY 
                CASE day_of_week 
                    WHEN 'Monday' THEN 1
                    WHEN 'Tuesday' THEN 2 
                    WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4
                    WHEN 'Friday' THEN 5
                    WHEN 'Saturday' THEN 6
                    ELSE 7
                END,
                period_number
            LIMIT 10
        ''')
        csit_schedule = cursor.fetchall()
        for cs in csit_schedule:
            print(f"   {cs[0]} P{cs[1]}: {cs[2]} ({cs[3]}-{cs[4]})")
        
        conn.close()
        print(f"\n✅ Database structure check completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database_structure()