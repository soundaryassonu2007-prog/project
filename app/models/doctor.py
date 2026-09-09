"""
Doctor Model
"""
from datetime import datetime
from app import db


class Doctor(db.Model):
    """Doctor model"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    specialization = db.Column(db.String(120), nullable=False)
    license_number = db.Column(db.String(100), unique=True)
    registration_number = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))
    hospital_name = db.Column(db.String(200))
    department = db.Column(db.String(120))
    experience_years = db.Column(db.Integer)
    qualifications = db.Column(db.Text)
    profile_photo = db.Column(db.String(255))
    signature = db.Column(db.String(255))
    is_approved = db.Column(db.Boolean, default=False)
    approval_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('DoctorReview', backref='doctor', cascade='all, delete-orphan')
    prescriptions = db.relationship('Prescription', backref='doctor', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert doctor to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'hospital_name': self.hospital_name,
            'department': self.department,
            'experience_years': self.experience_years,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Doctor {self.full_name}>'
