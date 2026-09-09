"""
Activity Log Model
"""
from datetime import datetime
from app import db


class ActivityLog(db.Model):
    """User activity logging"""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    action_type = db.Column(
        db.Enum(
            'login',
            'logout',
            'upload',
            'download',
            'approve',
            'reject',
            'create_prescription',
            'generate_report',
            'update_profile',
            'delete',
            'access',
            'system'
        ),
        nullable=False
    )
    resource_type = db.Column(db.String(100))  # e.g., 'scan', 'report', 'user'
    resource_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))  # IPv4 or IPv6
    user_agent = db.Column(db.String(255))
    status = db.Column(db.Enum('success', 'failed'), default='success')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'action_type': self.action_type,
            'resource_type': self.resource_type,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ActivityLog {self.action_type}>'
