"""
Prescription Model
"""
from datetime import datetime
from app import db


class Prescription(db.Model):
    """Prescription model"""
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('doctor_reviews.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    medicine_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)  # e.g., "500mg"
    frequency = db.Column(db.String(100), nullable=False)  # e.g., "twice daily"
    duration = db.Column(db.String(100), nullable=False)  # e.g., "7 days"
    instructions = db.Column(db.Text)  # Special instructions
    warnings = db.Column(db.Text)  # Side effects and warnings
    followup_date = db.Column(db.Date)
    followup_type = db.Column(db.String(100))  # e.g., "Check-up", "Lab test"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'medicine_name': self.medicine_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'duration': self.duration,
            'instructions': self.instructions,
            'followup_date': self.followup_date.isoformat() if self.followup_date else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Prescription {self.medicine_name}>'
