"""
Input validation utilities
"""
import re
from email_validator import validate_email as email_validator


def validate_email(email):
    """
    Validate email format
    
    Args:
        email: Email address to validate
    
    Returns:
        Boolean indicating if email is valid
    """
    try:
        email_validator(email, check_deliverability=False)
        return True
    except:
        return False


def validate_password(password):
    """
    Validate password strength
    
    Args:
        password: Password to validate
    
    Returns:
        Tuple of (is_valid, message)
    """
    if len(password) < 8:
        return False, 'Password must be at least 8 characters'
    
    if not re.search(r'[a-z]', password):
        return False, 'Password must contain lowercase letters'
    
    if not re.search(r'[A-Z]', password):
        return False, 'Password must contain uppercase letters'
    
    if not re.search(r'[0-9]', password):
        return False, 'Password must contain numbers'
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, 'Password must contain special characters'
    
    return True, 'Valid password'


def validate_username(username):
    """
    Validate username format
    
    Args:
        username: Username to validate
    
    Returns:
        Tuple of (is_valid, message)
    """
    if len(username) < 3:
        return False, 'Username must be at least 3 characters'
    
    if len(username) > 20:
        return False, 'Username must be at most 20 characters'
    
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, 'Username can only contain alphanumeric characters, underscores, and hyphens'
    
    return True, 'Valid username'


def validate_file_size(file_size, max_size_mb=50):
    """
    Validate file size
    
    Args:
        file_size: File size in bytes
        max_size_mb: Maximum allowed size in MB
    
    Returns:
        Tuple of (is_valid, message)
    """
    max_bytes = max_size_mb * 1024 * 1024
    
    if file_size > max_bytes:
        return False, f'File size exceeds {max_size_mb}MB limit'
    
    return True, 'Valid file size'


def validate_phone(phone):
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
    
    Returns:
        Tuple of (is_valid, message)
    """
    # Simple phone validation (E.164 format)
    if not re.match(r'^\+?[0-9]{10,15}$', phone.replace('-', '').replace(' ', '')):
        return False, 'Invalid phone number format'
    
    return True, 'Valid phone number'
