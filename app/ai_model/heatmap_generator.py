"""
Heatmap Generator - Grad-CAM visualization
"""
import numpy as np
import cv2
import tensorflow as tf
from flask import current_app
import os
from datetime import datetime
from app import db
from app.models.heatmap import Heatmap


class HeatmapGenerator:
    """Generate Grad-CAM heatmaps for model interpretability"""
    
    def __init__(self, model):
        """
        Initialize heatmap generator
        
        Args:
            model: Keras model
        """
        self.model = model
    
    def generate_gradcam(self, image_array, layer_name=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            image_array: Input image array
            layer_name: Name of layer to use (default: last conv layer)
        
        Returns:
            Heatmap array
        """
        try:
            # Find target layer
            if layer_name is None:
                # Use last convolutional layer
                for layer in reversed(self.model.layers):
                    if 'conv' in layer.name:
                        layer_name = layer.name
                        break
            
            # Create gradient model
            grad_model = tf.keras.models.Model(
                [self.model.inputs],
                [self.model.get_layer(layer_name).output, self.model.output]
            )
            
            # Record gradients
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(image_array)
                class_idx = tf.argmax(predictions[0])
                class_channel = predictions[:, class_idx]
            
            # Compute gradients
            grads = tape.gradient(class_channel, conv_outputs)
            
            # Average pooling of gradients
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Weight activation maps by importance
            conv_outputs = conv_outputs[0]
            for i in range(pooled_grads.shape[-1]):
                conv_outputs[:, :, i] *= pooled_grads[i]
            
            # Average across channels
            heatmap = tf.reduce_mean(conv_outputs, axis=-1)
            heatmap = tf.nn.relu(heatmap)
            
            # Normalize heatmap
            heatmap_max = tf.reduce_max(heatmap)
            if heatmap_max != 0:
                heatmap = heatmap / heatmap_max
            
            return heatmap.numpy()
        
        except Exception as e:
            current_app.logger.error(f'Error generating Grad-CAM: {str(e)}')
            raise
    
    def overlay_heatmap(self, original_image_path, heatmap_array, output_path, colormap='jet'):
        """
        Overlay heatmap on original image
        
        Args:
            original_image_path: Path to original image
            heatmap_array: Grad-CAM heatmap array
            output_path: Output image path
            colormap: OpenCV colormap name
        
        Returns:
            Boolean indicating success
        """
        try:
            # Read original image
            image = cv2.imread(original_image_path)
            if image is None:
                raise ValueError('Failed to read original image')
            
            # Resize heatmap to match image
            heatmap_resized = cv2.resize(
                heatmap_array,
                (image.shape[1], image.shape[0])
            )
            
            # Normalize heatmap to 0-255
            heatmap_normalized = (heatmap_resized * 255).astype('uint8')
            
            # Apply colormap
            colormap_cv = getattr(cv2, f'COLORMAP_{colormap.upper()}')
            heatmap_colored = cv2.applyColorMap(heatmap_normalized, colormap_cv)
            
            # Overlay on original image (40% heatmap, 60% original)
            overlay = cv2.addWeighted(image, 0.6, heatmap_colored, 0.4, 0)
            
            # Save overlay
            cv2.imwrite(output_path, overlay)
            
            return True
        
        except Exception as e:
            current_app.logger.error(f'Error overlaying heatmap: {str(e)}')
            return False
    
    def save_heatmap(self, scan_id, heatmap_array, original_image_path):
        """
        Generate and save heatmap with overlay
        
        Args:
            scan_id: Medical scan ID
            heatmap_array: Grad-CAM heatmap array
            original_image_path: Path to original image
        
        Returns:
            Heatmap object
        """
        try:
            from flask import current_app
            
            # Save heatmap
            heatmap_filename = f'heatmap_{scan_id}_{datetime.now().timestamp()}.png'
            heatmap_path = os.path.join(
                current_app.config['HEATMAP_FOLDER'],
                heatmap_filename
            )
            
            # Save heatmap image
            heatmap_normalized = (heatmap_array * 255).astype('uint8')
            cv2.imwrite(heatmap_path, heatmap_normalized)
            
            # Create overlay
            overlay_filename = f'overlay_{scan_id}_{datetime.now().timestamp()}.png'
            overlay_path = os.path.join(
                current_app.config['HEATMAP_FOLDER'],
                overlay_filename
            )
            self.overlay_heatmap(original_image_path, heatmap_array, overlay_path)
            
            # Save to database
            heatmap_obj = Heatmap(
                scan_id=scan_id,
                heatmap_path=heatmap_path,
                original_image_path=original_image_path,
                overlay_path=overlay_path,
                intensity_values=heatmap_array.tolist(),
                color_map='jet'
            )
            
            db.session.add(heatmap_obj)
            db.session.commit()
            
            return heatmap_obj
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error saving heatmap: {str(e)}')
            raise
