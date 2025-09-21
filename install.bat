@echo off
echo Installing School Management System dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing packages...
echo.

REM Install packages
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install Flask==2.3.3
python -m pip install Werkzeug==2.3.7
python -m pip install qrcode==7.4.2
python -m pip install Pillow==10.0.1

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python app.py
echo.
echo Then open your browser to: http://localhost:5000
echo.
pause

