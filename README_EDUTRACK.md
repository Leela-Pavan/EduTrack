# EduTrack - Smart Curriculum Activity & Attendance App

## 🎓 Overview

EduTrack is a comprehensive educational management system designed to streamline curriculum activities, attendance tracking, and academic progress monitoring. Built with Flask and modern web technologies, it provides an intuitive interface for students, teachers, and administrators.

## ✨ Features

### 🔐 Enhanced Authentication System
- **Role-based Access Control**: Separate dashboards for Students, Teachers, and Admins
- **Email/Mobile Verification**: 3-code verification system for secure registration
- **Department Management**: Organized by CSIT, CSD, and other departments
- **Secure Login**: Password encryption with session management

### 👨‍🎓 Student Dashboard
- **Scanner Attendance**: Real-time QR code attendance marking
- **Marks Tracking**: View Mid-1, Mid-2, and Semester exam results
- **Project Submissions**: Upload and track project files with status monitoring
- **Assignment Management**: Submit assignments with file uploads and text submissions
- **Profile Management**: Photo upload and personal information management
- **Subject-wise Progress**: Track progress across different subjects

### 👩‍🏫 Teacher Dashboard
- **Subject-specific Attendance**: Manage attendance for assigned subjects
- **Marks Management**: Enter and update student marks for all exam types
- **Assignment Creation**: Create assignments with deadlines and descriptions
- **Project Evaluation**: Review and grade student project submissions
- **Student Progress Tracking**: Monitor individual student performance
- **Class Analytics**: View attendance and performance statistics

### 👨‍💼 Admin Dashboard
- **Comprehensive Data Management**: Full control over students, teachers, and subjects
- **Marks Administration**: Oversee all marks entry and modifications
- **Project & Assignment Oversight**: Monitor all submissions and evaluations
- **Timetable Management**: Create and manage class schedules
- **Department Organization**: Manage department-wise data
- **System Analytics**: Generate reports and view system-wide statistics

### 📱 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Education-themed Interface**: Custom pastel color scheme with smooth animations
- **Interactive Components**: Real-time updates and dynamic content
- **Accessibility**: User-friendly interface with clear navigation

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with comprehensive schema
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.1.3 + Custom CSS
- **Icons**: Font Awesome 6.0
- **File Handling**: Support for multiple file formats
- **Security**: Password hashing, session management, CSRF protection

## 📋 Database Schema

### Core Tables
- **users**: Authentication and role management
- **students**: Student profiles with department information
- **teachers**: Teacher profiles with subject assignments
- **departments**: Department management (CSIT, CSD, etc.)
- **subjects**: Subject information with department mapping

### Academic Tables
- **attendance**: Real-time attendance tracking
- **marks**: Comprehensive marks system (Mid-1, Mid-2, Semester)
- **projects**: Project submissions with file management
- **assignments**: Assignment system with deadlines
- **submissions**: Track all student submissions

### Management Tables
- **timetables**: Class scheduling system
- **verification_codes**: Secure verification system

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Leela-Pavan/EduTrack.git
cd EduTrack
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database
```bash
python app_new.py
```
The database will be automatically created on first run.

### Step 4: Run the Application
```bash
python app_new.py
```

### Step 5: Access the Application
Open your web browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
EduTrack/
├── app.py                      # Original application
├── app_new.py                  # Enhanced EduTrack application
├── requirements.txt            # Python dependencies
├── school_system.db           # SQLite database
├── static/
│   ├── css/
│   │   ├── style.css          # Original styles
│   │   └── edutrack-theme.css # EduTrack custom theme
│   └── js/
│       ├── main.js            # Original JavaScript
│       └── edutrack.js        # EduTrack interactive features
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Original homepage
│   ├── index_new.html         # EduTrack homepage
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── student_dashboard.html # Student interface
│   ├── teacher_dashboard.html # Teacher interface
│   └── admin_dashboard.html   # Admin interface
└── uploads/                   # File upload directory
    ├── projects/              # Project submissions
    ├── assignments/           # Assignment files
    └── profiles/              # Profile pictures
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///school_system.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Email Configuration (Optional)
For email verification features:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 👥 Default Users

### Admin Account
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator

### Sample Teacher
- **Username**: teacher1
- **Password**: teacher123
- **Role**: Teacher

### Sample Student
- **Username**: student1
- **Password**: student123
- **Role**: Student

## 📊 Features in Detail

### Attendance System
- QR code-based attendance marking
- Real-time attendance tracking
- Subject-wise attendance reports
- Automated attendance analytics

### Marks Management
- Three-tier examination system (Mid-1, Mid-2, Semester)
- Subject-wise marks entry
- Progress tracking and analytics
- Grade calculation and reporting

### Project & Assignment System
- File upload support (PDF, DOC, images)
- Deadline management
- Submission status tracking
- Teacher evaluation interface

### Verification System
- Email verification during registration
- Mobile number verification
- 3-code verification challenge
- Secure account activation

## 🔒 Security Features

- **Password Encryption**: Bcrypt hashing for secure password storage
- **Session Management**: Secure session handling with timeout
- **File Upload Security**: Type validation and size limits
- **SQL Injection Prevention**: Parameterized queries
- **CSRF Protection**: Cross-site request forgery prevention

## 📱 Mobile Compatibility

- Responsive design for all screen sizes
- Touch-friendly interface elements
- Mobile-optimized navigation
- Fast loading on mobile networks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Development Team

- **Leela Pavan** - Project Lead & Developer
- **Team Nexora** - Development Team

## 🆘 Support

For support and questions:
- **Email**: support@edutrack.app
- **GitHub Issues**: [Create an Issue](https://github.com/Leela-Pavan/EduTrack/issues)
- **Documentation**: [Wiki](https://github.com/Leela-Pavan/EduTrack/wiki)

## 📈 Roadmap

### Version 2.0 (Upcoming)
- [ ] Mobile App Development
- [ ] Advanced Analytics Dashboard
- [ ] Integration with External LMS
- [ ] Video Lecture Management
- [ ] Parent Portal
- [ ] Fee Management System

### Version 2.1 (Future)
- [ ] AI-powered Attendance Recognition
- [ ] Automated Report Generation
- [ ] Multi-language Support
- [ ] Cloud Storage Integration
- [ ] Advanced Security Features

---

**EduTrack** - Transforming Education Management, One Click at a Time! 🎓✨