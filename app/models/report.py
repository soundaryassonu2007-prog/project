"""
Report Model - PDF Reports
"""
from datetime import datetime
from app import db


class Report(db.Model):
    """Generated PDF report"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('medical_scans.id'), nullable=False, unique=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    file_size = db.Column(db.Integer)  # in bytes
    report_status = db.Column(
        db.Enum(
            'draft',
            'pending_approval',
            'approved',
            'rejected',
            'finalized',
            'archived'
        ),
        default='draft'
    )
    qr_code_data = db.Column(db.String(255))  # QR code content
    digital_signature = db.Column(db.String(255))
    signature_date = db.Column(db.DateTime)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    finalized_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'patient_id': self.patient_id,
            'report_status': self.report_status,
            'generated_at': self.generated_at.isoformat(),
            'finalized_at': self.finalized_at.isoformat() if self.finalized_at else None
        }
    
    def __repr__(self):
        return f'<Report scan_id={self.scan_id}>'
