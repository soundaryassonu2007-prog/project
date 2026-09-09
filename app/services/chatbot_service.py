"""
Chatbot Service
"""
import json
import os
from flask import current_app


class ChatbotService:
    """AI Chatbot service for patient queries"""
    
    def __init__(self):
        """Initialize chatbot with knowledge base"""
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """
        Load chatbot knowledge base
        
        Returns:
            Dictionary of chatbot responses
        """
        knowledge_base = {
            'faq': [
                {
                    'question': 'What is AI Radiology Assistant?',
                    'answer': 'AI Radiology Assistant is a healthcare application that uses artificial intelligence to analyze medical scans and help predict diseases with confidence scores.'
                },
                {
                    'question': 'What types of scans are supported?',
                    'answer': 'We support X-ray, MRI, CT Scan, and Ultrasound images.'
                },
                {
                    'question': 'How accurate is the AI prediction?',
                    'answer': 'Our AI models are trained on thousands of medical images and achieve high accuracy. However, always consult with a qualified doctor for diagnosis.'
                },
                {
                    'question': 'Is my data secure?',
                    'answer': 'Yes, all patient data is encrypted and securely stored following HIPAA standards.'
                },
                {
                    'question': 'How long does prediction take?',
                    'answer': 'AI prediction typically completes within 30 seconds of upload.'
                }
            ],
            'scan_preparation': [
                {
                    'keyword': 'xray',
                    'tips': [
                        'Remove all metal objects (jewelry, buttons, zippers)',
                        'Wear comfortable, loose-fitting clothing',
                        'The procedure is painless and takes 5-10 minutes',
                        'Hold your breath as instructed during the scan'
                    ]
                },
                {
                    'keyword': 'mri',
                    'tips': [
                        'Remove all metal objects including implants',
                        'Scan takes 30-45 minutes',
                        'You will hear loud banging noises - this is normal',
                        'Stay still during the scan for best results'
                    ]
                },
                {
                    'keyword': 'ct_scan',
                    'tips': [
                        'Remove metal objects',
                        'Fast procedure, usually 5-10 minutes',
                        'May involve contrast injection',
                        'Tell technician if you have iodine allergy'
                    ]
                },
                {
                    'keyword': 'ultrasound',
                    'tips': [
                        'No special preparation needed',
                        'Gel applied to skin - helps sound waves pass',
                        'Completely painless and safe',
                        'Takes 15-30 minutes'
                    ]
                }
            ],
            'disease_info': [
                {
                    'disease': 'pneumonia',
                    'info': 'Pneumonia is a lung infection that causes inflammation in air sacs. Symptoms include cough, fever, and difficulty breathing. Treatment depends on the cause.'
                },
                {
                    'disease': 'tuberculosis',
                    'info': 'TB is a serious infection usually affecting the lungs. It is treatable with antibiotics. Early detection is crucial.'
                },
                {
                    'disease': 'covid-19',
                    'info': 'COVID-19 is a viral infection. Some cases show pneumonia-like symptoms on imaging. Prevention through vaccination is recommended.'
                },
                {
                    'disease': 'lung_cancer',
                    'info': 'Lung cancer is a serious condition. Early detection through screening improves survival rates. Consult an oncologist for treatment options.'
                },
                {
                    'disease': 'brain_tumor',
                    'info': 'Brain tumors can be benign or malignant. Treatment options include surgery, radiation, and chemotherapy. Specialist consultation is essential.'
                }
            ]
        }
        return knowledge_base
    
    def get_response(self, user_message):
        """
        Get chatbot response to user message
        
        Args:
            user_message: User query
        
        Returns:
            Dictionary with response and message type
        """
        message_lower = user_message.lower()
        
        # Check for FAQ matches
        for faq in self.knowledge_base['faq']:
            if any(keyword in message_lower for keyword in faq['question'].lower().split()):
                return {
                    'answer': faq['answer'],
                    'type': 'faq'
                }
        
        # Check for disease information
        for disease_info in self.knowledge_base['disease_info']:
            if disease_info['disease'] in message_lower:
                return {
                    'answer': disease_info['info'],
                    'type': 'disease_info'
                }
        
        # Check for scan preparation tips
        for scan_prep in self.knowledge_base['scan_preparation']:
            if scan_prep['keyword'] in message_lower:
                tips = '\n'.join([f'• {tip}' for tip in scan_prep['tips']])
                return {
                    'answer': f"Here are preparation tips for your {scan_prep['keyword'].upper()} scan:\n{tips}",
                    'type': 'scan_prep'
                }
        
        # Default response
        return {
            'answer': 'I\'m here to help! You can ask me about scan preparation, disease information, or medical concerns. Please consult a doctor for specific medical advice.',
            'type': 'general'
        }
    
    def get_faq(self):
        """
        Get all FAQs
        
        Returns:
            List of FAQ items
        """
        return self.knowledge_base['faq']
