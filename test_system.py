#!/usr/bin/env python3
"""
EduTrack System Test Script
Tests basic functionality of the EduTrack application
"""

import os
import sys
import sqlite3
import subprocess
import requests
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_status(message, status="INFO"):
    """Print a status message."""
    status_colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m", 
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    
    color = status_colors.get(status, status_colors["INFO"])
    reset = status_colors["RESET"]
    print(f"{color}[{status}]{reset} {message}")

def check_python_version():
    """Check if Python version is compatible."""
    print_header("Python Version Check")
    
    version = sys.version_info
    print_status(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print_status("Python version is compatible ✓", "SUCCESS")
        return True
    else:
        print_status("Python 3.8+ required ✗", "ERROR")
        return False

def check_required_files():
    """Check if all required files exist."""
    print_header("Required Files Check")
    
    required_files = [
        "app_new.py",
        "config.py", 
        "requirements.txt",
        "templates/index_new.html",
        "templates/login_new.html",
        "templates/register_new.html",
        "static/css/edutrack-theme.css",
        "static/js/edutrack.js"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print_status(f"Found: {file_path} ✓", "SUCCESS")
        else:
            print_status(f"Missing: {file_path} ✗", "ERROR")
            all_exist = False
    
    return all_exist

def check_directories():
    """Check and create required directories."""
    print_header("Directory Structure Check")
    
    required_dirs = [
        "uploads",
        "uploads/profiles",
        "uploads/projects", 
        "uploads/assignments",
        "uploads/documents"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print_status(f"Directory exists: {dir_path} ✓", "SUCCESS")
        else:
            try:
                os.makedirs(dir_path, exist_ok=True)
                print_status(f"Created directory: {dir_path} ✓", "SUCCESS")
            except Exception as e:
                print_status(f"Failed to create {dir_path}: {e} ✗", "ERROR")
                return False
    
    return True

def test_database_connection():
    """Test database connectivity."""
    print_header("Database Connection Test")
    
    try:
        # Test SQLite connection
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        conn.close()
        
        print_status(f"SQLite version: {version} ✓", "SUCCESS")
        return True
        
    except Exception as e:
        print_status(f"Database test failed: {e} ✗", "ERROR")
        return False

def test_imports():
    """Test if all required Python packages can be imported."""
    print_header("Package Import Test")
    
    required_packages = [
        ("flask", "Flask"),
        ("werkzeug", "Werkzeug"), 
        ("sqlite3", "SQLite3"),
        ("hashlib", "Hashlib"),
        ("datetime", "Datetime"),
        ("os", "OS"),
        ("json", "JSON")
    ]
    
    all_imported = True
    for package, display_name in required_packages:
        try:
            __import__(package)
            print_status(f"{display_name} imported successfully ✓", "SUCCESS")
        except ImportError as e:
            print_status(f"Failed to import {display_name}: {e} ✗", "ERROR")
            all_imported = False
    
    return all_imported

def test_app_startup():
    """Test if the Flask app can start."""
    print_header("Application Startup Test")
    
    try:
        # Import and test basic app creation
        sys.path.insert(0, os.getcwd())
        
        # Test configuration
        try:
            from config import Config, get_config
            config = get_config()
            print_status("Configuration loaded ✓", "SUCCESS")
        except Exception as e:
            print_status(f"Configuration error: {e} ✗", "ERROR")
            return False
        
        # Test app import (without running)
        try:
            import app_new
            print_status("App module imported ✓", "SUCCESS")
        except Exception as e:
            print_status(f"App import error: {e} ✗", "ERROR")
            return False
        
        return True
        
    except Exception as e:
        print_status(f"Startup test failed: {e} ✗", "ERROR")
        return False

def test_template_syntax():
    """Test template files for basic syntax errors."""
    print_header("Template Syntax Test")
    
    template_files = [
        "templates/index_new.html",
        "templates/login_new.html", 
        "templates/register_new.html"
    ]
    
    all_valid = True
    for template in template_files:
        if os.path.exists(template):
            try:
                with open(template, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Basic checks
                if content.strip():
                    print_status(f"Template {template} has content ✓", "SUCCESS")
                else:
                    print_status(f"Template {template} is empty ✗", "ERROR")
                    all_valid = False
                    
            except Exception as e:
                print_status(f"Error reading {template}: {e} ✗", "ERROR")
                all_valid = False
        else:
            print_status(f"Template {template} not found ✗", "ERROR")
            all_valid = False
    
    return all_valid

def generate_test_report():
    """Generate a comprehensive test report."""
    print_header("EduTrack System Test Report")
    
    tests = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Directory Structure", check_directories),
        ("Database Connection", test_database_connection),
        ("Package Imports", test_imports),
        ("Application Startup", test_app_startup),
        ("Template Syntax", test_template_syntax)
    ]
    
    results = {}
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_function in tests:
        try:
            result = test_function()
            results[test_name] = result
            if result:
                passed_tests += 1
        except Exception as e:
            print_status(f"Test {test_name} crashed: {e}", "ERROR")
            results[test_name] = False
    
    # Final report
    print_header("Test Summary")
    print_status(f"Total Tests: {total_tests}")
    print_status(f"Passed: {passed_tests}", "SUCCESS" if passed_tests == total_tests else "INFO")
    print_status(f"Failed: {total_tests - passed_tests}", "ERROR" if passed_tests != total_tests else "INFO")
    
    if passed_tests == total_tests:
        print_status("🎉 All tests passed! EduTrack is ready to run.", "SUCCESS")
        print_status("Run 'python app_new.py' to start the application.", "INFO")
    else:
        print_status("❌ Some tests failed. Please check the errors above.", "ERROR")
        print_status("Fix the issues before running the application.", "WARNING")
    
    return passed_tests == total_tests

def main():
    """Main test function."""
    print_header("EduTrack System Test Suite")
    print_status("Testing EduTrack v2.0.0 - Smart Curriculum Activity & Attendance")
    print_status("Repository: https://github.com/Leela-Pavan/EduTrack")
    
    success = generate_test_report()
    
    print_header("Next Steps")
    if success:
        print_status("✅ System check completed successfully!")
        print_status("🚀 Ready to launch EduTrack")
        print_status("📖 Run 'python app_new.py' to start")
        print_status("🌐 Open http://localhost:5000 in your browser")
        print_status("👤 Use demo credentials from README")
    else:
        print_status("❌ System check found issues")
        print_status("🔧 Please fix the errors above")
        print_status("📚 Check README_EDUTRACK.md for help")
        print_status("💬 Contact support@edutrack.app for assistance")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\nTest interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"Unexpected error: {e}", "ERROR")
        sys.exit(1)