# EduTrack Configuration File
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'edutrack-secret-key-2024'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///school_system.db'
    
    # Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))  # 16MB
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'images': {'png', 'jpg', 'jpeg', 'gif', 'bmp'},
        'documents': {'pdf', 'doc', 'docx', 'txt', 'rtf'},
        'presentations': {'ppt', 'pptx'},
        'spreadsheets': {'xls', 'xlsx'},
        'archives': {'zip', 'rar', '7z'},
        'code': {'py', 'java', 'cpp', 'c', 'js', 'html', 'css', 'sql'}
    }
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Email Configuration (for verification)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@edutrack.app'
    
    # SMS Configuration (Twilio for verification)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Verification Settings
    VERIFICATION_CODE_LENGTH = 6
    VERIFICATION_CODE_EXPIRY_MINUTES = 10
    MAX_VERIFICATION_ATTEMPTS = 3
    
    # Application Settings
    ITEMS_PER_PAGE = 20
    DEFAULT_TIMEZONE = 'Asia/Kolkata'
    
    # Department Configuration
    DEPARTMENTS = {
        'CSIT': 'Computer Science & Information Technology',
        'CSD': 'Computer Science & Design',
        'ECE': 'Electronics & Communication Engineering',
        'ME': 'Mechanical Engineering',
        'CE': 'Civil Engineering',
        'EEE': 'Electrical & Electronics Engineering'
    }
    
    # Academic Configuration
    ACADEMIC_YEAR = '2024-25'
    SEMESTERS = ['1', '2', '3', '4', '5', '6', '7', '8']
    EXAM_TYPES = ['Mid-1', 'Mid-2', 'Semester']
    
    # Attendance Configuration
    ATTENDANCE_GRACE_PERIOD = 30  # minutes
    MIN_ATTENDANCE_PERCENTAGE = 75
    
    # QR Code Configuration
    QR_CODE_EXPIRY = 300  # 5 minutes in seconds
    QR_CODE_SIZE = 10
    QR_CODE_BORDER = 4
    
    # Security Configuration
    VERIFICATION_CODE_EXPIRY = 600  # 10 minutes in seconds
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 900  # 15 minutes in seconds
    
    # File Upload Paths
    PROFILE_UPLOAD_PATH = os.path.join(UPLOAD_FOLDER, 'profiles')
    PROJECT_UPLOAD_PATH = os.path.join(UPLOAD_FOLDER, 'projects')
    ASSIGNMENT_UPLOAD_PATH = os.path.join(UPLOAD_FOLDER, 'assignments')
    DOCUMENT_UPLOAD_PATH = os.path.join(UPLOAD_FOLDER, 'documents')
    
    # Pagination Configuration
    STUDENTS_PER_PAGE = 25
    TEACHERS_PER_PAGE = 20
    PROJECTS_PER_PAGE = 15
    ASSIGNMENTS_PER_PAGE = 10
    
    # Grade Configuration
    GRADE_SCALE = {
        'A+': {'min': 95, 'max': 100, 'points': 10},
        'A': {'min': 90, 'max': 94, 'points': 9},
        'A-': {'min': 85, 'max': 89, 'points': 8},
        'B+': {'min': 80, 'max': 84, 'points': 7},
        'B': {'min': 75, 'max': 79, 'points': 6},
        'B-': {'min': 70, 'max': 74, 'points': 5},
        'C+': {'min': 65, 'max': 69, 'points': 4},
        'C': {'min': 60, 'max': 64, 'points': 3},
        'D': {'min': 50, 'max': 59, 'points': 2},
        'F': {'min': 0, 'max': 49, 'points': 0}
    }
    
    # Default User Credentials
    DEFAULT_ADMIN = {
        'username': 'admin',
        'password': 'admin123',
        'email': 'admin@edutrack.app',
        'name': 'System Administrator'
    }
    
    DEFAULT_TEACHER = {
        'username': 'teacher1',
        'password': 'teacher123',
        'email': 'teacher@edutrack.app',
        'name': 'Demo Teacher',
        'department': 'CSIT'
    }
    
    DEFAULT_STUDENT = {
        'username': 'student1',
        'password': 'student123',
        'email': 'student@edutrack.app',
        'name': 'Demo Student',
        'department': 'CSIT',
        'semester': '1'
    }

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Override with production values
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Production email settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Utility functions
def get_config():
    """Get configuration based on environment."""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, DevelopmentConfig)

def allowed_file(filename, file_type='all'):
    """Check if uploaded file is allowed."""
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'all':
        all_extensions = set()
        for extensions in Config.ALLOWED_EXTENSIONS.values():
            all_extensions.update(extensions)
        return extension in all_extensions
    
    return extension in Config.ALLOWED_EXTENSIONS.get(file_type, set())

def get_file_type(filename):
    """Determine file type based on extension."""
    if '.' not in filename:
        return 'unknown'
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    for file_type, extensions in Config.ALLOWED_EXTENSIONS.items():
        if extension in extensions:
            return file_type
    
    return 'unknown'

def calculate_grade(marks):
    """Calculate grade based on marks."""
    for grade, criteria in Config.GRADE_SCALE.items():
        if criteria['min'] <= marks <= criteria['max']:
            return grade
    return 'F'

def calculate_gpa(marks_list):
    """Calculate GPA based on list of marks."""
    if not marks_list:
        return 0.0
    
    total_points = 0
    for marks in marks_list:
        grade = calculate_grade(marks)
        total_points += Config.GRADE_SCALE[grade]['points']
    
    return round(total_points / len(marks_list), 2)

# Application constants
APP_NAME = "EduTrack"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Smart Curriculum Activity & Attendance App"
APP_AUTHOR = "Team Nexora"
APP_URL = "https://github.com/Leela-Pavan/EduTrack"
APP_EMAIL = "support@edutrack.app"

# Feature flags
FEATURES = {
    'EMAIL_VERIFICATION': True,
    'MOBILE_VERIFICATION': True,
    'QR_ATTENDANCE': True,
    'FILE_UPLOADS': True,
    'GRADE_CALCULATION': True,
    'ANALYTICS': True,
    'MOBILE_APP': False,  # Future feature
    'VIDEO_LECTURES': False,  # Future feature
    'PARENT_PORTAL': False,  # Future feature
}

# API Configuration (for future mobile app)
API_CONFIG = {
    'VERSION': 'v1',
    'BASE_URL': '/api/v1',
    'RATE_LIMIT': '100/hour',
    'AUTHENTICATION': 'JWT'
}