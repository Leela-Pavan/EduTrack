#!/usr/bin/env python3
"""
Simplified School Management System - Demo Version
This version runs without external dependencies for demonstration purposes.
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import base64
import hashlib

class SchoolSystemHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_file('templates/index.html')
        elif self.path == '/login':
            self.serve_file('templates/login.html')
        elif self.path == '/register':
            self.serve_file('templates/register.html')
        elif self.path == '/dashboard':
            self.serve_file('templates/student_dashboard.html')
        elif self.path == '/student/dashboard':
            self.serve_file('templates/student_dashboard.html')
        elif self.path == '/teacher/dashboard':
            self.serve_file('templates/teacher_dashboard.html')
        elif self.path == '/admin/dashboard':
            self.serve_file('templates/admin_dashboard.html')
        elif self.path == '/attendance/qr':
            self.serve_file('templates/attendance_qr.html')
        elif self.path.startswith('/static/'):
            self.serve_static_file(self.path[8:])
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == '/login':
            self.handle_login()
        elif self.path == '/register':
            self.handle_register()
        elif self.path == '/attendance/mark':
            self.handle_mark_attendance()
        else:
            self.send_error(404)
    
    def serve_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace template variables
            content = content.replace('{{ moment().format(\'dddd, MMMM Do YYYY\') }}', datetime.now().strftime('%A, %B %d, %Y'))
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404)
    
    def serve_static_file(self, filename):
        try:
            filepath = f'static/{filename}'
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Determine content type
            if filename.endswith('.css'):
                content_type = 'text/css'
            elif filename.endswith('.js'):
                content_type = 'application/javascript'
            elif filename.endswith('.png'):
                content_type = 'image/png'
            elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                content_type = 'image/jpeg'
            else:
                content_type = 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def handle_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))
        
        username = data.get('username', [''])[0]
        password = data.get('password', [''])[0]
        
        # Simple authentication (in real app, use proper hashing)
        if username == 'admin' and password == 'admin123':
            self.send_redirect('/admin/dashboard')
        elif username == 'student1' and password == 'password123':
            self.send_redirect('/student/dashboard')
        elif username == 'teacher1' and password == 'password123':
            self.send_redirect('/teacher/dashboard')
        else:
            self.send_redirect('/login?error=invalid')
    
    def handle_register(self):
        self.send_redirect('/login?message=registered')
    
    def handle_mark_attendance(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'success': True, 'message': 'Attendance marked successfully'})
        self.wfile.write(response.encode('utf-8'))
    
    def send_redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

def init_database():
    """Initialize the SQLite database with sample data"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            student_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            interests TEXT,
            strengths TEXT,
            career_goals TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            teacher_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            day_of_week TEXT NOT NULL,
            period_number INTEGER NOT NULL,
            subject TEXT NOT NULL,
            teacher_id INTEGER,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggested_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            task_title TEXT NOT NULL,
            task_description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            estimated_duration INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample data
    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                   ('admin', 'admin123', 'admin', 'admin@school.com'))
    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                   ('student1', 'password123', 'student', 'student1@school.com'))
    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                   ('teacher1', 'password123', 'teacher', 'teacher1@school.com'))
    
    conn.commit()
    conn.close()

def main():
    print("School Management System - Demo Version")
    print("=====================================")
    print()
    print("Initializing database...")
    init_database()
    print("Database initialized successfully!")
    print()
    print("Starting server...")
    print("Open your browser and go to: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print()
    
    server = HTTPServer(('localhost', 8000), SchoolSystemHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()

if __name__ == '__main__':
    main()



