#!/usr/bin/env python3
"""
Script to test Flask URL generation.
"""

from app import app

def test_url_generation():
    """Test Flask URL generation for admin dashboard."""
    with app.test_request_context():
        try:
            # Test url_for admin_dashboard
            admin_url = app.url_for('admin_dashboard')
            print(f"✅ admin_dashboard URL: {admin_url}")
            
            # Test other URLs for comparison
            student_url = app.url_for('student_dashboard')
            print(f"✅ student_dashboard URL: {student_url}")
            
            teacher_url = app.url_for('teacher_dashboard')
            print(f"✅ teacher_dashboard URL: {teacher_url}")
            
            dashboard_url = app.url_for('dashboard')
            print(f"✅ dashboard URL: {dashboard_url}")
            
            print("\n🎉 All URL generation successful!")
            
        except Exception as e:
            print(f"❌ Error generating URLs: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_url_generation()