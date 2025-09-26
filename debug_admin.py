#!/usr/bin/env python3
"""
Debug script to test admin database operations
"""

import sqlite3
import json
import sys

def check_database_schema():
    """Check if the database schema matches what the admin endpoints expect"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("=== Database Schema Check ===")
    
    # Check if students table exists and get its schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students';")
    students_schema = cursor.fetchone()
    if students_schema:
        print("Students table schema:")
        print(students_schema[0])
    else:
        print("ERROR: Students table does not exist!")
    
    # Check if teachers table exists and get its schema
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='teachers';")
    teachers_schema = cursor.fetchone()
    if teachers_schema:
        print("\nTeachers table schema:")
        print(teachers_schema[0])
    else:
        print("ERROR: Teachers table does not exist!")
    
    conn.close()

def test_add_student():
    """Test adding a student to the database"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("\n=== Testing Student Addition ===")
    
    # Test data
    student_data = {
        'student_id': 'TEST001',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'Student',
        'department': 'Computer Science',
        'section': 'CSIT-A',
        'mobile': '1234567890'
    }
    
    try:
        # Try to insert the student
        cursor.execute("""
            INSERT INTO students (student_id, email, first_name, last_name, department, section, mobile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_data['student_id'],
            student_data['email'],
            student_data['first_name'],
            student_data['last_name'],
            student_data['department'],
            student_data['section'],
            student_data['mobile']
        ))
        
        conn.commit()
        print(f"✓ Successfully added student: {student_data['student_id']}")
        
        # Verify the student was added
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_data['student_id'],))
        result = cursor.fetchone()
        if result:
            print("✓ Student verified in database")
        else:
            print("✗ Student not found after insertion!")
            
    except Exception as e:
        print(f"✗ Error adding student: {e}")
    
    conn.close()

def test_add_teacher():
    """Test adding a teacher to the database"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("\n=== Testing Teacher Addition ===")
    
    # Test data
    teacher_data = {
        'teacher_id': 'TEACH001',
        'email': 'teacher@example.com',
        'first_name': 'Test',
        'last_name': 'Teacher',
        'subject': 'Mathematics',
        'department': 'Computer Science',
        'section': 'CSIT-A',
        'mobile': '9876543210'
    }
    
    try:
        # Try to insert the teacher
        cursor.execute("""
            INSERT INTO teachers (teacher_id, email, first_name, last_name, subject, department, section, mobile)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            teacher_data['teacher_id'],
            teacher_data['email'],
            teacher_data['first_name'],
            teacher_data['last_name'],
            teacher_data['subject'],
            teacher_data['department'],
            teacher_data['section'],
            teacher_data['mobile']
        ))
        
        conn.commit()
        print(f"✓ Successfully added teacher: {teacher_data['teacher_id']}")
        
        # Verify the teacher was added
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = ?", (teacher_data['teacher_id'],))
        result = cursor.fetchone()
        if result:
            print("✓ Teacher verified in database")
        else:
            print("✗ Teacher not found after insertion!")
            
    except Exception as e:
        print(f"✗ Error adding teacher: {e}")
    
    conn.close()

def show_existing_data():
    """Show existing students and teachers"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("\n=== Existing Data ===")
    
    # Show students
    cursor.execute("SELECT COUNT(*) FROM students")
    student_count = cursor.fetchone()[0]
    print(f"Total students: {student_count}")
    
    if student_count > 0:
        cursor.execute("SELECT student_id, first_name, last_name, department, section FROM students LIMIT 5")
        students = cursor.fetchall()
        print("Sample students:")
        for student in students:
            print(f"  - {student[0]}: {student[1]} {student[2]} ({student[3]}, {student[4]})")
    
    # Show teachers
    cursor.execute("SELECT COUNT(*) FROM teachers")
    teacher_count = cursor.fetchone()[0]
    print(f"Total teachers: {teacher_count}")
    
    if teacher_count > 0:
        cursor.execute("SELECT teacher_id, first_name, last_name, subject, department FROM teachers LIMIT 5")
        teachers = cursor.fetchall()
        print("Sample teachers:")
        for teacher in teachers:
            print(f"  - {teacher[0]}: {teacher[1]} {teacher[2]} ({teacher[3]}, {teacher[4]})")
    
    conn.close()

def cleanup_test_data():
    """Remove test data"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("\n=== Cleaning up test data ===")
    
    try:
        cursor.execute("DELETE FROM students WHERE student_id = 'TEST001'")
        cursor.execute("DELETE FROM teachers WHERE teacher_id = 'TEACH001'")
        conn.commit()
        print("✓ Test data cleaned up")
    except Exception as e:
        print(f"Error cleaning up: {e}")
    
    conn.close()

if __name__ == "__main__":
    print("EduTrack Admin Debug Tool")
    print("=" * 50)
    
    check_database_schema()
    show_existing_data()
    test_add_student()
    test_add_teacher()
    cleanup_test_data()
    
    print("\nDebug complete!")