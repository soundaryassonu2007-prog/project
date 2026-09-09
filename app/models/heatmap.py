"""
Heatmap Model - Grad-CAM Visualizations
"""
from datetime import datetime
from app import db


class Heatmap(db.Model):
    """Grad-CAM heatmap for model predictions"""
    __tablename__ = 'heatmaps'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('medical_scans.id'), nullable=False, unique=True)
    heatmap_path = db.Column(db.String(255), nullable=False, unique=True)
    original_image_path = db.Column(db.String(255))
    overlay_path = db.Column(db.String(255))  # Original image with heatmap overlay
    intensity_values = db.Column(db.JSON)  # Raw heatmap intensity data
    color_map = db.Column(db.String(50), default='jet')  # Color mapping scheme
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'heatmap_path': self.heatmap_path,
            'overlay_path': self.overlay_path,
            'generated_at': self.generated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Heatmap scan_id={self.scan_id}>'
