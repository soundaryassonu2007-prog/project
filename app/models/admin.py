"""
Admin Model
"""
from datetime import datetime
from app import db


class Admin(db.Model):
    """Admin model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    position = db.Column(db.String(120))
    department = db.Column(db.String(120))
    permissions = db.Column(db.JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert admin to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'full_name': self.full_name,
            'position': self.position,
            'department': self.department,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Admin {self.full_name}>'
