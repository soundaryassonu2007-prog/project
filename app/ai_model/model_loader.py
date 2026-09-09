"""
Model Loader - Load and manage AI models
"""
import tensorflow as tf
from tensorflow import keras
from flask import current_app
import os


class ModelLoader:
    """Load and manage pre-trained AI models"""
    
    _instance = None
    _models = {}
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def load_model(cls, model_name, model_path):
        """
        Load a model
        
        Args:
            model_name: Name of the model
            model_path: Path to model file
        
        Returns:
            Loaded model
        """
        try:
            if model_name in cls._models:
                return cls._models[model_name]
            
            if not os.path.exists(model_path):
                current_app.logger.warning(f'Model file not found: {model_path}')
                return None
            
            model = keras.models.load_model(model_path)
            cls._models[model_name] = model
            current_app.logger.info(f'Loaded model: {model_name}')
            
            return model
        
        except Exception as e:
            current_app.logger.error(f'Error loading model {model_name}: {str(e)}')
            return None
    
    @classmethod
    def get_model(cls, model_name):
        """
        Get loaded model
        
        Args:
            model_name: Name of the model
        
        Returns:
            Loaded model or None
        """
        return cls._models.get(model_name)
    
    @classmethod
    def unload_model(cls, model_name):
        """
        Unload a model
        
        Args:
            model_name: Name of the model
        """
        if model_name in cls._models:
            del cls._models[model_name]
            current_app.logger.info(f'Unloaded model: {model_name}')
    
    @classmethod
    def clear_all_models(cls):
        """
        Clear all loaded models
        """
        cls._models.clear()
        current_app.logger.info('Cleared all models')
