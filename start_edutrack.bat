@echo off
echo ==========================================
echo       Starting EduTrack Platform
echo ==========================================
echo.

:: Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_edutrack.bat first
    pause
    exit /b 1
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if required files exist
if not exist "app_new.py" (
    echo [ERROR] Application file not found!
    echo Please ensure you're in the correct directory
    pause
    exit /b 1
)

:: Display startup information
echo.
echo [INFO] EduTrack is starting...
echo [INFO] Platform: Smart Curriculum Activity ^& Attendance
echo [INFO] Version: 2.0.0
echo [INFO] Environment: Development
echo.
echo ==========================================
echo         APPLICATION INFORMATION
echo ==========================================
echo.
echo URL: http://localhost:5000
echo.
echo Default Login Credentials:
echo.
echo Admin Dashboard:
echo   Username: admin
echo   Password: admin123
echo.
echo Teacher Dashboard:  
echo   Username: teacher1
echo   Password: teacher123
echo.
echo Student Dashboard:
echo   Username: student1
echo   Password: student123
echo.
echo ==========================================
echo.
echo [INFO] Press Ctrl+C to stop the server
echo [INFO] Open http://localhost:5000 in your browser
echo.

:: Start the application
python app_new.py