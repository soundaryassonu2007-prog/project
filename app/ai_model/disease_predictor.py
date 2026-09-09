"""
Disease Predictor - Main AI prediction model
"""
import numpy as np
from flask import current_app
import tensorflow as tf
from tensorflow import keras
import os
import json
from datetime import datetime
from app import db
from app.models.prediction import Prediction
from app.models.medical_scan import MedicalScan


class DiseasePredictor:
    """CNN-based disease prediction model"""
    
    def __init__(self):
        """
        Initialize disease predictor
        Load pre-trained models for different scan types
        """
        self.models = {}
        self.model_paths = {
            'xray': 'app/ai_model/models/chest_xray_model.h5',
            'mri': 'app/ai_model/models/mri_model.h5',
            'ct_scan': 'app/ai_model/models/ct_scan_model.h5',
            'ultrasound': 'app/ai_model/models/ultrasound_model.h5'
        }
        self.disease_labels = {
            'xray': ['Pneumonia', 'Tuberculosis', 'COVID-19', 'Lung Opacity', 'Normal'],
            'mri': ['Brain Tumor', 'Stroke', 'Normal'],
            'ct_scan': ['Lung Cancer', 'Kidney Stone', 'Brain Hemorrhage'],
            'ultrasound': ['Liver Disease', 'Kidney Disease', 'Gallstone']
        }
        self._load_models()
    
    def _load_models(self):
        """
        Load pre-trained models
        Note: Models should be trained and saved separately
        """
        try:
            for scan_type, model_path in self.model_paths.items():
                if os.path.exists(model_path):
                    try:
                        self.models[scan_type] = keras.models.load_model(model_path)
                        current_app.logger.info(f'Loaded {scan_type} model')
                    except Exception as e:
                        current_app.logger.warning(f'Failed to load {scan_type} model: {str(e)}')
                else:
                    current_app.logger.warning(f'Model file not found: {model_path}')
        except Exception as e:
            current_app.logger.error(f'Error loading models: {str(e)}')
    
    def predict(self, image_array, scan_type):
        """
        Make prediction on medical image
        
        Args:
            image_array: Preprocessed image array
            scan_type: Type of scan (xray, mri, ct_scan, ultrasound)
        
        Returns:
            Dictionary with prediction results
        """
        try:
            start_time = datetime.now()
            
            # Check if model is loaded
            if scan_type not in self.models:
                raise ValueError(f'Model not available for {scan_type}')
            
            model = self.models[scan_type]
            labels = self.disease_labels[scan_type]
            
            # Make prediction
            predictions = model.predict(image_array)
            
            # Get top predictions
            pred_scores = predictions[0]
            top_indices = np.argsort(pred_scores)[::-1]
            
            # Calculate prediction time
            prediction_time = (datetime.now() - start_time).total_seconds()
            
            # Format results
            results = {
                'predicted_disease': labels[top_indices[0]],
                'confidence_score': float(pred_scores[top_indices[0]]),
                'top_5_predictions': [
                    {
                        'disease': labels[idx],
                        'probability': float(pred_scores[idx])
                    }
                    for idx in top_indices[:5]
                ],
                'prediction_probabilities': {
                    labels[idx]: float(pred_scores[idx])
                    for idx in range(len(labels))
                },
                'prediction_time': prediction_time,
                'model_name': f'{scan_type}_model',
                'model_version': '1.0.0'
            }
            
            return results
        
        except Exception as e:
            current_app.logger.error(f'Prediction error: {str(e)}')
            raise
    
    def predict_and_save(self, scan_id, image_array, scan_type):
        """
        Make prediction and save results to database
        
        Args:
            scan_id: Medical scan ID
            image_array: Preprocessed image array
            scan_type: Type of scan
        
        Returns:
            Prediction object
        """
        try:
            # Get prediction
            pred_results = self.predict(image_array, scan_type)
            
            # Create prediction record
            prediction = Prediction(
                scan_id=scan_id,
                model_name=pred_results['model_name'],
                model_version=pred_results['model_version'],
                predicted_disease=pred_results['predicted_disease'],
                confidence_score=pred_results['confidence_score'],
                prediction_probabilities=pred_results['prediction_probabilities'],
                top_5_predictions=pred_results['top_5_predictions'],
                prediction_time=pred_results['prediction_time'],
                raw_output={'predictions': pred_results}
            )
            
            db.session.add(prediction)
            
            # Update scan status
            scan = MedicalScan.query.get(scan_id)
            if scan:
                scan.status = 'prediction_ready'
                scan.processing_time = pred_results['prediction_time']
            
            db.session.commit()
            
            return prediction
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error saving prediction: {str(e)}')
            raise
