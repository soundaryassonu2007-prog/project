# Installation & Setup Guide

## AI Radiology Assistant - Complete Setup Instructions

### Prerequisites

- **Python 3.8+** installed
- **MySQL 5.7+** installed and running
- **Visual Studio Code** (recommended)
- **Git** for version control
- **Pip** (Python package manager)

### Step 1: Clone Repository

```bash
git clone https://github.com/soundaryassonu2007-prog/project.git
cd project
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

#### Create Database:

```bash
mysql -u root -psystem -e "CREATE DATABASE ai_radiology;"
```

#### Initialize Schema:

```bash
mysql -u root -psystem ai_radiology < database/schema.sql
```

### Step 5: Configure Environment

Create `.env` file in project root:

```env
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DATABASE_URL=mysql+pymysql://root:system@localhost/ai_radiology

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@airadiology.com
```

### Step 6: Run Application

```bash
python app.py
```

Application will start at: `http://localhost:5000`

### Step 7: Create Initial Admin User

```bash
flask seed-db
```

Default Admin Credentials:
- Username: `admin`
- Password: `admin123`

### Step 8: Configure AI Models

Place your trained models in:
- `app/ai_model/models/chest_xray_model.h5`
- `app/ai_model/models/mri_model.h5`
- `app/ai_model/models/ct_scan_model.h5`
- `app/ai_model/models/ultrasound_model.h5`

If models are not available, the system will display a warning but continue to function.

## Project Structure

```
project/
├── app.py                    # Main application entry
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create manually)
├── app/
│   ├── __init__.py
│   ├── models/               # Database models
│   ├── routes/               # API endpoints
│   ├── services/             # Business logic
│   ├── ai_model/             # AI/ML models
│   ├── utils/                # Utilities & helpers
│   ├── static/               # CSS, JS, images
│   └── templates/            # HTML templates
├── database/
│   └── schema.sql            # Database schema
└── README.md                 # Project documentation
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/forgot-password` - Request OTP
- `POST /api/auth/reset-password` - Reset password

### Patient Endpoints
- `GET /api/patient/profile` - Get profile
- `PUT /api/patient/profile` - Update profile
- `POST /api/scan/upload` - Upload scan
- `GET /api/patient/scans` - Get scans
- `GET /api/prediction/<scan_id>` - Get prediction

### Doctor Endpoints
- `GET /api/doctor/pending-reviews` - Get pending scans
- `POST /api/doctor/review-scan/<scan_id>` - Review scan
- `POST /api/doctor/prescription/<scan_id>` - Create prescription

### Admin Endpoints
- `GET /api/admin/users` - Get all users
- `PUT /api/admin/user/<user_id>/activate` - Activate user
- `GET /api/admin/statistics` - Get statistics

### Chatbot
- `POST /api/chatbot/ask` - Send message
- `GET /api/chatbot/faq` - Get FAQs

## Database Configuration

### MySQL Connection

```python
DATABASE_URL = 'mysql+pymysql://root:system@localhost/ai_radiology'
```

### Create Database Manually

```sql
CREATE DATABASE ai_radiology;
USE ai_radiology;
```

Then run schema.sql to create tables.

## Default User Credentials

### Admin
- Username: `admin`
- Password: `admin123`
- Email: `admin@airadiology.com`

## Troubleshooting

### Issue: MySQL Connection Error

**Solution:**
1. Verify MySQL is running
2. Check database credentials in `.env`
3. Ensure database exists: `CREATE DATABASE ai_radiology;`

### Issue: Module Import Error

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Static Files Not Loading

**Solution:**
Ensure `static/` directory exists with proper structure.

### Issue: Email Not Sending

**Solution:**
1. Enable "Less secure app access" in Gmail
2. Generate App Password for Gmail account
3. Update `MAIL_USERNAME` and `MAIL_PASSWORD` in `.env`

## Running Tests

```bash
pytest tests/
```

## Development

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
pylint app/
```

### Database Migrations

```bash
# Create migration
flask db migrate

# Apply migration
flask db upgrade
```

## Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## Security Best Practices

1. **Change SECRET_KEY and JWT_SECRET_KEY** in production
2. **Enable HTTPS** in production
3. **Set FLASK_ENV=production**
4. **Use strong database password**
5. **Implement rate limiting** for API endpoints
6. **Regular database backups**
7. **Monitor activity logs** regularly

## Performance Optimization

1. **Enable caching** for frequent queries
2. **Optimize database indexes**
3. **Use CDN for static files**
4. **Implement pagination** for large datasets
5. **Enable gzip compression**

## Support & Documentation

For more information, refer to:
- README.md - Project overview
- API documentation - In code comments
- Database schema - database/schema.sql

## License

This project is proprietary and confidential.

## Contact

For support, contact: support@airadiology.com
