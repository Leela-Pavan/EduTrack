from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import json
from datetime import datetime, timedelta
import qrcode
import io
import base64
from functools import wraps
import random
import string

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'projects'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'assignments'), exist_ok=True)

# Database initialization with new schema
def init_db():
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    
    # Users table - enhanced with verification
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin')),
            email TEXT UNIQUE NOT NULL,
            mobile TEXT,
            profile_photo TEXT,
            email_verified INTEGER DEFAULT 0,
            mobile_verified INTEGER DEFAULT 0,
            verification_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Students table - enhanced for new requirements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            registration_number TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            department_id INTEGER,
            year INTEGER NOT NULL CHECK(year IN (1, 2, 3, 4)),
            section TEXT NOT NULL,
            overall_attendance_percentage REAL DEFAULT 0.0,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    
    # Teachers table - enhanced with designation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            teacher_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            department_id INTEGER,
            designation TEXT NOT NULL CHECK(designation IN ('HOD', 'Professor', 'Asst Professor', 'Lab Assistant')),
            subjects TEXT, -- JSON array of subjects they teach
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    
    # Subjects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department_id INTEGER,
            year INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            credits INTEGER DEFAULT 3,
            teacher_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments (id),
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    
    # Enhanced attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            date TEXT NOT NULL,
            period_number INTEGER,
            status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late')),
            marked_by INTEGER, -- teacher who marked
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attendance_method TEXT DEFAULT 'manual' CHECK(attendance_method IN ('manual', 'scanner')),
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (subject_id) REFERENCES subjects (id),
            FOREIGN KEY (marked_by) REFERENCES teachers (id)
        )
    ''')
    
    # Marks table - for mid-1, mid-2, semester
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            exam_type TEXT NOT NULL CHECK(exam_type IN ('mid1', 'mid2', 'semester', 'assignment')),
            marks_obtained INTEGER,
            total_marks INTEGER,
            grade TEXT,
            teacher_id INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (subject_id) REFERENCES subjects (id),
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    
    # Projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            subject_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            file_path TEXT,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted' CHECK(status IN ('submitted', 'reviewed', 'approved', 'rejected')),
            teacher_feedback TEXT,
            marks INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        )
    ''')
    
    # Assignments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATE,
            total_marks INTEGER DEFAULT 100,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects (id),
            FOREIGN KEY (created_by) REFERENCES teachers (id)
        )
    ''')
    
    # Assignment submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignment_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER,
            student_id INTEGER,
            file_path TEXT,
            submission_text TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'submitted' CHECK(status IN ('submitted', 'late', 'reviewed', 'graded')),
            marks_obtained INTEGER,
            teacher_feedback TEXT,
            FOREIGN KEY (assignment_id) REFERENCES assignments (id),
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    # Timetables table - enhanced
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department_id INTEGER,
            year INTEGER,
            section TEXT,
            day_of_week TEXT NOT NULL,
            period_number INTEGER NOT NULL,
            subject_id INTEGER,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            FOREIGN KEY (department_id) REFERENCES departments (id),
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize default departments
def init_default_data():
    conn = sqlite3.connect('edutrack.db')
    cursor = conn.cursor()
    
    # Add default departments
    departments = [
        ('CSIT', 'Computer Science & Information Technology'),
        ('CSD', 'Computer Science & Design'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering')
    ]
    
    for code, name in departments:
        cursor.execute('INSERT OR IGNORE INTO departments (code, name) VALUES (?, ?)', (code, name))
    
    # Create default admin user
    admin_password = generate_password_hash('Admin')
    cursor.execute('''INSERT OR IGNORE INTO users 
                     (username, password_hash, role, email, email_verified, mobile_verified) 
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                   ('Admin', admin_password, 'admin', 'admin@edutrack.com', 1, 1))
    
    conn.commit()
    conn.close()

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != required_role:
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def verification_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') in ['student', 'teacher']:
            conn = sqlite3.connect('edutrack.db')
            cursor = conn.cursor()
            cursor.execute('SELECT email_verified, mobile_verified FROM users WHERE id = ?', (session['user_id'],))
            verification = cursor.fetchone()
            conn.close()
            
            if not verification or not (verification[0] and verification[1]):
                flash('Please verify your email and mobile number to continue.', 'warning')
                return redirect(url_for('verify_account'))
        return f(*args, **kwargs)
    return decorated_function

# Generate verification code
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    init_default_data()
    app.run(debug=True)