"""
Image Preprocessing Service
"""
import cv2
import numpy as np
from PIL import Image
from flask import current_app
import os


class ImagePreprocessor:
    """Image preprocessing for medical scans"""
    
    def __init__(self, target_size=(224, 224)):
        """
        Initialize preprocessor
        
        Args:
            target_size: Target image size for model input
        """
        self.target_size = target_size
    
    def preprocess_image(self, image_path):
        """
        Preprocess medical scan image
        
        Args:
            image_path: Path to image file
        
        Returns:
            Preprocessed image array
        """
        try:
            # Read image
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                raise ValueError('Failed to read image')
            
            # Resize
            image = cv2.resize(image, self.target_size)
            
            # Normalize (0-1)
            image = image.astype('float32') / 255.0
            
            # Remove noise using bilateral filter
            image = cv2.bilateralFilter(
                (image * 255).astype('uint8'), 9, 75, 75
            )
            image = image.astype('float32') / 255.0
            
            # Enhance contrast using CLAHE
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            image = clahe.apply((image * 255).astype('uint8'))
            image = image.astype('float32') / 255.0
            
            # Add channel dimension for model
            image = np.expand_dims(image, axis=-1)
            image = np.expand_dims(image, axis=0)
            
            return image
        
        except Exception as e:
            current_app.logger.error(f'Image preprocessing error: {str(e)}')
            raise
    
    def validate_image(self, image_path):
        """
        Validate image file
        
        Args:
            image_path: Path to image file
        
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            # Check file exists
            if not os.path.exists(image_path):
                return False, 'File not found'
            
            # Check file size (max 50MB)
            file_size = os.path.getsize(image_path)
            if file_size > 50 * 1024 * 1024:
                return False, 'File size exceeds 50MB limit'
            
            # Validate image can be read
            image = cv2.imread(image_path)
            if image is None:
                return False, 'Invalid image file'
            
            return True, 'Valid'
        
        except Exception as e:
            return False, str(e)
    
    def save_preprocessed_image(self, image_array, output_path):
        """
        Save preprocessed image
        
        Args:
            image_array: Numpy array of image
            output_path: Output file path
        
        Returns:
            Boolean indicating success
        """
        try:
            # Remove batch dimension if present
            if len(image_array.shape) == 4:
                image_array = image_array[0]
            
            # Remove channel dimension if present
            if len(image_array.shape) == 3 and image_array.shape[-1] == 1:
                image_array = image_array[:, :, 0]
            
            # Normalize to 0-255
            image_array = (image_array * 255).astype('uint8')
            
            # Save image
            cv2.imwrite(output_path, image_array)
            return True
        
        except Exception as e:
            current_app.logger.error(f'Error saving preprocessed image: {str(e)}')
            return False
