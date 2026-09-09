"""
AI Radiology Assistant - Main Application Entry Point
Production-ready healthcare web application for medical scan analysis
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from config import config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()


def create_app(config_name=None):
    """
    Application factory function
    
    Args:
        config_name: Configuration environment (development, testing, production)
    
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Create upload directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['HEATMAP_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Setup logging
    setup_logging(app)
    
    # Register database models
    with app.app_context():
        from app.models import (
            user, patient, doctor, admin, medical_scan,
            prediction, heatmap, doctor_review, prescription,
            report, notification, chat_history, activity_log
        )
        db.create_all()
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register JWT handlers
    register_jwt_handlers(app)
    
    # CLI commands
    register_cli_commands(app)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'application': app.config['APP_NAME'],
            'version': app.config['APP_VERSION']
        }), 200
    
    # API root
    @app.route('/api', methods=['GET'])
    def api_root():
        return jsonify({
            'message': 'AI Radiology Assistant API',
            'version': app.config['APP_VERSION'],
            'endpoints': {
                'auth': '/api/auth',
                'patient': '/api/patient',
                'doctor': '/api/doctor',
                'admin': '/api/admin',
                'scan': '/api/scan',
                'prediction': '/api/prediction',
                'chatbot': '/api/chatbot',
                'health': '/api/health'
            }
        }), 200
    
    return app


def register_blueprints(app):
    """
    Register all application blueprints
    """
    from app.routes import auth_bp, patient_bp, doctor_bp, admin_bp, scan_bp, prediction_bp, chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(patient_bp, url_prefix='/api/patient')
    app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(scan_bp, url_prefix='/api/scan')
    app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')


def register_error_handlers(app):
    """
    Register global error handlers
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Forbidden', 'message': 'Access denied'}), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not Found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'error': 'Too Many Requests', 'message': 'Rate limit exceeded'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal Server Error', 'message': 'An error occurred'}), 500


def register_jwt_handlers(app):
    """
    Register JWT callback handlers
    """
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from app.models.user import User
        identity = jwt_data["sub"]
        return User.query.get(identity)
    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        from app.models.user import User
        user = User.query.get(identity)
        if user:
            return {'role': user.role}
        return {}
    
    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_data):
        return jsonify({'error': 'Token expired', 'message': 'Please login again'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Invalid token', 'message': str(error)}), 401


def register_cli_commands(app):
    """
    Register CLI commands
    """
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized.')
    
    @app.cli.command()
    def drop_db():
        """Drop all database tables."""
        if input('Are you sure? (y/n) ').lower() == 'y':
            db.drop_all()
            print('Database dropped.')
    
    @app.cli.command()
    def seed_db():
        """Seed database with initial data."""
        from app.models.user import User
        from app.models.admin import Admin
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@airadiology.com',
            role='admin',
            is_active=True
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        admin_profile = Admin(
            user_id=admin_user.id,
            full_name='Administrator'
        )
        db.session.add(admin_profile)
        db.session.commit()
        
        print('Database seeded with admin user.')


def setup_logging(app):
    """
    Configure application logging
    """
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/airadiology.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('AI Radiology Assistant startup')


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
