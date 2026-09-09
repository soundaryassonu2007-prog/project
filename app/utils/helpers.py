"""
Helper functions
"""
from datetime import datetime
import os
from flask import current_app


def generate_unique_filename(original_filename, prefix=''):
    """
    Generate unique filename
    
    Args:
        original_filename: Original filename
        prefix: Filename prefix
    
    Returns:
        Unique filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(original_filename)
    return f"{prefix}_{timestamp}{ext}"


def get_file_extension(filename):
    """
    Get file extension
    
    Args:
        filename: Filename
    
    Returns:
        File extension
    """
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def calculate_age(date_of_birth):
    """
    Calculate age from date of birth
    
    Args:
        date_of_birth: Date of birth
    
    Returns:
        Age in years
    """
    today = datetime.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def get_datetime_string(dt):
    """
    Format datetime as string
    
    Args:
        dt: Datetime object
    
    Returns:
        Formatted datetime string
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else 'N/A'


def safe_json_dumps(data):
    """
    Safely convert to JSON string
    
    Args:
        data: Data to convert
    
    Returns:
        JSON string
    """
    import json
    try:
        return json.dumps(data)
    except Exception as e:
        current_app.logger.error(f'JSON conversion error: {str(e)}')
        return '{}'
