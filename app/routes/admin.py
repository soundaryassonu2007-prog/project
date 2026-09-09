"""
Admin Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.medical_scan import MedicalScan
from app.models.activity_log import ActivityLog
from app.utils.decorators import require_role

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_users():
    """
    Get all users
    """
    try:
        role = request.args.get('role')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = User.query
        if role:
            query = query.filter_by(role=role)
        
        users = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'total': users.total,
            'pages': users.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/user/<int:user_id>/activate', methods=['PUT'])
@jwt_required()
@require_role('admin')
def activate_user(user_id):
    """
    Activate user account
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = True
        db.session.commit()
        
        return jsonify({
            'message': 'User activated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/user/<int:user_id>/deactivate', methods=['PUT'])
@jwt_required()
@require_role('admin')
def deactivate_user(user_id):
    """
    Deactivate user account
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'User deactivated successfully',
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/statistics', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_statistics():
    """
    Get system statistics
    """
    try:
        total_users = User.query.count()
        total_patients = Patient.query.count()
        total_doctors = Doctor.query.count()
        total_scans = MedicalScan.query.count()
        
        scan_types = db.session.query(
            MedicalScan.scan_type,
            db.func.count(MedicalScan.id)
        ).group_by(MedicalScan.scan_type).all()
        
        return jsonify({
            'statistics': {
                'total_users': total_users,
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'total_scans': total_scans,
                'scan_types': dict(scan_types)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/activity-logs', methods=['GET'])
@jwt_required()
@require_role('admin')
def get_activity_logs():
    """
    Get activity logs
    """
    try:
        action_type = request.args.get('action_type')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = ActivityLog.query.order_by(ActivityLog.created_at.desc())
        if action_type:
            query = query.filter_by(action_type=action_type)
        
        logs = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'total': logs.total,
            'pages': logs.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@require_role('admin')
def dashboard():
    """
    Get admin dashboard data
    """
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        inactive_users = User.query.filter_by(is_active=False).count()
        total_scans = MedicalScan.query.count()
        pending_approvals = MedicalScan.query.filter_by(status='awaiting_review').count()
        
        return jsonify({
            'statistics': {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'total_scans': total_scans,
                'pending_approvals': pending_approvals
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
