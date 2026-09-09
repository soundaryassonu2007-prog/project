# AI Radiology Assistant – Disease Predictor

A modern, secure, and production-ready AI-powered healthcare web application for medical scan analysis and disease prediction.

## Overview

The application helps patients upload medical scans (X-ray, CT Scan, MRI, and Ultrasound). Artificial Intelligence analyzes the uploaded images and predicts possible diseases with confidence scores and heatmaps. Predictions are then reviewed by doctors/radiologists who can approve or modify the diagnosis, write prescriptions, and generate professional PDF reports.

## Features

### Core Features
- **Medical Scan Upload**: Support for JPG, JPEG, PNG, and DICOM formats
- **AI Disease Prediction**: CNN-based deep learning model with confidence scores
- **Heatmap Generation**: Grad-CAM visualization overlaid on original images
- **Doctor Review Workflow**: Multi-stage review process with status tracking
- **Prescription Management**: Comprehensive prescription generation
- **PDF Report Generation**: Professional medical reports with QR codes
- **Role-Based Access**: Separate dashboards for Patients, Doctors, and Admins
- **Notification System**: Email and dashboard notifications
- **AI Chatbot**: Common patient questions and medical guidance

### Security Features
- JWT Authentication
- Password Hashing (bcrypt)
- SQL Injection Prevention
- XSS Protection
- CSRF Protection
- Input Validation
- File Validation
- Role-Based Authorization

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap 5

### Backend
- Python Flask
- Flask REST API
- Flask-JWT Authentication
- Flask-Mail (OTP)
- ReportLab (PDF Generation)

### Database
- MySQL
- SQLAlchemy ORM

### AI & ML
- TensorFlow/Keras
- OpenCV
- NumPy
- Scikit-learn
- Pillow
- Grad-CAM for Heatmap Visualization

### Development Tools
- Visual Studio Code
- Git & GitHub

## Project Structure

```
project/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
│
├── app/
│   ├── __init__.py
│   ├── models/                     # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── admin.py
│   │   ├── medical_scan.py
│   │   ├── prediction.py
│   │   ├── heatmap.py
│   │   ├── doctor_review.py
│   │   ├── prescription.py
│   │   ├── report.py
│   │   ├── notification.py
│   │   ├── chat_history.py
│   │   └── activity_log.py
│   │
│   ├── routes/                     # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── admin.py
│   │   ├── scan.py
│   │   ├── prediction.py
│   │   └── chatbot.py
│   │
│   ├── controllers/                # Business logic
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── patient_controller.py
│   │   ├── doctor_controller.py
│   │   ├── admin_controller.py
│   │   ├── scan_controller.py
│   │   ├── prediction_controller.py
│   │   └── chatbot_controller.py
│   │
│   ├── services/                   # Service layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── email_service.py
│   │   ├── image_preprocessing.py
│   │   ├── pdf_generator.py
│   │   └── notification_service.py
│   │
│   ├── ai_model/                   # AI/ML models
│   │   ├── __init__.py
│   │   ├── model_loader.py
│   │   ├── disease_predictor.py
│   │   ├── heatmap_generator.py
│   │   └── models/
│   │       ├── chest_xray_model.h5
│   │       ├── mri_model.h5
│   │       ├── ct_scan_model.h5
│   │       └── ultrasound_model.h5
│   │
│   ├── chatbot/                    # AI Chatbot
│   │   ├── __init__.py
│   │   ├── chatbot.py
│   │   ├── knowledge_base.py
│   │   └── responses.json
│   │
│   ├── utils/                      # Utility functions
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   └── constants.py
│   │
│   ├── static/                     # Static files
│   │   ├── css/
│   │   │   ├── style.css
│   │   │   └── bootstrap-custom.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── auth.js
│   │   │   ├── upload.js
│   │   │   └── charts.js
│   │   ├── images/
│   │   ├── uploads/                # User uploads directory
│   │   ├── heatmaps/               # Generated heatmaps
│   │   └── reports/                # Generated PDF reports
│   │
│   └── templates/                  # HTML templates
│       ├── base.html
│       ├── auth/
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── forgot_password.html
│       │   └── reset_password.html
│       ├── patient/
│       │   ├── dashboard.html
│       │   ├── upload_scan.html
│       │   ├── view_predictions.html
│       │   ├── reports.html
│       │   └── profile.html
│       ├── doctor/
│       │   ├── dashboard.html
│       │   ├── patient_list.html
│       │   ├── review_scan.html
│       │   ├── write_prescription.html
│       │   └── patient_history.html
│       ├── admin/
│       │   ├── dashboard.html
│       │   ├── manage_users.html
│       │   ├── manage_patients.html
│       │   ├── manage_doctors.html
│       │   ├── view_reports.html
│       │   ├── ai_statistics.html
│       │   └── activity_logs.html
│       └── components/
│           ├── navbar.html
│           ├── sidebar.html
│           └── footer.html
│
├── database/
│   ├── schema.sql                  # Database schema
│   └── seed_data.sql               # Initial data
│
└── .gitignore
```

## System Roles

1. **Admin**: Full system control, user management, analytics, and monitoring
2. **Doctor/Radiologist**: Scan review, diagnosis approval, prescription writing, report generation
3. **Patient**: Scan upload, prediction viewing, report download, prescription viewing

## Database Schema

### Core Tables
- `users` - Authentication and basic user information
- `patients` - Patient-specific information
- `doctors` - Doctor-specific information and specializations
- `admins` - Admin user details
- `medical_scans` - Uploaded medical images metadata
- `predictions` - AI model predictions and confidence scores
- `heatmaps` - Grad-CAM heatmap data
- `doctor_reviews` - Doctor's review and approval status
- `prescriptions` - Medicine prescriptions
- `reports` - Generated PDF reports
- `notifications` - System notifications
- `chat_history` - Chatbot conversations
- `activity_logs` - User activity tracking

