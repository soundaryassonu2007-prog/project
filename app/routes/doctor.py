"""
Doctor Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.doctor import Doctor
from app.models.medical_scan import MedicalScan
from app.models.doctor_review import DoctorReview
from app.models.prescription import Prescription
from app.utils.decorators import require_role

doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/profile', methods=['GET'])
@jwt_required()
@require_role('doctor')
def get_profile():
    """
    Get doctor profile
    """
    try:
        user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        return jsonify(doctor.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/pending-reviews', methods=['GET'])
@jwt_required()
@require_role('doctor')
def get_pending_reviews():
    """
    Get pending scans for review
    """
    try:
        user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        scans = MedicalScan.query.filter_by(status='prediction_ready').paginate(
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


@doctor_bp.route('/review-scan/<int:scan_id>', methods=['POST'])
@jwt_required()
@require_role('doctor')
def review_scan(scan_id):
    """
    Review and approve/reject scan
    
    JSON Payload:
    {
        "doctor_diagnosis": "string",
        "clinical_notes": "string",
        "findings": "string",
        "severity_level": "low|moderate|high|critical",
        "approved": boolean
    }
    """
    try:
        user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        scan = MedicalScan.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        data = request.get_json()
        
        # Create or update review
        review = DoctorReview.query.filter_by(scan_id=scan_id).first()
        if not review:
            review = DoctorReview(scan_id=scan_id, doctor_id=doctor.id)
            db.session.add(review)
        
        review.doctor_diagnosis = data.get('doctor_diagnosis')
        review.clinical_notes = data.get('clinical_notes')
        review.findings = data.get('findings')
        review.severity_level = data.get('severity_level')
        review.approved = data.get('approved', False)
        review.rejected = not data.get('approved', False)
        
        if review.approved:
            scan.status = 'approved'
        else:
            scan.status = 'rejected'
            review.rejection_reason = data.get('rejection_reason')
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review submitted successfully',
            'review': review.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_role('doctor')
def dashboard():
    """
    Get doctor dashboard data
    """
    try:
        user_id = get_jwt_identity()
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        
        if not doctor:
            return jsonify({'error': 'Doctor profile not found'}), 404
        
        # Get statistics
        pending_reviews = MedicalScan.query.filter_by(status='prediction_ready').count()
        approved_scans = DoctorReview.query.filter_by(doctor_id=doctor.id, approved=True).count()
        total_reviews = DoctorReview.query.filter_by(doctor_id=doctor.id).count()
        
        return jsonify({
            'doctor': doctor.to_dict(),
            'statistics': {
                'pending_reviews': pending_reviews,
                'approved_scans': approved_scans,
                'total_reviews': total_reviews
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
