#!/usr/bin/env python3

import sqlite3

def check_database():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()

    # Check classes table
    print('Classes table:')
    cursor.execute('SELECT * FROM classes')
    classes = cursor.fetchall()
    print(f'Found {len(classes)} classes')
    for c in classes:
        print(c)

    print('\n')

    # Check timetable table  
    print('Timetable table:')
    cursor.execute('SELECT * FROM timetable')
    timetable = cursor.fetchall()
    print(f'Found {len(timetable)} timetable entries')
    for t in timetable:
        print(t)

    print('\n')

    # Check teachers table
    print('Teachers table:')
    cursor.execute('SELECT teacher_id, first_name, last_name, subject FROM teachers')
    teachers = cursor.fetchall()
    print(f'Found {len(teachers)} teachers')
    for t in teachers:
        print(t)

    print('\n')

    # Check users table
    print('Users table:')
    cursor.execute('SELECT id, username, email, role FROM users')
    users = cursor.fetchall()
    print(f'Found {len(users)} users')
    for u in users:
        print(u)

    conn.close()

if __name__ == '__main__':
    check_database()