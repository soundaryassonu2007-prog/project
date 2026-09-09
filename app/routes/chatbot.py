"""
Chatbot Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.chat_history import ChatHistory
from app.services.chatbot_service import ChatbotService

chatbot_bp = Blueprint('chatbot', __name__)
chatbot_service = ChatbotService()


@chatbot_bp.route('/ask', methods=['POST'])
@jwt_required()
@limiter.limit("30 per hour")
def ask_chatbot():
    """
    Send message to chatbot
    
    JSON Payload:
    {
        "message": "string",
        "session_id": "string (optional)"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        message = data.get('message')
        session_id = data.get('session_id', str(user_id))
        
        if not message:
            return jsonify({'error': 'Message required'}), 400
        
        # Get chatbot response
        response = chatbot_service.get_response(message)
        
        # Save to chat history
        chat = ChatHistory(
            user_id=user_id,
            session_id=session_id,
            user_message=message,
            bot_response=response['answer'],
            message_type=response.get('type', 'general')
        )
        db.session.add(chat)
        db.session.commit()
        
        return jsonify({
            'session_id': session_id,
            'message': message,
            'response': response['answer'],
            'message_type': response.get('type', 'general')
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/chat-history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """
    Get user's chat history
    """
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        chats = ChatHistory.query.filter_by(user_id=user_id).order_by(
            ChatHistory.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'chats': [chat.to_dict() for chat in chats.items],
            'total': chats.total,
            'pages': chats.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chatbot_bp.route('/faq', methods=['GET'])
def get_faq():
    """
    Get frequently asked questions
    """
    try:
        faq = chatbot_service.get_faq()
        return jsonify({'faq': faq}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
