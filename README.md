# School Management System

A comprehensive full-stack web application designed to revolutionize educational institutions with automated attendance, personalized learning, and intelligent scheduling.

## 🚀 Features

### Core Functionality
- **Automated Attendance System**: QR code scanning, Bluetooth proximity, and face recognition simulation
- **Smart Scheduling**: Personalized daily routines with intelligent free period suggestions
- **Role-based Dashboards**: Separate interfaces for Students, Teachers, and Administrators
- **Real-time Analytics**: Data visualization with Chart.js for attendance and productivity insights
- **Task Management**: Personalized academic and skill development suggestions

### User Roles
- **Students**: Mark attendance, view schedules, receive personalized task suggestions
- **Teachers**: Generate QR codes, monitor attendance, manage classes
- **Administrators**: Access comprehensive reports and analytics

## 🛠️ Technology Stack

### Backend
- **Python Flask**: Web framework
- **SQLite**: Database
- **Werkzeug**: Security utilities
- **QRCode**: QR code generation

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with Bootstrap 5
- **JavaScript**: Interactive functionality
- **Chart.js**: Data visualization
- **Font Awesome**: Icons

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd school-management-system
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 👥 Demo Accounts

The application comes with pre-populated demo accounts:

### Administrator
- **Username**: `admin`
- **Password**: `admin123`

### Students
- **Username**: `student1` | **Password**: `password123`
- **Username**: `student2` | **Password**: `password123`
- **Username**: `student3` | **Password**: `password123`

### Teachers
- **Username**: `teacher1` | **Password**: `password123`
- **Username**: `teacher2` | **Password**: `password123`

## 📱 Usage Guide

### For Students

1. **Login** with student credentials
2. **Mark Attendance**:
   - Click "Mark Attendance" in the navigation
   - Use QR code scanner, Bluetooth proximity, or face recognition
   - Alternative: Manual entry option available
3. **View Schedule**: Check today's timetable and free periods
4. **Task Suggestions**: Review personalized tasks for free periods
5. **Generate Daily Routine**: Get AI-powered daily schedule

### For Teachers

1. **Login** with teacher credentials
2. **Generate QR Codes**:
   - Click on any class in the dashboard
   - Generate QR code for attendance marking
   - Print or display for students
3. **Monitor Attendance**:
   - View real-time attendance for each class
   - Edit attendance records if needed
   - Export attendance data
4. **Analytics**: View attendance charts and reports

### For Administrators

1. **Login** with admin credentials
2. **View Analytics**:
   - Overall attendance statistics
   - Class-wise performance metrics
   - Student engagement insights
3. **Generate Reports**:
   - Comprehensive attendance reports
   - Productivity analytics
   - Export data in various formats
4. **Manage System**: Access user management and system settings

## 🗄️ Database Schema

### Tables
- **users**: User authentication and roles
- **students**: Student profiles and preferences
- **teachers**: Teacher information and subjects
- **timetable**: Class schedules and timings
- **attendance**: Attendance records
- **suggested_tasks**: Personalized task recommendations

### Relationships
- Each student is linked to their class timetable
- Attendance records reference students and classes
- Task suggestions are personalized based on student interests

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///school_system.db
DEBUG=True
```

### Customization
- Modify `static/css/style.css` for custom styling
- Update `templates/` for UI changes
- Extend `app.py` for additional functionality

## 📊 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Attendance
- `POST /attendance/mark` - Mark attendance
- `GET /attendance/qr` - QR code attendance page
- `GET /generate_qr/<class>/<section>/<subject>/<period>` - Generate QR code

### Data
- `GET /api/attendance_stats` - Get attendance statistics
- `GET /student/dashboard` - Student dashboard
- `GET /teacher/dashboard` - Teacher dashboard
- `GET /admin/dashboard` - Admin dashboard

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `DEBUG=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Configure reverse proxy with Nginx
4. Set up SSL certificates
5. Configure database backups

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management
- Role-based access control
- CSRF protection
- Input validation and sanitization

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Efficient SQL queries with proper joins
- Client-side caching for static assets
- Responsive design for mobile devices
- Lazy loading for large datasets

## 🐛 Troubleshooting

### Common Issues

1. **Database not found**
   - Solution: The database is created automatically on first run
   - Check file permissions in the project directory

2. **QR codes not generating**
   - Solution: Ensure Pillow is properly installed
   - Check Python version compatibility

3. **Charts not displaying**
   - Solution: Ensure Chart.js is loaded
   - Check browser console for JavaScript errors

4. **Attendance not saving**
   - Solution: Check database permissions
   - Verify user authentication

### Debug Mode
Enable debug mode by setting `app.run(debug=True)` in `app.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bootstrap for UI components
- Chart.js for data visualization
- Font Awesome for icons
- Flask community for excellent documentation
- Educational institutions for inspiration and requirements

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- Mobile app development
- Advanced AI-powered recommendations
- Integration with school management systems
- Real-time notifications
- Advanced analytics and machine learning
- Multi-language support
- Cloud deployment options

---

**Built with ❤️ for educational institutions worldwide**



