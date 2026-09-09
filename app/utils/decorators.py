"""
Decorators for route protection and access control
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def require_role(*roles):
    """
    Decorator to require specific user roles
    
    Args:
        *roles: Required roles
    
    Returns:
        Decorated function
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            if claims.get('role') not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_verified():
    """
    Decorator to require verified user
    
    Returns:
        Decorated function
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from flask_jwt_extended import get_jwt_identity
            from app.models.user import User
            
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_verified:
                return jsonify({'error': 'Email verification required'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator
