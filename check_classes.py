#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('school_system.db')
cursor = conn.cursor()

print("=== Student Classes ===")
cursor.execute('SELECT DISTINCT class_name, section FROM students LIMIT 10')
students = cursor.fetchall()
for s in students:
    print(f"  {s[0]} - {s[1]}")

print("\n=== Attendance Classes ===")
cursor.execute('SELECT DISTINCT class_name, section FROM attendance LIMIT 10')
attendance = cursor.fetchall()
for a in attendance:
    print(f"  {a[0]} - {a[1]}")

conn.close()