## Supported Medical Scans

### Chest X-ray
- Pneumonia, Tuberculosis, COVID-19, Lung Opacity, Normal

### MRI
- Brain Tumor, Stroke, Normal

### CT Scan
- Lung Cancer, Kidney Stone, Brain Hemorrhage

### Ultrasound
- Liver Disease, Kidney Disease, Gallstone

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Visual Studio Code
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/soundaryassonu2007-prog/project.git
cd project
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
1. Update `config.py` with your MySQL credentials:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:system@localhost/ai_radiology'
   ```
2. Create the database:
   ```bash
   mysql -u root -psystem -e "CREATE DATABASE ai_radiology;"
   ```
3. Initialize the schema:
   ```bash
   mysql -u root -psystem ai_radiology < database/schema.sql
   ```

### Step 5: Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/forgot-password` - Request password reset OTP
- `POST /api/auth/reset-password` - Reset password with OTP
- `POST /api/auth/change-password` - Change password (authenticated)

### Patient Routes
- `GET /api/patient/dashboard` - Patient dashboard data
- `GET /api/patient/profile` - Get patient profile
- `PUT /api/patient/profile` - Update patient profile
- `POST /api/patient/upload-scan` - Upload medical scan
- `GET /api/patient/scans` - Get upload history
- `GET /api/patient/predictions` - Get predictions for scans
- `GET /api/patient/reports` - Get generated reports
- `GET /api/patient/prescriptions` - Get prescriptions

### Doctor Routes
- `GET /api/doctor/dashboard` - Doctor dashboard data
- `GET /api/doctor/patients` - Get assigned patients
- `GET /api/doctor/pending-reviews` - Get pending scan reviews
- `POST /api/doctor/review-scan/:scanId` - Review and approve/reject scan
- `POST /api/doctor/prescription/:scanId` - Create prescription
- `POST /api/doctor/generate-report/:scanId` - Generate PDF report
- `GET /api/doctor/patient-history/:patientId` - Get patient history

### Admin Routes
- `GET /api/admin/dashboard` - Admin dashboard data
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/user/:userId/status` - Activate/Deactivate user
- `GET /api/admin/statistics` - AI and system statistics
- `GET /api/admin/activity-logs` - User activity logs
- `GET /api/admin/reports` - View all reports

### Scan & Prediction Routes
- `POST /api/scan/upload` - Upload scan
- `GET /api/prediction/:scanId` - Get prediction results
- `GET /api/heatmap/:scanId` - Get heatmap visualization

### Chatbot Routes
- `POST /api/chatbot/ask` - Send message to chatbot
- `GET /api/chatbot/faq` - Get FAQ responses

## Configuration

Edit `config.py` to customize:
- Database connection
- JWT secret key
- Email configuration
- File upload limits
- AI model paths
- Application settings

## Security Considerations

1. **JWT Tokens**: Secure token-based authentication
2. **Password Hashing**: Bcrypt hashing for all passwords
3. **SQL Injection Prevention**: Use SQLAlchemy ORM
4. **XSS Protection**: Template auto-escaping
5. **CSRF Protection**: CSRF tokens on all forms
6. **File Validation**: Type and size validation for uploads
7. **Role Authorization**: Decorator-based access control
8. **HTTPS**: Enable in production
9. **Environment Variables**: Store sensitive data in `.env`
10. **Rate Limiting**: API rate limiting for security

## Features Breakdown

### 1. User Authentication Module
- Registration with email verification
- Secure login with JWT
- Password hashing with bcrypt
- Forgot password with OTP
- Change password functionality
- Role-based access control

### 2. Medical Scan Upload
- Support for JPG, JPEG, PNG, DICOM
- Image validation and preprocessing
- Virus scanning for uploaded files
- Upload progress tracking
- Storage optimization

### 3. AI Disease Prediction
- CNN-based deep learning models
- Real-time prediction
- Confidence score calculation
- Support for multiple scan types
- Batch processing capability

### 4. Doctor Review Workflow
- Multi-stage status tracking
- Prediction approval/rejection
- Diagnosis modification
- Clinical notes recording
- Review history

### 5. Prescription Management
- Medicine name and dosage
- Duration and instructions
- Follow-up date scheduling
- Prescription history

### 6. PDF Report Generation
- Professional medical report format
- Patient and doctor details
- Scan and heatmap inclusion
- QR code generation
- Digital signature support

### 7. Dashboards
- Real-time analytics
- Charts and statistics
- Performance metrics
- User activity tracking
- Export functionality

### 8. Notification System
- Email notifications
- In-app notifications
- Notification history
- Notification preferences

### 9. AI Chatbot
- Disease information
- Scan preparation tips
- Report explanation
- Medication guidance
- FAQ responses

## Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
pylint app/
black app/
```

### Database Migrations
```bash
flask db init
flask db migrate
flask db upgrade
```

## Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS certificates
- [ ] Configure proper database backups
- [ ] Enable rate limiting
- [ ] Set up logging and monitoring
- [ ] Configure email service
- [ ] Optimize database indexes
- [ ] Set up CDN for static files
- [ ] Configure file storage (S3 or similar)
- [ ] Enable security headers

### Docker Deployment
(Dockerfile and docker-compose.yml coming soon)

## Contributing

1. Create a feature branch: `git checkout -b feature/YourFeature`
2. Commit changes: `git commit -am 'Add YourFeature'`
3. Push to branch: `git push origin feature/YourFeature`
4. Submit a pull request

## License

This project is proprietary and confidential.

## Support

For support, contact: support@airadiology.com

---

**Last Updated**: September 9, 2026  
**Version**: 1.0.0  
**Status**: In Development
