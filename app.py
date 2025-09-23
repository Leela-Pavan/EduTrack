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

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Database initialization
def init_db():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('student', 'teacher', 'admin')),
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Students table
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
            career_goals TEXT,
            mobile TEXT,
            profile_picture TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Teachers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            teacher_id TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            mobile TEXT,
            profile_picture TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Timetable table
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
            end_time TEXT NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        )
    ''')
    
    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            class_name TEXT NOT NULL,
            section TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late')),
            marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    # Suggested tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggested_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            task_title TEXT NOT NULL,
            task_description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('high', 'medium', 'low')),
            estimated_duration INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    
    # Admin password storage table (for admin to view user passwords)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_password_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plain_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create default admin account if it doesn't exist
    from werkzeug.security import generate_password_hash
    admin_password_hash = generate_password_hash('ADMIN')
    cursor.execute('''INSERT OR IGNORE INTO users (username, password_hash, role, email, mobile_number) 
                     VALUES (?, ?, ?, ?, ?)''',
                 ('ADMIN', admin_password_hash, 'admin', 'admin@edutrack.com', ''))
    
    conn.commit()
    conn.close()

def migrate_database():
    """Add missing columns to existing tables"""
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    try:
        # Check if mobile column exists in students table
        cursor.execute("PRAGMA table_info(students)")
        students_columns = [column[1] for column in cursor.fetchall()]
        
        if 'mobile' not in students_columns:
            cursor.execute("ALTER TABLE students ADD COLUMN mobile TEXT")
        
        if 'profile_picture' not in students_columns:
            cursor.execute("ALTER TABLE students ADD COLUMN profile_picture TEXT")
        
        # Check if mobile column exists in teachers table
        cursor.execute("PRAGMA table_info(teachers)")
        teachers_columns = [column[1] for column in cursor.fetchall()]
        
        if 'mobile' not in teachers_columns:
            cursor.execute("ALTER TABLE teachers ADD COLUMN mobile TEXT")
        
        if 'profile_picture' not in teachers_columns:
            cursor.execute("ALTER TABLE teachers ADD COLUMN profile_picture TEXT")
        
        # Create admin password store table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_password_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plain_password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")
    finally:
        conn.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Role required decorator
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

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash, role FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            session['role'] = user[2]
            print(f"=== Login Successful ===")
            print(f"User ID: {user[0]}")
            print(f"Username: {username}")
            print(f"Role: {user[2]}")
            print(f"Session after login: {session}")
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            print(f"=== Login Failed ===")
            print(f"Username: {username}")
            print(f"User found: {user}")
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            role = request.form['role']
            
            # Prevent admin registration through the form
            if role == 'admin':
                flash('Admin registration is not allowed. Admin account is pre-configured.', 'error')
                return render_template('register.html')
            
            # Additional fields based on role
            if role == 'student':
                student_id = request.form['student_id']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                department = request.form['department']  # Changed from class_name to department
                section = request.form['section']  # Now required field
                year = request.form['year']  # New field
                mobile_number = request.form.get('mobile_number', '')
                interests = request.form.get('interests', '')
                strengths = request.form.get('strengths', '')
                career_goals = request.form.get('career_goals', '')
            elif role == 'teacher':
                teacher_id = request.form['teacher_id']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                subject = request.form['subject']
                designation = request.form['designation']  # Changed from class_name to designation
                mobile_number = request.form.get('mobile_number', '')
            
            conn = sqlite3.connect('school_system.db')
            cursor = conn.cursor()
            
            # Create user account with mobile number
            password_hash = generate_password_hash(password)
            cursor.execute('''INSERT INTO users (username, password_hash, role, email, mobile_number) 
                             VALUES (?, ?, ?, ?, ?)''',
                         (username, password_hash, role, email, mobile_number))
            user_id = cursor.lastrowid
            
            # Create role-specific profile
            if role == 'student':
                cursor.execute('''INSERT INTO students (user_id, student_id, first_name, last_name, 
                                 class_name, section, mobile, interests, strengths, career_goals) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, student_id, first_name, last_name, f"{department}-{year}", section, 
                              mobile_number, interests, strengths, career_goals))
            elif role == 'teacher':
                cursor.execute('''INSERT INTO teachers (user_id, teacher_id, first_name, last_name, 
                                 subject, class_name, section, mobile) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, teacher_id, first_name, last_name, subject, designation, 'N/A', mobile_number))
            
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError:
            conn.rollback()
            conn.close()
            flash('Username or email already exists', 'error')
        except Exception as e:
            conn.rollback()
            conn.close()
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('register.html')
        except KeyError as e:
            flash(f'Missing required field: {str(e)}', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/simple_register', methods=['GET', 'POST'])
def simple_register():
    if request.method == 'POST':
        # Test with the same logic as register
        return register()
    return render_template('simple_register.html')

@app.route('/test_teacher_registration')
def test_teacher_registration():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Teacher Registration Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 300px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .test-data { background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h2>Teacher Registration Test</h2>
    
    <div class="test-data">
        <h3>Test Data Provided:</h3>
        <p><strong>Username:</strong> Raju</p>
        <p><strong>Email:</strong> raju@gmail.com</p>
        <p><strong>Password:</strong> 2580</p>
        <p><strong>Role:</strong> Teacher</p>
        <p><strong>Subject:</strong> DLCO</p>
        <p><strong>ID:</strong> 101</p>
        <p><strong>Designation:</strong> Asst Prof</p>
        <p><strong>Mobile:</strong> 9885618712</p>
    </div>
    
    <form method="POST" action="/register">
        <div class="form-group">
            <label for="username">Username *</label>
            <input type="text" id="username" name="username" value="Raju" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email *</label>
            <input type="email" id="email" name="email" value="raju@gmail.com" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password *</label>
            <input type="password" id="password" name="password" value="2580" required>
        </div>
        
        <div class="form-group">
            <label for="role">Role *</label>
            <select id="role" name="role" required>
                <option value="teacher" selected>Teacher</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="teacher_id">Teacher ID *</label>
            <input type="text" id="teacher_id" name="teacher_id" value="101" required>
        </div>
        
        <div class="form-group">
            <label for="first_name">First Name *</label>
            <input type="text" id="first_name" name="first_name" value="Raju" required>
        </div>
        
        <div class="form-group">
            <label for="last_name">Last Name</label>
            <input type="text" id="last_name" name="last_name" value="">
        </div>
        
        <div class="form-group">
            <label for="subject">Subject *</label>
            <input type="text" id="subject" name="subject" value="DLCO" required>
        </div>
        
        <div class="form-group">
            <label for="designation">Designation *</label>
            <select id="designation" name="designation" required>
                <option value="Asst Prof" selected>Assistant Professor</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="mobile_number">Mobile Number</label>
            <input type="tel" id="mobile_number" name="mobile_number" value="9885618712">
        </div>
        
        <button type="submit">Register Teacher</button>
    </form>
</body>
</html>
    '''

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session['role']
    print(f"=== Dashboard Route Called ===")
    print(f"User role: {role}")
    print(f"Session: {session}")
    
    if role == 'student':
        print("Redirecting to student_dashboard")
        return redirect(url_for('student_dashboard'))
    elif role == 'teacher':
        print("Redirecting to teacher_dashboard")
        return redirect(url_for('teacher_dashboard'))
    elif role == 'admin':
        print("Redirecting to admin_dashboard")
        return redirect(url_for('admin_dashboard'))
    
    print("No matching role, redirecting to login")
    return redirect(url_for('login'))

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get student info
    cursor.execute('''SELECT s.*, u.username, u.email FROM students s 
                     JOIN users u ON s.user_id = u.id WHERE u.id = ?''', (session['user_id'],))
    student = cursor.fetchone()
    
    # Get today's timetable
    today = datetime.now().strftime('%A')
    cursor.execute('''SELECT * FROM timetable WHERE class_name = ? AND section = ? AND day_of_week = ? 
                     ORDER BY period_number''', (student[4], student[5], today))
    timetable = cursor.fetchall()
    
    # Get free periods
    all_periods = list(range(1, 9))  # Assuming 8 periods
    scheduled_periods = [row[4] for row in timetable]
    free_periods = [p for p in all_periods if p not in scheduled_periods]
    
    # Get suggested tasks
    cursor.execute('''SELECT * FROM suggested_tasks WHERE student_id = ? 
                     ORDER BY priority DESC, created_at DESC''', (student[0],))
    suggested_tasks = cursor.fetchall()
    
    # Get attendance summary
    cursor.execute('''SELECT COUNT(*) as total, 
                     SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                     SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                     FROM attendance WHERE student_id = ? AND date >= date('now', '-30 days')''', 
                   (student[0],))
    attendance_summary = cursor.fetchone()
    
    conn.close()
    
    # Get current date formatted for display
    current_date = datetime.now().strftime('%A, %B %d, %Y')
    
    return render_template('student_dashboard.html', 
                         student=student, 
                         timetable=timetable, 
                         free_periods=free_periods,
                         suggested_tasks=suggested_tasks,
                         attendance_summary=attendance_summary,
                         current_date=current_date)

@app.route('/teacher/dashboard')
@login_required
@role_required('teacher')
def teacher_dashboard():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get teacher info
    cursor.execute('''SELECT t.*, u.username, u.email FROM teachers t 
                     JOIN users u ON t.user_id = u.id WHERE u.id = ?''', (session['user_id'],))
    teacher = cursor.fetchone()
    
    # Get today's classes
    today = datetime.now().strftime('%A')
    cursor.execute('''SELECT * FROM timetable WHERE teacher_id = ? AND day_of_week = ? 
                     ORDER BY period_number''', (teacher[0], today))
    today_classes = cursor.fetchall()
    
    # Get attendance for today's classes
    today_date = datetime.now().strftime('%Y-%m-%d')
    attendance_data = []
    for class_info in today_classes:
        cursor.execute('''SELECT s.first_name, s.last_name, a.status, a.marked_at 
                         FROM attendance a 
                         JOIN students s ON a.student_id = s.id 
                         WHERE a.class_name = ? AND a.section = ? AND a.subject = ? AND a.date = ?
                         ORDER BY s.first_name''', 
                      (class_info[1], class_info[2], class_info[5], today_date))
        class_attendance = cursor.fetchall()
        attendance_data.append({
            'class_info': class_info,
            'attendance': class_attendance
        })
    
    conn.close()
    
    # Get current date formatted for display
    current_date = datetime.now().strftime('%A, %B %d, %Y')
    
    return render_template('teacher_dashboard.html', 
                         teacher=teacher, 
                         today_classes=today_classes,
                         attendance_data=attendance_data,
                         current_date=current_date)

@app.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get overall statistics
    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM teachers')
    total_teachers = cursor.fetchone()[0]
    
    # Get attendance statistics
    cursor.execute('''SELECT COUNT(*) as total_records,
                     SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                     SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                     FROM attendance WHERE date >= date('now', '-30 days')''')
    attendance_stats = cursor.fetchone()
    
    # Get class-wise attendance
    cursor.execute('''SELECT class_name, section, 
                     COUNT(*) as total,
                     SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
                     FROM attendance WHERE date >= date('now', '-7 days')
                     GROUP BY class_name, section
                     ORDER BY class_name, section''')
    class_attendance = cursor.fetchall()
    
    conn.close()
    
    # Get current date formatted for display
    current_date = datetime.now().strftime('%A, %B %d, %Y')
    
    return render_template('admin_dashboard.html',
                         total_students=total_students,
                         total_teachers=total_teachers,
                         attendance_stats=attendance_stats,
                         class_attendance=class_attendance,
                         current_date=current_date)

@app.route('/api/students')
@login_required
def get_all_students():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get all students with their details and passwords
    cursor.execute('''
        SELECT s.student_id, s.first_name, s.last_name, s.class_name, s.section, 
               s.mobile, u.email, u.username, aps.plain_password
        FROM students s
        LEFT JOIN users u ON s.user_id = u.id
        LEFT JOIN admin_password_store aps ON u.id = aps.user_id
        ORDER BY s.class_name, s.section, s.first_name, s.last_name
    ''')
    
    students = cursor.fetchall()
    conn.close()
    
    # Format the data for JSON response
    student_list = []
    for student in students:
        # Apply department mapping
        class_display = student[3]
        if student[3] == '10':
            class_display = 'CSIT'
        elif student[3] == '11':
            class_display = 'CSD'
        elif student[3] == '12':
            class_display = 'CSE'
        
        student_list.append({
            'student_id': student[0],
            'name': f"{student[1]} {student[2]}",
            'department': class_display,
            'section': student[4],
            'year': '2',  # Default year as we don't have this in current schema
            'email': student[6] if student[6] else 'Not provided',
            'mobile': student[5] if student[5] else 'Not provided',
            'password': student[8] if student[8] else student[7] if student[7] else 'Not set'  # Plain password or username
        })
    
    return jsonify(student_list)

@app.route('/api/teachers')
@login_required
def get_all_teachers():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get all teachers with their details and passwords
    cursor.execute('''
        SELECT t.teacher_id, t.first_name, t.last_name, t.subject, 
               t.class_name, t.section, u.email, u.username, aps.plain_password
        FROM teachers t
        LEFT JOIN users u ON t.user_id = u.id
        LEFT JOIN admin_password_store aps ON u.id = aps.user_id
        ORDER BY t.first_name, t.last_name
    ''')
    
    teachers = cursor.fetchall()
    conn.close()
    
    # Format the data for JSON response
    teacher_list = []
    for teacher in teachers:
        # Apply department mapping
        class_display = teacher[4]  # class_name
        if teacher[4] == '10':
            class_display = 'CSIT'
        elif teacher[4] == '11':
            class_display = 'CSD'
        elif teacher[4] == '12':
            class_display = 'CSE'
        
        teacher_list.append({
            'teacher_id': teacher[0],
            'name': f"{teacher[1]} {teacher[2]}",
            'subject': teacher[3] if teacher[3] else 'Not assigned',
            'department': class_display,
            'section': teacher[5] if teacher[5] else 'All',
            'email': teacher[6] if teacher[6] else 'Not provided',
            'password': teacher[8] if teacher[8] else teacher[7] if teacher[7] else 'Not set'  # Plain password or username
        })
    
    return jsonify(teacher_list)

@app.route('/api/add_student', methods=['POST'])
@login_required
def add_student():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # First create user account
        password = 'student123'  # Default password
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, 'student', ?)
        ''', (data['student_id'], generate_password_hash(password), data['email']))
        
        user_id = cursor.lastrowid
        
        # Store plain password for admin reference
        cursor.execute('''
            INSERT INTO admin_password_store (user_id, plain_password)
            VALUES (?, ?)
        ''', (user_id, password))
        
        # Then create student record
        cursor.execute('''
            INSERT INTO students (user_id, student_id, first_name, last_name, class_name, section, mobile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data['student_id'], data['first_name'], data['last_name'], 
              data['department'], data['section'], data['mobile']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Student added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_teacher', methods=['POST'])
@login_required  
def add_teacher():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # First create user account
        password = 'teacher123'  # Default password
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, email)
            VALUES (?, ?, 'teacher', ?)
        ''', (data['teacher_id'], generate_password_hash(password), data['email']))
        
        user_id = cursor.lastrowid
        
        # Store plain password for admin reference
        cursor.execute('''
            INSERT INTO admin_password_store (user_id, plain_password)
            VALUES (?, ?)
        ''', (user_id, password))
        
        # Then create teacher record
        cursor.execute('''
            INSERT INTO teachers (user_id, teacher_id, first_name, last_name, subject, class_name, section, mobile)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data['teacher_id'], data['first_name'], data['last_name'],
              data['subject'], data['department'], data['section'], data['mobile']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Teacher added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_student/<student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Get user_id before deleting student
        cursor.execute('SELECT user_id FROM students WHERE student_id = ?', (student_id,))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            
            # Delete from students table
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            
            # Delete from admin_password_store table
            cursor.execute('DELETE FROM admin_password_store WHERE user_id = ?', (user_id,))
            
            # Delete from users table
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Student deleted successfully'})
        else:
            return jsonify({'error': 'Student not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete_teacher/<teacher_id>', methods=['DELETE'])
@login_required
def delete_teacher(teacher_id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Get user_id before deleting teacher
        cursor.execute('SELECT user_id FROM teachers WHERE teacher_id = ?', (teacher_id,))
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]
            
            # Delete from teachers table
            cursor.execute('DELETE FROM teachers WHERE teacher_id = ?', (teacher_id,))
            
            # Delete from admin_password_store table
            cursor.execute('DELETE FROM admin_password_store WHERE user_id = ?', (user_id,))
            
            # Delete from users table
            cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
            
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Teacher deleted successfully'})
        else:
            return jsonify({'error': 'Teacher not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/attendance/qr')
@login_required
@role_required('student')
def attendance_qr():
    return render_template('attendance_qr.html')

@app.route('/attendance/mark', methods=['POST'])
@login_required
@role_required('student')
def mark_attendance():
    data = request.get_json()
    qr_data = data.get('qr_data', '')
    
    # Parse QR data (format: class_name:section:subject:period)
    try:
        parts = qr_data.split(':')
        if len(parts) != 4:
            return jsonify({'success': False, 'message': 'Invalid QR code format'})
        
        class_name, section, subject, period = parts
        
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Get student info
        cursor.execute('SELECT id, class_name, section FROM students WHERE user_id = ?', (session['user_id'],))
        student = cursor.fetchone()
        
        if not student:
            return jsonify({'success': False, 'message': 'Student not found'})
        
        # Check if already marked
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''SELECT id FROM attendance WHERE student_id = ? AND class_name = ? 
                         AND section = ? AND subject = ? AND date = ?''',
                      (student[0], class_name, section, subject, today))
        
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Attendance already marked for this class'})
        
        # Mark attendance
        cursor.execute('''INSERT INTO attendance (student_id, class_name, section, subject, date, status) 
                         VALUES (?, ?, ?, ?, ?, 'present')''',
                      (student[0], class_name, section, subject, today))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Attendance marked successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/generate_qr/<class_name>/<section>/<subject>/<period>')
@login_required
@role_required('teacher')
def generate_qr(class_name, section, subject, period):
    qr_data = f"{class_name}:{section}:{subject}:{period}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return jsonify({'qr_code': f"data:image/png;base64,{img_str}", 'qr_data': qr_data})

@app.route('/api/attendance_stats')
@login_required
def attendance_stats():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get attendance data for charts
    cursor.execute('''SELECT date, 
                     SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                     SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent
                     FROM attendance WHERE date >= date('now', '-30 days')
                     GROUP BY date ORDER BY date''')
    
    daily_stats = cursor.fetchall()
    
    # Get class-wise attendance
    cursor.execute('''SELECT class_name, section,
                     SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present,
                     COUNT(*) as total
                     FROM attendance WHERE date >= date('now', '-7 days')
                     GROUP BY class_name, section''')
    
    class_stats = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'daily_stats': daily_stats,
        'class_stats': class_stats
    })

def populate_dummy_data():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Create admin user
    admin_password = generate_password_hash('admin123')
    cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                   ('admin', admin_password, 'admin', 'admin@school.com'))
    admin_user_id = cursor.lastrowid
    
    # Create sample students
    students_data = [
        ('student1', 'password123', 'student', 'john@student.com', 'S001', 'John', 'Doe', '10', 'A', 'Mathematics,Science', 'Problem Solving,Analytical Thinking', 'Software Engineer'),
        ('student2', 'password123', 'student', 'jane@student.com', 'S002', 'Jane', 'Smith', '10', 'A', 'Literature,History', 'Creative Writing,Research', 'Journalist'),
        ('student3', 'password123', 'student', 'bob@student.com', 'S003', 'Bob', 'Johnson', '10', 'B', 'Physics,Chemistry', 'Logical Reasoning,Experimentation', 'Scientist'),
        ('student4', 'password123', 'student', 'alice@student.com', 'S004', 'Alice', 'Brown', '11', 'A', 'Art,Design', 'Creativity,Visual Thinking', 'Graphic Designer'),
        ('student5', 'password123', 'student', 'charlie@student.com', 'S005', 'Charlie', 'Wilson', '11', 'B', 'Mathematics,Physics', 'Problem Solving,Mathematical Reasoning', 'Engineer')
    ]
    
    for username, password, role, email, student_id, first_name, last_name, class_name, section, interests, strengths, career_goals in students_data:
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                       (username, password_hash, role, email))
        user_id = cursor.lastrowid
        
        cursor.execute('''INSERT INTO students (user_id, student_id, first_name, last_name, 
                         class_name, section, interests, strengths, career_goals) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (user_id, student_id, first_name, last_name, class_name, section, 
                        interests, strengths, career_goals))
    
    # Create sample teachers
    teachers_data = [
        ('teacher1', 'password123', 'teacher', 'math@teacher.com', 'T001', 'Dr. Sarah', 'Williams', 'Mathematics', '10', 'A'),
        ('teacher2', 'password123', 'teacher', 'science@teacher.com', 'T002', 'Prof. Michael', 'Davis', 'Physics', '10', 'A'),
        ('teacher3', 'password123', 'teacher', 'english@teacher.com', 'T003', 'Ms. Emily', 'Johnson', 'English', '10', 'A'),
        ('teacher4', 'password123', 'teacher', 'chemistry@teacher.com', 'T004', 'Dr. Robert', 'Brown', 'Chemistry', '11', 'A'),
        ('teacher5', 'password123', 'teacher', 'art@teacher.com', 'T005', 'Ms. Lisa', 'Garcia', 'Art', '11', 'A')
    ]
    
    teacher_ids = []
    for username, password, role, email, teacher_id, first_name, last_name, subject, class_name, section in teachers_data:
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                       (username, password_hash, role, email))
        user_id = cursor.lastrowid
        
        cursor.execute('''INSERT INTO teachers (user_id, teacher_id, first_name, last_name, 
                         subject, class_name, section) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (user_id, teacher_id, first_name, last_name, subject, class_name, section))
        teacher_ids.append(cursor.lastrowid)
    
    # Create timetable
    timetable_data = [
        # Class 10A
        ('10', 'A', 'Monday', 1, 'Mathematics', teacher_ids[0], '08:00', '08:45'),
        ('10', 'A', 'Monday', 2, 'Physics', teacher_ids[1], '08:45', '09:30'),
        ('10', 'A', 'Monday', 3, 'English', teacher_ids[2], '09:30', '10:15'),
        ('10', 'A', 'Monday', 4, 'Chemistry', teacher_ids[3], '10:15', '11:00'),
        ('10', 'A', 'Monday', 5, 'Mathematics', teacher_ids[0], '11:15', '12:00'),
        ('10', 'A', 'Monday', 6, 'Physics', teacher_ids[1], '12:00', '12:45'),
        ('10', 'A', 'Monday', 7, 'English', teacher_ids[2], '12:45', '13:30'),
        ('10', 'A', 'Monday', 8, 'Free Period', None, '13:30', '14:15'),
        
        # Class 11A
        ('11', 'A', 'Monday', 1, 'Chemistry', teacher_ids[3], '08:00', '08:45'),
        ('11', 'A', 'Monday', 2, 'Art', teacher_ids[4], '08:45', '09:30'),
        ('11', 'A', 'Monday', 3, 'Mathematics', teacher_ids[0], '09:30', '10:15'),
        ('11', 'A', 'Monday', 4, 'Physics', teacher_ids[1], '10:15', '11:00'),
        ('11', 'A', 'Monday', 5, 'Free Period', None, '11:15', '12:00'),
        ('11', 'A', 'Monday', 6, 'Chemistry', teacher_ids[3], '12:00', '12:45'),
        ('11', 'A', 'Monday', 7, 'Art', teacher_ids[4], '12:45', '13:30'),
        ('11', 'A', 'Monday', 8, 'Mathematics', teacher_ids[0], '13:30', '14:15'),
    ]
    
    for class_name, section, day, period, subject, teacher_id, start_time, end_time in timetable_data:
        cursor.execute('''INSERT INTO timetable (class_name, section, day_of_week, period_number, 
                         subject, teacher_id, start_time, end_time) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (class_name, section, day, period, subject, teacher_id, start_time, end_time))
    
    # Create suggested tasks
    tasks_data = [
        (1, 'Practice Math Problems', 'Solve 10 algebra problems to strengthen your mathematical foundation', 'Academic', 'high', 30),
        (1, 'Learn Python Programming', 'Complete a coding tutorial on basic Python concepts', 'Skill Development', 'medium', 45),
        (2, 'Read Classic Literature', 'Read a chapter from a classic novel to improve vocabulary', 'Academic', 'medium', 30),
        (2, 'Practice Creative Writing', 'Write a short story or poem to enhance creative skills', 'Skill Development', 'high', 40),
        (3, 'Physics Experiment', 'Conduct a simple physics experiment at home', 'Academic', 'high', 60),
        (3, 'Learn Data Analysis', 'Start learning Excel or Google Sheets for data analysis', 'Skill Development', 'medium', 45),
        (4, 'Art Portfolio', 'Create a new artwork for your portfolio', 'Skill Development', 'high', 50),
        (4, 'Design Thinking', 'Learn about design principles and user experience', 'Skill Development', 'medium', 30),
        (5, 'Advanced Math', 'Study calculus or advanced algebra topics', 'Academic', 'high', 60),
        (5, 'Programming Project', 'Start building a small software project', 'Skill Development', 'high', 90)
    ]
    
    for student_id, title, description, category, priority, duration in tasks_data:
        cursor.execute('''INSERT INTO suggested_tasks (student_id, task_title, task_description, 
                         category, priority, estimated_duration) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                       (student_id, title, description, category, priority, duration))
    
    # Create sample attendance records
    from datetime import datetime, timedelta
    today = datetime.now()
    
    for i in range(7):  # Last 7 days
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        for student_id in range(1, 6):  # 5 students
            for class_name, section in [('10', 'A'), ('11', 'A')]:
                cursor.execute('''INSERT INTO attendance (student_id, class_name, section, subject, 
                                 date, status) VALUES (?, ?, ?, ?, ?, ?)''',
                               (student_id, class_name, section, 'Mathematics', date, 'present'))
                cursor.execute('''INSERT INTO attendance (student_id, class_name, section, subject, 
                                 date, status) VALUES (?, ?, ?, ?, ?, ?)''',
                               (student_id, class_name, section, 'Physics', date, 'present'))
    
    conn.commit()
    conn.close()

@app.route('/api/update_student_profile', methods=['POST'])
@login_required
def update_student_profile():
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Update user table
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Update email in users table
        cursor.execute('UPDATE users SET email = ? WHERE id = ?', 
                      (data['email'], user_id))
        
        # Update student table
        cursor.execute('''UPDATE students SET 
                         first_name = ?, last_name = ?, class_name = ?, 
                         section = ?, mobile = ?
                         WHERE user_id = ?''',
                      (data['first_name'], data['last_name'], data['department'], 
                       data['section'], data['mobile'], user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/update_teacher_profile', methods=['POST'])
@login_required
def update_teacher_profile():
    try:
        data = request.get_json()
        user_id = session['user_id']
        
        # Update user table
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Update email in users table
        cursor.execute('UPDATE users SET email = ? WHERE id = ?', 
                      (data['email'], user_id))
        
        # Update teacher table
        cursor.execute('''UPDATE teachers SET 
                         first_name = ?, last_name = ?, subject = ?, 
                         class_name = ?, section = ?, mobile = ?
                         WHERE user_id = ?''',
                      (data['first_name'], data['last_name'], data['subject'],
                       data['department'], data['section'], data['mobile'], user_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    try:
        if 'profile_picture' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['profile_picture']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(app.static_folder, 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # Generate unique filename
            filename = secure_filename(f"{session['user_id']}_{file.filename}")
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            
            # Update database with image path
            conn = sqlite3.connect('school_system.db')
            cursor = conn.cursor()
            
            # Check if user is student or teacher
            role = session.get('role')
            image_url = f"/static/uploads/{filename}"
            
            if role == 'student':
                cursor.execute('UPDATE students SET profile_picture = ? WHERE user_id = ?',
                              (image_url, session['user_id']))
            elif role == 'teacher':
                cursor.execute('UPDATE teachers SET profile_picture = ? WHERE user_id = ?',
                              (image_url, session['user_id']))
            
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'image_url': image_url})
        else:
            return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/debug/add_sample_timetable')
def add_sample_timetable():
    """Debug route to add sample timetable data for testing"""
    try:
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        # Check if teacher with ID 101 exists
        cursor.execute('SELECT teacher_id FROM teachers WHERE teacher_id = ?', (101,))
        teacher = cursor.fetchone()
        
        if not teacher:
            return jsonify({'error': 'Teacher with ID 101 not found. Please register first.'}), 404
        
        # Get current day
        from datetime import datetime
        today = datetime.now().strftime('%A')
        
        # Clear existing timetable for this teacher
        cursor.execute('DELETE FROM timetable WHERE teacher_id = ?', (101,))
        
        # Add sample timetable entries
        timetable_data = [
            (101, '11', 'A', today, 1, 'DLCO', '09:00', '10:00'),
            (101, '11', 'B', today, 3, 'DLCO', '11:00', '12:00'),
            (101, '12', 'A', today, 5, 'DLCO', '14:00', '15:00'),
        ]
        
        cursor.executemany('''INSERT INTO timetable 
                             (teacher_id, class_name, section, day_of_week, period_number, subject, start_time, end_time)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', timetable_data)
        
        # Add some classes for other days too
        other_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        for day in other_days:
            if day != today:
                cursor.execute('''INSERT INTO timetable 
                                 (teacher_id, class_name, section, day_of_week, period_number, subject, start_time, end_time)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                              (101, '11', 'A', day, 2, 'DLCO', '10:00', '11:00'))
        
        conn.commit()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM timetable WHERE teacher_id = ?', (101,))
        count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True, 
            'message': f'Added sample timetable data for teacher 101. Total classes: {count}',
            'today': today
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    migrate_database()
    populate_dummy_data()
    app.run(debug=True)



