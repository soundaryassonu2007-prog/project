"""
Application constants
"""

# Scan types
SCAN_TYPES = {
    'xray': 'X-Ray',
    'mri': 'MRI',
    'ct_scan': 'CT Scan',
    'ultrasound': 'Ultrasound'
}

# Scan categories
SCAN_CATEGORIES = {
    'xray': ['Chest', 'Hand', 'Spine', 'Pelvis'],
    'mri': ['Brain', 'Spine', 'Knee', 'Shoulder'],
    'ct_scan': ['Brain', 'Chest', 'Abdomen', 'Spine'],
    'ultrasound': ['Abdomen', 'Heart', 'Pregnancy', 'Thyroid']
}

# Disease categories
DISEASES = {
    'xray': ['Pneumonia', 'Tuberculosis', 'COVID-19', 'Lung Opacity', 'Normal'],
    'mri': ['Brain Tumor', 'Stroke', 'Normal'],
    'ct_scan': ['Lung Cancer', 'Kidney Stone', 'Brain Hemorrhage'],
    'ultrasound': ['Liver Disease', 'Kidney Disease', 'Gallstone']
}

# Report statuses
REPORT_STATUSES = {
    'draft': 'Draft',
    'pending_approval': 'Pending Approval',
    'approved': 'Approved',
    'rejected': 'Rejected',
    'finalized': 'Finalized',
    'archived': 'Archived'
}

# Scan processing statuses
SCAN_STATUSES = {
    'uploaded': 'Uploaded',
    'ai_processing': 'AI Processing',
    'prediction_ready': 'Prediction Ready',
    'awaiting_review': 'Awaiting Review',
    'approved': 'Approved',
    'rejected': 'Rejected',
    'completed': 'Completed'
}

# User roles
USER_ROLES = ['admin', 'doctor', 'patient']

# Severity levels
SEVERITY_LEVELS = ['low', 'moderate', 'high', 'critical']

# Notification types
NOTIFICATION_TYPES = [
    'scan_uploaded',
    'prediction_ready',
    'doctor_approved',
    'doctor_rejected',
    'prescription_added',
    'report_ready',
    'new_message',
    'system'
]

# File extensions allowed
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'dcm'}

# Maximum file size in MB
MAX_FILE_SIZE_MB = 50

# Model confidence threshold
MODEL_CONFIDENCE_THRESHOLD = 0.5

# OTP settings
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 10
