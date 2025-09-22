@echo off
echo ==========================================
echo    EduTrack - Smart Education Platform
echo        Deployment & Setup Script
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python version: %PYTHON_VERSION%

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

:: Install requirements
echo [INFO] Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)
echo [SUCCESS] All packages installed successfully

:: Create necessary directories
echo [INFO] Creating application directories...
if not exist "uploads" mkdir uploads
if not exist "uploads\profiles" mkdir uploads\profiles
if not exist "uploads\projects" mkdir uploads\projects
if not exist "uploads\assignments" mkdir uploads\assignments
if not exist "uploads\documents" mkdir uploads\documents
echo [SUCCESS] Directory structure created

:: Create .env file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating environment configuration file...
    (
        echo SECRET_KEY=edutrack-secret-key-2024-production
        echo FLASK_ENV=development
        echo DATABASE_URL=sqlite:///school_system.db
        echo UPLOAD_FOLDER=uploads
        echo MAX_CONTENT_LENGTH=16777216
        echo.
        echo # Email Configuration ^(Optional^)
        echo # MAIL_SERVER=smtp.gmail.com
        echo # MAIL_PORT=587
        echo # MAIL_USE_TLS=True
        echo # MAIL_USERNAME=your-email@gmail.com
        echo # MAIL_PASSWORD=your-app-password
        echo # MAIL_DEFAULT_SENDER=noreply@edutrack.app
    ) > .env
    echo [SUCCESS] Environment file created
) else (
    echo [INFO] Environment file already exists
)

:: Check if database exists and initialize if needed
python -c "import sqlite3; import os; print('[INFO] Database exists' if os.path.exists('school_system.db') else '[INFO] Database will be created on first run')"

:: Display completion message
echo.
echo ==========================================
echo         SETUP COMPLETED SUCCESSFULLY!
echo ==========================================
echo.
echo What's next:
echo.
echo 1. To start the application:
echo    - Run: start_edutrack.bat
echo    - Or manually: python app_new.py
echo.
echo 2. Access the application:
echo    - Open your browser
echo    - Go to: http://localhost:5000
echo.
echo 3. Default login credentials:
echo.
echo    Admin:
echo      Username: admin
echo      Password: admin123
echo.
echo    Teacher:
echo      Username: teacher1  
echo      Password: teacher123
echo.
echo    Student:
echo      Username: student1
echo      Password: student123
echo.
echo 4. Features available:
echo    - Role-based dashboards
echo    - Attendance tracking
echo    - Marks management
echo    - Project submissions
echo    - Assignment system
echo    - File uploads
echo    - Verification system
echo.
echo 5. For production deployment:
echo    - Update .env file with production values
echo    - Set FLASK_ENV=production
echo    - Configure email settings
echo    - Use a production WSGI server
echo.
echo ==========================================
echo        Visit: https://github.com/Leela-Pavan/EduTrack
echo        Support: support@edutrack.app
echo ==========================================
echo.

:: Ask if user wants to start the application
set /p START_APP=Do you want to start EduTrack now? (y/n): 
if /i "%START_APP%"=="y" (
    echo.
    echo [INFO] Starting EduTrack...
    echo [INFO] Press Ctrl+C to stop the server
    echo [INFO] Open http://localhost:5000 in your browser
    echo.
    python app_new.py
) else (
    echo.
    echo [INFO] Setup complete. Run 'start_edutrack.bat' to start the application.
)

pause