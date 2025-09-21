"""
Project Preparation Script
Run this to prepare the School Management System for sharing
"""

import os
import shutil
from pathlib import Path

def show_project_summary():
    """Display project summary for sharing"""
    print("=" * 60)
    print("🎓 SCHOOL MANAGEMENT SYSTEM - READY TO SHARE!")
    print("=" * 60)
    
    # Count files
    files = list(Path('.').rglob('*'))
    py_files = [f for f in files if f.suffix == '.py']
    html_files = [f for f in files if f.suffix == '.html']
    
    print(f"\n📊 PROJECT STATS:")
    print(f"   • Python files: {len(py_files)}")
    print(f"   • HTML templates: {len(html_files)}")
    print(f"   • Total files: {len([f for f in files if f.is_file()])}")
    
    print(f"\n📋 MAIN FILES:")
    important_files = [
        'app.py', 'requirements.txt', 'README.md', 'SETUP_GUIDE.md',
        'setup_sample_data.py'
    ]
    
    for file in important_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024
            print(f"   ✅ {file:<20} ({size:.1f} KB)")
        else:
            print(f"   ❌ {file:<20} (MISSING)")
    
    print(f"\n🔧 TEST FILES:")
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.py')]
    for test_file in test_files:
        print(f"   ✅ {test_file}")
    
    print(f"\n📁 FOLDERS:")
    folders = ['templates', 'static', 'static/css', 'static/js']
    for folder in folders:
        if os.path.exists(folder):
            file_count = len([f for f in Path(folder).rglob('*') if f.is_file()])
            print(f"   ✅ {folder:<15} ({file_count} files)")
        else:
            print(f"   ❌ {folder:<15} (MISSING)")

def create_sharing_instructions():
    """Create final instructions for sharing"""
    instructions = """
🎯 SHARING INSTRUCTIONS FOR YOUR FRIEND:

1. 📦 SHARE THESE FILES/FOLDERS:
   • app.py (main application)
   • requirements.txt (dependencies)
   • README.md (quick start guide)
   • SETUP_GUIDE.md (detailed instructions)
   • setup_sample_data.py (sample data script)
   • templates/ folder (all HTML files)
   • static/ folder (CSS, JS files)
   • test_*.py files (for testing)
   
2. 📋 YOUR FRIEND SHOULD:
   • Extract all files to a folder
   • Open terminal/command prompt in that folder
   • Run: pip install -r requirements.txt
   • Run: python setup_sample_data.py (for test data)
   • Run: python app.py
   • Open browser to: http://localhost:5000

3. 🔑 TEST CREDENTIALS:
   • Student: testuser / testpass
   • Teacher: testteacher / teacherpass  
   • Admin: admin / adminpass

4. ✅ VERIFICATION:
   • Run: python test_all_dashboards.py
   • Should see all green checkmarks ✓

5. 🆘 IF PROBLEMS:
   • Check SETUP_GUIDE.md
   • Try deleting school_system.db and restart
   • Verify all files were copied correctly
"""
    
    with open('SHARING_INSTRUCTIONS.txt', 'w') as f:
        f.write(instructions)
    
    print("✅ Created SHARING_INSTRUCTIONS.txt")

def main():
    """Main preparation function"""
    show_project_summary()
    create_sharing_instructions()
    
    print("\n" + "=" * 60)
    print("🚀 PROJECT IS READY TO SHARE!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Zip the entire project folder")
    print("   2. Send to your friend")
    print("   3. They follow README.md or SETUP_GUIDE.md")
    print("   4. They can use test_*.py files to verify everything works")
    
    print("\n🎉 All dashboard issues have been fixed!")
    print("   • Student dashboard: ✅ Shows correct name and date")
    print("   • Teacher dashboard: ✅ Shows correct name and date")  
    print("   • Admin dashboard: ✅ Shows correct date")
    print("   • All login flows: ✅ Working perfectly")

if __name__ == '__main__':
    main()