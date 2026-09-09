"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db, limiter
from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.admin import Admin
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.utils.validators import validate_email, validate_password
from app.utils.decorators import require_role

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
email_service = EmailService()


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """
    User registration endpoint
    
    JSON Payload:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "role": "patient|doctor|admin",
        "full_name": "string"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role', 'full_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate email format
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        password_valid, message = validate_password(data['password'])
        if not password_valid:
            return jsonify({'error': message}), 400
        
        # Validate role
        if data['role'] not in ['patient', 'doctor', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            role=data['role']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.flush()
        
        # Create role-specific profile
        if data['role'] == 'patient':
            profile = Patient(
                user_id=user.id,
                full_name=data['full_name']
            )
        elif data['role'] == 'doctor':
            profile = Doctor(
                user_id=user.id,
                full_name=data['full_name'],
                specialization=data.get('specialization', '')
            )
        elif data['role'] == 'admin':
            profile = Admin(
                user_id=user.id,
                full_name=data['full_name']
            )
        
        db.session.add(profile)
        db.session.commit()
        
        # Send verification email
        email_service.send_welcome_email(user.email, user.username)
        
        return jsonify({
            'message': 'Registration successful. Please check your email to verify your account.',
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    """
    User login endpoint
    
    JSON Payload:
    {
        "username": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 403
        
        # Update last login
        user.last_login = db.func.now()
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    """
    try:
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout endpoint
    """
    return jsonify({'message': 'Logout successful'}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("3 per hour")
def forgot_password():
    """
    Request password reset OTP
    
    JSON Payload:
    {
        "email": "string"
    }
    """
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal if email exists
            return jsonify({'message': 'If email exists, OTP has been sent'}), 200
        
        # Generate OTP
        otp, expiry = auth_service.generate_otp()
        user.otp = otp
        user.otp_expiry = expiry
        db.session.commit()
        
        # Send OTP via email
        email_service.send_otp_email(user.email, otp)
        
        return jsonify({'message': 'OTP sent to email'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP for password reset
    
    JSON Payload:
    {
        "email": "string",
        "otp": "string"
    }
    """
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return jsonify({'error': 'Email and OTP required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        is_valid, message = auth_service.verify_otp(user.otp, user.otp_expiry, otp)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        return jsonify({'message': 'OTP verified. You can now reset your password'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Reset password with OTP
    
    JSON Payload:
    {
        "email": "string",
        "otp": "string",
        "new_password": "string"
    }
    """
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')
        
        if not all([email, otp, new_password]):
            return jsonify({'error': 'Email, OTP, and new password required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        is_valid, message = auth_service.verify_otp(user.otp, user.otp_expiry, otp)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        password_valid, message = validate_password(new_password)
        if not password_valid:
            return jsonify({'error': message}), 400
        
        user.set_password(new_password)
        user.otp = None
        user.otp_expiry = None
        db.session.commit()
        
        email_service.send_password_reset_confirmation(user.email)
        
        return jsonify({'message': 'Password reset successful'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change password for authenticated user
    
    JSON Payload:
    {
        "old_password": "string",
        "new_password": "string"
    }
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({'error': 'Both passwords required'}), 400
        
        if not user.check_password(old_password):
            return jsonify({'error': 'Incorrect old password'}), 401
        
        password_valid, message = validate_password(new_password)
        if not password_valid:
            return jsonify({'error': message}), 400
        
        if old_password == new_password:
            return jsonify({'error': 'New password must be different'}), 400
        
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
