"""
Medical Scan Model
"""
from datetime import datetime
from app import db


class MedicalScan(db.Model):
    """Medical scan model"""
    __tablename__ = 'medical_scans'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    scan_type = db.Column(db.Enum('xray', 'mri', 'ct_scan', 'ultrasound'), nullable=False)
    scan_category = db.Column(db.String(120), nullable=False)  # e.g., 'Chest', 'Brain'
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    file_size = db.Column(db.Integer)  # in bytes
    file_format = db.Column(db.String(10))  # jpg, png, dcm
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    clinical_notes = db.Column(db.Text)  # Notes from patient
    status = db.Column(
        db.Enum(
            'uploaded',
            'ai_processing',
            'prediction_ready',
            'awaiting_review',
            'approved',
            'rejected',
            'completed'
        ),
        default='uploaded'
    )
    processing_time = db.Column(db.Float)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prediction = db.relationship('Prediction', backref='scan', uselist=False, cascade='all, delete-orphan')
    heatmap = db.relationship('Heatmap', backref='scan', uselist=False, cascade='all, delete-orphan')
    doctor_review = db.relationship('DoctorReview', backref='scan', uselist=False, cascade='all, delete-orphan')
    report = db.relationship('Report', backref='scan', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'scan_type': self.scan_type,
            'scan_category': self.scan_category,
            'file_name': self.file_name,
            'upload_date': self.upload_date.isoformat(),
            'status': self.status,
            'processing_time': self.processing_time
        }
    
    def __repr__(self):
        return f'<MedicalScan {self.file_name}>'
