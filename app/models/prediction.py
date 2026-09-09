"""
Prediction Model - AI Model Predictions
"""
from datetime import datetime
from app import db


class Prediction(db.Model):
    """AI prediction results"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('medical_scans.id'), nullable=False, unique=True)
    model_name = db.Column(db.String(120), nullable=False)
    model_version = db.Column(db.String(50))
    predicted_disease = db.Column(db.String(120), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)  # 0-1
    prediction_probabilities = db.Column(db.JSON)  # {disease: probability}
    prediction_time = db.Column(db.Float)  # in seconds
    top_5_predictions = db.Column(db.JSON)  # Top 5 diseases
    raw_output = db.Column(db.JSON)  # Raw model output
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'predicted_disease': self.predicted_disease,
            'confidence_score': float(self.confidence_score),
            'top_5_predictions': self.top_5_predictions,
            'prediction_time': self.prediction_time,
            'is_approved': self.is_approved,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Prediction {self.predicted_disease}>'
