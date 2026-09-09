"""
Medical Scan Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from app import db, limiter
from app.models.patient import Patient
from app.models.medical_scan import MedicalScan
from app.utils.decorators import require_role
from app.services.image_preprocessing import ImagePreprocessor

scan_bp = Blueprint('scan', __name__)
preprocessor = ImagePreprocessor()

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'dcm'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@scan_bp.route('/upload', methods=['POST'])
@jwt_required()
@require_role('patient')
@limiter.limit("5 per hour")  # Limit uploads
def upload_scan():
    """
    Upload medical scan
    
    Form Data:
    {
        "file": binary file,
        "scan_type": "xray|mri|ct_scan|ultrasound",
        "scan_category": "string",
        "clinical_notes": "string (optional)"
    }
    """
    try:
        user_id = get_jwt_identity()
        patient = Patient.query.filter_by(user_id=user_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient profile not found'}), 404
        
        # Check file
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use jpg, jpeg, png, or dcm'}), 400
        
        # Get scan details
        scan_type = request.form.get('scan_type')
        scan_category = request.form.get('scan_category')
        clinical_notes = request.form.get('clinical_notes', '')
        
        if not scan_type or not scan_category:
            return jsonify({'error': 'Scan type and category required'}), 400
        
        if scan_type not in ['xray', 'mri', 'ct_scan', 'ultrasound']:
            return jsonify({'error': 'Invalid scan type'}), 400
        
        # Save file
        from flask import current_app
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Create scan record
        scan = MedicalScan(
            patient_id=patient.id,
            scan_type=scan_type,
            scan_category=scan_category,
            file_name=filename,
            file_path=filepath,
            file_size=os.path.getsize(filepath),
            file_format=filename.rsplit('.', 1)[1].lower(),
            clinical_notes=clinical_notes,
            status='uploaded'
        )
        db.session.add(scan)
        db.session.commit()
        
        return jsonify({
            'message': 'Scan uploaded successfully',
            'scan': scan.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@scan_bp.route('/<int:scan_id>', methods=['GET'])
@jwt_required()
def get_scan(scan_id):
    """
    Get scan details
    """
    try:
        scan = MedicalScan.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        return jsonify(scan.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
