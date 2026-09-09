-- AI Radiology Assistant Database Schema
-- MySQL Database Structure

CREATE DATABASE IF NOT EXISTS ai_radiology;
USE ai_radiology;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'doctor', 'patient') NOT NULL DEFAULT 'patient',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    otp VARCHAR(6),
    otp_expiry DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login DATETIME,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Patients Table
CREATE TABLE IF NOT EXISTS patients (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other'),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    blood_group VARCHAR(10),
    allergies TEXT,
    medical_history TEXT,
    emergency_contact VARCHAR(120),
    emergency_phone VARCHAR(20),
    profile_photo VARCHAR(255),
    insurance_provider VARCHAR(120),
    insurance_id VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_full_name (full_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Doctors Table
CREATE TABLE IF NOT EXISTS doctors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    specialization VARCHAR(120) NOT NULL,
    license_number VARCHAR(100) UNIQUE,
    registration_number VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    hospital_name VARCHAR(200),
    department VARCHAR(120),
    experience_years INT,
    qualifications TEXT,
    profile_photo VARCHAR(255),
    signature VARCHAR(255),
    is_approved BOOLEAN DEFAULT FALSE,
    approval_date DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_specialization (specialization),
    INDEX idx_is_approved (is_approved)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    position VARCHAR(120),
    department VARCHAR(120),
    permissions JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Medical Scans Table
CREATE TABLE IF NOT EXISTS medical_scans (
    id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    scan_type ENUM('xray', 'mri', 'ct_scan', 'ultrasound') NOT NULL,
    scan_category VARCHAR(120) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(255) NOT NULL UNIQUE,
    file_size INT,
    file_format VARCHAR(10),
    clinical_notes TEXT,
    status ENUM('uploaded', 'ai_processing', 'prediction_ready', 'awaiting_review', 'approved', 'rejected', 'completed') DEFAULT 'uploaded',
    processing_time FLOAT,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    INDEX idx_patient_id (patient_id),
    INDEX idx_status (status),
    INDEX idx_scan_type (scan_type),
    INDEX idx_upload_date (upload_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scan_id INT NOT NULL UNIQUE,
    model_name VARCHAR(120) NOT NULL,
    model_version VARCHAR(50),
    predicted_disease VARCHAR(120) NOT NULL,
    confidence_score FLOAT NOT NULL,
    prediction_probabilities JSON,
    top_5_predictions JSON,
    prediction_time FLOAT,
    raw_output JSON,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES medical_scans(id) ON DELETE CASCADE,
    INDEX idx_scan_id (scan_id),
    INDEX idx_predicted_disease (predicted_disease),
    INDEX idx_confidence_score (confidence_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Heatmaps Table
CREATE TABLE IF NOT EXISTS heatmaps (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scan_id INT NOT NULL UNIQUE,
    heatmap_path VARCHAR(255) NOT NULL UNIQUE,
    original_image_path VARCHAR(255),
    overlay_path VARCHAR(255),
    intensity_values JSON,
    color_map VARCHAR(50) DEFAULT 'jet',
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES medical_scans(id) ON DELETE CASCADE,
    INDEX idx_scan_id (scan_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Doctor Reviews Table
CREATE TABLE IF NOT EXISTS doctor_reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scan_id INT NOT NULL UNIQUE,
    doctor_id INT NOT NULL,
    ai_prediction VARCHAR(120),
    doctor_diagnosis VARCHAR(120),
    clinical_notes TEXT,
    findings TEXT,
    severity_level ENUM('low', 'moderate', 'high', 'critical'),
    approved BOOLEAN DEFAULT FALSE,
    rejected BOOLEAN DEFAULT FALSE,
    rejection_reason TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES medical_scans(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    INDEX idx_scan_id (scan_id),
    INDEX idx_doctor_id (doctor_id),
    INDEX idx_approved (approved)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Prescriptions Table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    review_id INT NOT NULL,
    doctor_id INT NOT NULL,
    medicine_name VARCHAR(200) NOT NULL,
    dosage VARCHAR(100) NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    duration VARCHAR(100) NOT NULL,
    instructions TEXT,
    warnings TEXT,
    followup_date DATE,
    followup_type VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (review_id) REFERENCES doctor_reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
    INDEX idx_review_id (review_id),
    INDEX idx_doctor_id (doctor_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scan_id INT NOT NULL UNIQUE,
    patient_id INT NOT NULL,
    doctor_id INT,
    file_path VARCHAR(255) NOT NULL UNIQUE,
    file_size INT,
    report_status ENUM('draft', 'pending_approval', 'approved', 'rejected', 'finalized', 'archived') DEFAULT 'draft',
    qr_code_data VARCHAR(255),
    digital_signature VARCHAR(255),
    signature_date DATETIME,
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    finalized_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (scan_id) REFERENCES medical_scans(id) ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    INDEX idx_scan_id (scan_id),
    INDEX idx_patient_id (patient_id),
    INDEX idx_report_status (report_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    scan_id INT,
    notification_type ENUM('scan_uploaded', 'prediction_ready', 'doctor_approved', 'doctor_rejected', 'prescription_added', 'report_ready', 'new_message', 'system') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    email_sent BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (scan_id) REFERENCES medical_scans(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_notification_type (notification_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Chat History Table
CREATE TABLE IF NOT EXISTS chat_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    message_type ENUM('faq', 'disease_info', 'scan_prep', 'medication', 'appointment', 'general') DEFAULT 'general',
    sentiment VARCHAR(50),
    user_rating INT,
    feedback TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Activity Logs Table
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    action VARCHAR(200) NOT NULL,
    action_type ENUM('login', 'logout', 'upload', 'download', 'approve', 'reject', 'create_prescription', 'generate_report', 'update_profile', 'delete', 'access', 'system') NOT NULL,
    resource_type VARCHAR(100),
    resource_id INT,
    description TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(255),
    status ENUM('success', 'failed') DEFAULT 'success',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_action_type (action_type),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create Indexes for Performance
CREATE INDEX idx_medical_scans_patient_status ON medical_scans(patient_id, status);
CREATE INDEX idx_predictions_scan ON predictions(scan_id);
CREATE INDEX idx_doctor_reviews_doctor_approved ON doctor_reviews(doctor_id, approved);
CREATE INDEX idx_reports_patient_status ON reports(patient_id, report_status);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);
