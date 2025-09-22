from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
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
    
    conn.commit()
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
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']
        
        # Additional fields based on role
        if role == 'student':
            student_id = request.form['student_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            class_name = request.form['class_name']
            section = request.form.get('section', 'A')  # Default to 'A' if not provided
            mobile_number = request.form.get('mobile_number', '')
            interests = request.form.get('interests', '')
            strengths = request.form.get('strengths', '')
            career_goals = request.form.get('career_goals', '')
        elif role == 'teacher':
            teacher_id = request.form['teacher_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            subject = request.form['subject']
            class_name = request.form['class_name']
            section = request.form.get('section', 'A')  # Default to 'A' if not provided
            mobile_number = request.form.get('mobile_number', '')
        
        conn = sqlite3.connect('school_system.db')
        cursor = conn.cursor()
        
        try:
            # Create user account with mobile number
            password_hash = generate_password_hash(password)
            cursor.execute('''INSERT INTO users (username, password_hash, role, email, mobile_number) 
                             VALUES (?, ?, ?, ?, ?)''',
                         (username, password_hash, role, email, mobile_number))
            user_id = cursor.lastrowid
            
            # Create role-specific profile
            if role == 'student':
                cursor.execute('''INSERT INTO students (user_id, student_id, first_name, last_name, 
                                 class_name, section, mobile_number, interests, strengths, career_goals) 
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, student_id, first_name, last_name, class_name, section, 
                              mobile_number, interests, strengths, career_goals))
            elif role == 'teacher':
                cursor.execute('''INSERT INTO teachers (user_id, teacher_id, first_name, last_name, 
                                 subject, class_name, section) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                             (user_id, teacher_id, first_name, last_name, subject, class_name, section))
            
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError:
            conn.rollback()
            conn.close()
            flash('Username or email already exists', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session['role']
    if role == 'student':
        return redirect(url_for('student_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    elif role == 'admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/student/dashboard')
@login_required
@role_required('student')
def student_dashboard():
    conn = sqlite3.connect('school_system.db')
    cursor = conn.cursor()
    
    # Get student info
    cursor.execute('''SELECT s.*, u.username FROM students s 
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
    cursor.execute('''SELECT t.*, u.username FROM teachers t 
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

if __name__ == '__main__':
    init_db()
    populate_dummy_data()
    app.run(debug=True)



