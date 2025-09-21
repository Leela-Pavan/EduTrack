import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    print("App imported successfully")
    
    # Test with proper request context
    with app.test_request_context():
        from flask import render_template
        
        # Test data that matches what student_dashboard expects
        test_student = (1, 1, 'John', 'Doe', '10', 'A', 'Science', 'Math', 'Engineer')
        test_timetable = []
        test_free_periods = [1, 2, 3]
        test_suggested_tasks = []
        test_attendance_summary = (30, 25, 5)
        test_current_date = "Saturday, September 21, 2025"
        
        try:
            result = render_template('student_dashboard.html', 
                                   student=test_student, 
                                   timetable=test_timetable, 
                                   free_periods=test_free_periods,
                                   suggested_tasks=test_suggested_tasks,
                                   attendance_summary=test_attendance_summary,
                                   current_date=test_current_date)
            print("SUCCESS: Template rendered successfully with request context")
            print(f"Template length: {len(result)} characters")
            
            # Check if template contains expected content
            if 'Welcome, John Doe' in result:
                print("SUCCESS: Template contains welcome message")
            else:
                print("WARNING: Template doesn't contain expected welcome message")
                
        except Exception as e:
            print(f"ERROR: Template rendering failed: {e}")
            import traceback
            traceback.print_exc()

except Exception as e:
    print(f"ERROR: Failed to import app: {e}")
    import traceback
    traceback.print_exc()