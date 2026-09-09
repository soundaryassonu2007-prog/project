"""
Patient Model
"""
from datetime import datetime
from app import db


class Patient(db.Model):
    """Patient model"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum('male', 'female', 'other'))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    blood_group = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    emergency_contact = db.Column(db.String(120))
    emergency_phone = db.Column(db.String(20))
    profile_photo = db.Column(db.String(255))
    insurance_provider = db.Column(db.String(120))
    insurance_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medical_scans = db.relationship('MedicalScan', backref='patient', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert patient to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'blood_group': self.blood_group,
            'allergies': self.allergies,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Patient {self.full_name}>'
