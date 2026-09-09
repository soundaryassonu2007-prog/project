"""
Email Service
"""
from flask import current_app, render_template_string
from flask_mail import Mail, Message
from app import mail


class EmailService:
    """Email service for sending notifications"""
    
    @staticmethod
    def send_welcome_email(email, username):
        """
        Send welcome email to new user
        """
        try:
            subject = 'Welcome to AI Radiology Assistant'
            html = f"""
            <h2>Welcome {username}!</h2>
            <p>Thank you for registering with AI Radiology Assistant.</p>
            <p>Your account has been created successfully.</p>
            <p>You can now login with your credentials.</p>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send welcome email: {str(e)}')
            return False
    
    @staticmethod
    def send_otp_email(email, otp):
        """
        Send OTP via email
        """
        try:
            subject = 'Your OTP for Password Reset'
            html = f"""
            <h2>Password Reset OTP</h2>
            <p>Your OTP for password reset is:</p>
            <h1 style="color: #007bff;">{otp}</h1>
            <p>This OTP is valid for 10 minutes.</p>
            <p>Do not share this OTP with anyone.</p>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send OTP email: {str(e)}')
            return False
    
    @staticmethod
    def send_password_reset_confirmation(email):
        """
        Send password reset confirmation email
        """
        try:
            subject = 'Password Reset Successful'
            html = """
            <h2>Password Reset Successful</h2>
            <p>Your password has been reset successfully.</p>
            <p>You can now login with your new password.</p>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send confirmation email: {str(e)}')
            return False
    
    @staticmethod
    def send_scan_notification(email, patient_name, scan_type):
        """
        Send scan upload notification
        """
        try:
            subject = f'New Medical Scan Uploaded - {scan_type}'
            html = f"""
            <h2>New Medical Scan Uploaded</h2>
            <p>Dear Doctor,</p>
            <p>A new {scan_type} scan has been uploaded by {patient_name}.</p>
            <p>Please review and provide your diagnosis.</p>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send scan notification: {str(e)}')
            return False
    
    @staticmethod
    def send_report_ready_notification(email, patient_name, report_id):
        """
        Send report ready notification
        """
        try:
            subject = 'Your Medical Report is Ready'
            html = f"""
            <h2>Medical Report Ready</h2>
            <p>Dear {patient_name},</p>
            <p>Your medical report is now ready for download.</p>
            <p>Report ID: {report_id}</p>
            <p>Please login to your account to view and download your report.</p>
            """
            
            msg = Message(
                subject=subject,
                recipients=[email],
                html=html
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f'Failed to send report notification: {str(e)}')
            return False
