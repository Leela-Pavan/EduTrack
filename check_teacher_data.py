#!/usr/bin/env python3
"""
Check teacher data in database
"""
import sqlite3

def check_teacher_data():
    print("📋 Checking Teacher Data...")
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check teacher names
        cursor.execute('SELECT teacher_id, first_name, last_name, subject FROM teachers LIMIT 5')
        teachers = cursor.fetchall()
        
        print("\n🧑‍🏫 Sample Teachers:")
        for t in teachers:
            name = f"{t[1]} {t[2]}" if t[1] and t[2] else (t[1] or t[2] or "No name")
            print(f"   ID: {t[0]}, Name: {name}, Subject: {t[3]}")
        
        # Check users table for teacher names
        cursor.execute('''
            SELECT u.id, u.username, t.first_name, t.last_name 
            FROM users u 
            LEFT JOIN teachers t ON u.id = t.user_id 
            WHERE u.role = 'teacher' 
            LIMIT 5
        ''')
        
        user_teachers = cursor.fetchall()
        print("\n👤 Teacher Users:")
        for ut in user_teachers:
            name = f"{ut[2]} {ut[3]}" if ut[2] and ut[3] else (ut[2] or ut[3] or ut[1] or "No name")
            print(f"   User ID: {ut[0]}, Username: {ut[1]}, Name: {name}")
        
        # Check current schedule entries with teacher info
        cursor.execute('''
            SELECT t.class_name, t.section, t.day_of_week, t.subject, t.teacher_id,
                   te.first_name, te.last_name, u.username
            FROM timetable t
            LEFT JOIN teachers te ON t.teacher_id = te.user_id
            LEFT JOIN users u ON t.teacher_id = u.id
            LIMIT 5
        ''')
        
        schedules = cursor.fetchall()
        print("\n📅 Sample Schedule Entries:")
        for s in schedules:
            teacher_name = f"{s[5]} {s[6]}" if s[5] and s[6] else (s[5] or s[6] or s[7] or "Unknown")
            print(f"   {s[0]}-{s[1]} {s[2]}: {s[3]} (Teacher: {teacher_name})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_teacher_data()