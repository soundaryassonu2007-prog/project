"""
Chat History Model - Chatbot Conversations
"""
from datetime import datetime
from app import db


class ChatHistory(db.Model):
    """Chatbot conversation history"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)  # Conversation session ID
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    message_type = db.Column(
        db.Enum(
            'faq',
            'disease_info',
            'scan_prep',
            'medication',
            'appointment',
            'general'
        ),
        default='general'
    )
    sentiment = db.Column(db.String(50))  # positive, negative, neutral
    user_rating = db.Column(db.Integer)  # 1-5 rating
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'message_type': self.message_type,
            'user_rating': self.user_rating,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ChatHistory session={self.session_id}>'
