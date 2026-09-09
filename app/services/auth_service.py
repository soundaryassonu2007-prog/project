"""
Authentication Service
"""
from datetime import datetime, timedelta
import random
import string
from app import db


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def generate_otp(length=6):
        """
        Generate OTP
        
        Args:
            length: OTP length
        
        Returns:
            Tuple of (otp, expiry_time)
        """
        otp = ''.join(random.choices(string.digits, k=length))
        expiry = datetime.utcnow() + timedelta(minutes=10)
        return otp, expiry
    
    @staticmethod
    def verify_otp(stored_otp, expiry_time, provided_otp):
        """
        Verify OTP
        
        Args:
            stored_otp: OTP stored in database
            expiry_time: OTP expiry time
            provided_otp: OTP provided by user
        
        Returns:
            Tuple of (is_valid, message)
        """
        if not stored_otp:
            return False, 'No OTP generated'
        
        if datetime.utcnow() > expiry_time:
            return False, 'OTP expired'
        
        if stored_otp != provided_otp:
            return False, 'Invalid OTP'
        
        return True, 'OTP verified'
