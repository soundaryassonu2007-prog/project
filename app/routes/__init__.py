"""
Routes Package
"""
from flask import Blueprint

# Import and create blueprints
auth_bp = Blueprint('auth', __name__)
doctor_bp = Blueprint('doctor', __name__)
patient_bp = Blueprint('patient', __name__)
admin_bp = Blueprint('admin', __name__)
scan_bp = Blueprint('scan', __name__)
prediction_bp = Blueprint('prediction', __name__)
chatbot_bp = Blueprint('chatbot', __name__)

# Import route handlers
from app.routes.auth import auth_bp
from app.routes.doctor import doctor_bp
from app.routes.patient import patient_bp
from app.routes.admin import admin_bp
from app.routes.scan import scan_bp
from app.routes.prediction import prediction_bp
from app.routes.chatbot import chatbot_bp

__all__ = ['auth_bp', 'doctor_bp', 'patient_bp', 'admin_bp', 'scan_bp', 'prediction_bp', 'chatbot_bp']
