#!/usr/bin/env python3

import sqlite3
from werkzeug.security import generate_password_hash

def create_test_student():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Create a test user for student
    username = "testStudent"
    email = "student@test.com"
    password = "password123"
    role = "student"
    
    # Check if user already exists
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        print(f"Student user '{username}' already exists.")
        conn.close()
        return
    
    # Create user account
    hashed_password = generate_password_hash(password)
    cursor.execute('''INSERT INTO users (username, email, password_hash, role)
                     VALUES (?, ?, ?, ?)''', (username, email, hashed_password, role))
    
    user_id = cursor.lastrowid
    
    # Create student profile
    student_data = (
        user_id,      # user_id
        "STU001",     # student_id
        "Test",       # first_name
        "Student",    # last_name
        "CSIT",       # department
        "A",          # section
        "2",          # year
        None          # profile_picture
    )
    
    cursor.execute('''INSERT INTO students 
                     (user_id, student_id, first_name, last_name, department, section, year, profile_picture)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', student_data)
    
    conn.commit()
    conn.close()
    
    print("Test student account created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Student ID: STU001")

if __name__ == '__main__':
    create_test_student()