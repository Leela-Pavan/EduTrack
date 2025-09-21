# School Management System

A comprehensive web-based school management system built with Flask, featuring separate dashboards for students, teachers, and administrators.

## Features

- **Student Dashboard**: View attendance, timetable, and personalized tasks
- **Teacher Dashboard**: Manage classes, mark attendance, view student information
- **Admin Dashboard**: System overview, statistics, and administrative controls
- **QR Code Attendance**: Modern attendance marking system
- **User Authentication**: Secure login system with role-based access

## Screenshots

The system includes three main dashboards:
- Student Dashboard: Displays welcome message, attendance summary, and daily schedule
- Teacher Dashboard: Shows today's classes, attendance management, and student data
- Admin Dashboard: Provides system-wide statistics and management tools

## Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- VS Code (recommended)
- Git (optional, for cloning)

### 2. Installation

1. **Download/Clone the project**
   ```bash
   # If you have the ZIP file, extract it
   # Or if using Git:
   git clone <repository-url>
   cd team-nexora-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:5000`
   - The app runs in debug mode by default

## Test Credentials

Use these credentials to test different user roles:

### Student Account
- **Username**: `testuser`
- **Password**: `testpass`
- **Features**: View attendance, timetable, suggested tasks

### Teacher Account  
- **Username**: `testteacher`
- **Password**: `teacherpass`
- **Features**: Manage classes, mark attendance, view student data

### Admin Account
- **Username**: `admin`  
- **Password**: `adminpass`
- **Features**: System statistics, user management, overall control

### Alternative Student Account
- **Username**: `student1`
- **Password**: `password123`

## Testing the Application

The project includes several test scripts to verify functionality:

### Run All Dashboard Tests
```bash
python test_all_dashboards.py
```

### Test Individual Components
```bash
# Test student login and dashboard
python test_login.py

# Test teacher dashboard specifically  
python test_teacher_dashboard.py

# Test admin dashboard
python test_admin_simple.py
```

### Test Template Rendering
```bash
# Test template rendering with proper context
python test_template_context.py
```

## Project Structure

```
team-nexora-main/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── school_system.db      # SQLite database (auto-created)
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── teacher_dashboard.html
│   ├── admin_dashboard.html
│   └── attendance_qr.html
│
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── test_*.py           # Test scripts for verification
```

## Database

- **Type**: SQLite (lightweight, no setup required)
- **File**: `school_system.db` (auto-created on first run)
- **Tables**: users, students, teachers, timetable, attendance, suggested_tasks

The database is automatically initialized when you first run the application.

## Creating New Users

### Through Web Interface
1. Go to `http://localhost:5000`
2. Click "Register" 
3. Fill in the form with appropriate role (student/teacher/admin)
4. Submit and then login

### Through Code
You can also create users programmatically using the provided test scripts as examples.

## Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

3. **Database errors**
   - Delete `school_system.db` and restart the app to recreate

4. **Template errors**
   - Ensure all files in `templates/` folder are present

### Verifying Installation

Run the comprehensive test:
```bash
python test_all_dashboards.py
```

Expected output:
```
=== COMPREHENSIVE DASHBOARD TEST ===

1. TESTING STUDENT DASHBOARD
   ✓ Renders successfully
   ✓ Shows welcome message
   ✓ Shows current date
   ✓ No template errors

2. TESTING TEACHER DASHBOARD
   ✓ Renders successfully
   ✓ Shows welcome message
   ✓ Shows current date
   ✓ No template errors
   ✓ Shows classes section

3. TESTING ADMIN DASHBOARD
   ✓ Shows admin title
   ✓ Shows current date
   ✓ No template errors
```

## Development

### Key Files Modified
- Fixed student name display in `student_dashboard.html`
- Fixed teacher name display in `teacher_dashboard.html`  
- Fixed date formatting in all dashboard templates
- Updated backend to pass properly formatted dates

### Recent Fixes
- ✅ Student dashboard shows correct "First Last" name format
- ✅ Teacher dashboard shows correct "First Last" name format
- ✅ All dashboards display current date properly
- ✅ Removed JavaScript moment.js dependency from templates
- ✅ All template rendering errors resolved

## Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Run the test scripts to identify specific problems
3. Verify all files are present and requirements are installed
4. Check the console output for error messages

## License

This project is for educational purposes.

---

**Happy coding! 🎓**