"""
Sample Data Setup Script for School Management System

This script creates test users and sample data for easy testing of the application.
Run this after starting the application for the first time to populate the database
with test accounts and sample data.

Usage: python setup_sample_data.py
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_sample_users():
    """Create sample users for testing"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("Creating sample users...")
    
    # Sample students
    students = [
        ('testuser', 'testpass', 'TEST123', 'Test', 'User', '10', 'A', 'Science,Math', 'Problem Solving', 'Engineer'),
        ('john_doe', 'password123', 'STU001', 'John', 'Doe', '10', 'A', 'Sports,Art', 'Leadership', 'Artist'),
        ('jane_smith', 'password123', 'STU002', 'Jane', 'Smith', '10', 'B', 'Music,Literature', 'Creativity', 'Writer'),
        ('mike_wilson', 'password123', 'STU003', 'Mike', 'Wilson', '11', 'A', 'Technology', 'Programming', 'Developer'),
        ('sara_jones', 'password123', 'STU004', 'Sara', 'Jones', '11', 'B', 'Science', 'Research', 'Scientist'),
    ]
    
    # Sample teachers
    teachers = [
        ('testteacher', 'teacherpass', 'TEST_TEACHER', 'Jane', 'Smith', 'Mathematics', '10', 'A'),
        ('prof_brown', 'teacher123', 'TEA001', 'Robert', 'Brown', 'Physics', '10', 'A'),
        ('prof_davis', 'teacher123', 'TEA002', 'Emily', 'Davis', 'Chemistry', '10', 'B'),
        ('prof_miller', 'teacher123', 'TEA003', 'David', 'Miller', 'English', '11', 'A'),
        ('prof_garcia', 'teacher123', 'TEA004', 'Maria', 'Garcia', 'History', '11', 'B'),
    ]
    
    # Create admin user
    admin_data = ('admin', 'adminpass', 'admin')
    
    try:
        # Create students
        for username, password, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals in students:
            # Check if user already exists
            cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            if cursor.fetchone()[0] == 0:
                password_hash = generate_password_hash(password)
                cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                             (username, password_hash, 'student', f'{username}@school.edu'))
                user_id = cursor.lastrowid
                
                cursor.execute('''INSERT INTO students (user_id, student_id, first_name, last_name, 
                                 class_name, section, interests, strengths, career_goals) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, student_id, first_name, last_name, class_name, section, 
                              interests, strengths, career_goals))
                print(f"✓ Created student: {username} ({first_name} {last_name})")
        
        # Create teachers
        for username, password, teacher_id, first_name, last_name, subject, class_name, section in teachers:
            cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            if cursor.fetchone()[0] == 0:
                password_hash = generate_password_hash(password)
                cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                             (username, password_hash, 'teacher', f'{username}@school.edu'))
                user_id = cursor.lastrowid
                
                cursor.execute('''INSERT INTO teachers (user_id, teacher_id, first_name, last_name, 
                                 subject, class_name, section) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, teacher_id, first_name, last_name, subject, class_name, section))
                print(f"✓ Created teacher: {username} ({first_name} {last_name} - {subject})")
        
        # Create admin
        username, password, role = admin_data
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
        if cursor.fetchone()[0] == 0:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                         (username, password_hash, role, f'{username}@school.edu'))
            print(f"✓ Created admin: {username}")
        
        conn.commit()
        print(f"\n✅ Sample users created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_sample_timetable():
    """Create sample timetable data"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("\nCreating sample timetable...")
    
    # Get teacher IDs
    cursor.execute('SELECT id, subject FROM teachers')
    teachers = cursor.fetchall()
    
    if not teachers:
        print("⚠️  No teachers found. Create teachers first.")
        conn.close()
        return
    
    # Sample timetable structure
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = [(1, '09:00', '10:00'), (2, '10:00', '11:00'), (3, '11:30', '12:30'), 
               (4, '12:30', '13:30'), (5, '14:30', '15:30'), (6, '15:30', '16:30')]
    
    classes = [('10', 'A'), ('10', 'B'), ('11', 'A'), ('11', 'B')]
    
    try:
        for class_name, section in classes:
            for day in days:
                for period_num, start_time, end_time in periods:
                    # Randomly assign a teacher and subject
                    teacher_id, subject = random.choice(teachers)
                    
                    cursor.execute('''INSERT OR IGNORE INTO timetable 
                                     (class_name, section, day_of_week, period_number, subject, teacher_id, start_time, end_time)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                                 (class_name, section, day, period_num, subject, teacher_id, start_time, end_time))
        
        conn.commit()
        print("✅ Sample timetable created!")
        
    except Exception as e:
        print(f"❌ Error creating timetable: {e}")
        conn.rollback()
    finally:
        conn.close()

def create_sample_attendance():
    """Create sample attendance data"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    print("\nCreating sample attendance...")
    
    # Get students
    cursor.execute('SELECT id, class_name, section FROM students')
    students = cursor.fetchall()
    
    if not students:
        print("⚠️  No students found. Create students first.")
        conn.close()
        return
    
    try:
        # Create attendance for last 30 days
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            
            for student_id, class_name, section in students:
                # Random attendance status (90% present, 10% absent)
                status = 'present' if random.random() > 0.1 else 'absent'
                
                cursor.execute('''INSERT OR IGNORE INTO attendance 
                                 (student_id, class_name, section, subject, date, status)
                                 VALUES (?, ?, ?, ?, ?, ?)''',
                             (student_id, class_name, section, 'Mathematics', date, status))
        
        conn.commit()
        print("✅ Sample attendance data created!")
        
    except Exception as e:
        print(f"❌ Error creating attendance: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main setup function"""
    print("=" * 50)
    print("School Management System - Sample Data Setup")
    print("=" * 50)
    
    # Initialize database first
    try:
        from app import init_db
        init_db()
        print("✅ Database initialized!")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return
    
    # Create sample data
    create_sample_users()
    create_sample_timetable()
    create_sample_attendance()
    
    print("\n" + "=" * 50)
    print("✅ SETUP COMPLETE!")
    print("=" * 50)
    print("\n📋 TEST CREDENTIALS:")
    print("\n🎓 STUDENTS:")
    print("   • Username: testuser    | Password: testpass")
    print("   • Username: john_doe    | Password: password123")
    print("   • Username: jane_smith  | Password: password123")
    print("   • Username: mike_wilson | Password: password123")
    print("   • Username: sara_jones  | Password: password123")
    
    print("\n👨‍🏫 TEACHERS:")
    print("   • Username: testteacher | Password: teacherpass")
    print("   • Username: prof_brown  | Password: teacher123")
    print("   • Username: prof_davis  | Password: teacher123")
    print("   • Username: prof_miller | Password: teacher123")
    print("   • Username: prof_garcia | Password: teacher123")
    
    print("\n👨‍💼 ADMIN:")
    print("   • Username: admin       | Password: adminpass")
    
    print("\n🚀 Ready to test! Run: python app.py")
    print("   Then visit: http://localhost:5000")

if __name__ == '__main__':
    main()