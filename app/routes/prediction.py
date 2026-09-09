"""
Prediction Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.medical_scan import MedicalScan
from app.models.prediction import Prediction
from app.models.heatmap import Heatmap

prediction_bp = Blueprint('prediction', __name__)


@prediction_bp.route('/<int:scan_id>', methods=['GET'])
@jwt_required()
def get_prediction(scan_id):
    """
    Get AI prediction for scan
    """
    try:
        scan = MedicalScan.query.get(scan_id)
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        prediction = Prediction.query.filter_by(scan_id=scan_id).first()
        if not prediction:
            return jsonify({'error': 'Prediction not found'}), 404
        
        return jsonify(prediction.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@prediction_bp.route('/<int:scan_id>/heatmap', methods=['GET'])
@jwt_required()
def get_heatmap(scan_id):
    """
    Get heatmap for prediction
    """
    try:
        heatmap = Heatmap.query.filter_by(scan_id=scan_id).first()
        if not heatmap:
            return jsonify({'error': 'Heatmap not found'}), 404
        
        return jsonify(heatmap.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
