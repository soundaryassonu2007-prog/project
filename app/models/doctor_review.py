"""
Doctor Review Model
"""
from datetime import datetime
from app import db


class DoctorReview(db.Model):
    """Doctor review of AI predictions"""
    __tablename__ = 'doctor_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('medical_scans.id'), nullable=False, unique=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    ai_prediction = db.Column(db.String(120))  # Original AI prediction
    doctor_diagnosis = db.Column(db.String(120))  # Doctor's diagnosis
    clinical_notes = db.Column(db.Text)
    findings = db.Column(db.Text)  # Detailed findings
    severity_level = db.Column(db.Enum('low', 'moderate', 'high', 'critical'))
    approved = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    rejection_reason = db.Column(db.Text)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prescriptions = db.relationship('Prescription', backref='review', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'doctor_id': self.doctor_id,
            'doctor_diagnosis': self.doctor_diagnosis,
            'approved': self.approved,
            'severity_level': self.severity_level,
            'review_date': self.review_date.isoformat()
        }
    
    def __repr__(self):
        return f'<DoctorReview scan_id={self.scan_id}>'
