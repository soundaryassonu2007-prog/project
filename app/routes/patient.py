"""
Patient Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.user import User
from app.models.patient import Patient
from app.models.medical_scan import MedicalScan
from app.utils.decorators import require_role

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/profile', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_profile():
    """
    Get patient profile
    """
    try:
        user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        return jsonify(patient.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/profile', methods=['PUT'])
@jwt_required()
@require_role('patient')
def update_profile():
    """
    Update patient profile
    """
    try:
        user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = [
            'full_name', 'date_of_birth', 'gender', 'phone', 'address',
            'city', 'state', 'postal_code', 'country', 'blood_group',
            'allergies', 'medical_history', 'emergency_contact',
            'emergency_phone', 'insurance_provider', 'insurance_id'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(patient, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'patient': patient.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/scans', methods=['GET'])
@jwt_required()
@require_role('patient')
def get_scans():
    """
    Get patient's medical scans
    """
    try:
        user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        scans = MedicalScan.query.filter_by(patient_id=patient.id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'scans': [scan.to_dict() for scan in scans.items],
            'total': scans.total,
            'pages': scans.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@patient_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_role('patient')
def dashboard():
    """
    Get patient dashboard data
    """
    try:
        user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        # Get statistics
        total_scans = MedicalScan.query.filter_by(patient_id=patient.id).count()
        pending_reviews = MedicalScan.query.filter_by(
            patient_id=patient.id,
            status='awaiting_review'
        ).count()
        completed_reports = MedicalScan.query.filter_by(
            patient_id=patient.id,
            status='completed'
        ).count()
        
        # Get recent scans
        recent_scans = MedicalScan.query.filter_by(patient_id=patient.id).order_by(
            MedicalScan.upload_date.desc()
        ).limit(5).all()
        
        return jsonify({
            'patient': patient.to_dict(),
            'statistics': {
                'total_scans': total_scans,
                'pending_reviews': pending_reviews,
                'completed_reports': completed_reports
            },
            'recent_scans': [scan.to_dict() for scan in recent_scans]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
