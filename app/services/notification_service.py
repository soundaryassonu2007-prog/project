"""
Notification Service
"""
from flask import current_app
from app import db
from app.models.notification import Notification
from app.services.email_service import EmailService
from datetime import datetime


class NotificationService:
    """Handle user notifications"""
    
    @staticmethod
    def create_notification(user_id, notification_type, title, message, scan_id=None):
        """
        Create new notification
        
        Args:
            user_id: User ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            scan_id: Related scan ID (optional)
        
        Returns:
            Notification object
        """
        try:
            notification = Notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                scan_id=scan_id
            )
            db.session.add(notification)
            db.session.commit()
            return notification
        
        except Exception as e:
            current_app.logger.error(f'Error creating notification: {str(e)}')
            return None
    
    @staticmethod
    def send_email_notification(user_email, subject, message):
        """
        Send email notification
        
        Args:
            user_email: User email address
            subject: Email subject
            message: Email message
        
        Returns:
            Boolean indicating success
        """
        try:
            email_service = EmailService()
            # Implement email sending logic
            return True
        
        except Exception as e:
            current_app.logger.error(f'Error sending email: {str(e)}')
            return False
    
    @staticmethod
    def mark_as_read(notification_id):
        """
        Mark notification as read
        
        Args:
            notification_id: Notification ID
        
        Returns:
            Boolean indicating success
        """
        try:
            notification = Notification.query.get(notification_id)
            if notification:
                notification.is_read = True
                notification.read_at = datetime.utcnow()
                db.session.commit()
                return True
            return False
        
        except Exception as e:
            current_app.logger.error(f'Error marking notification as read: {str(e)}')
            return False
