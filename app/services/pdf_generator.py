"""
PDF Report Generator Service
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from flask import current_app
from datetime import datetime
import qrcode
import io
import os


class PDFReportGenerator:
    """Generate professional medical PDF reports"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.page_width, self.page_height = letter
        self.styles = getSampleStyleSheet()
    
    def generate_report(self, report_data, output_path):
        """
        Generate comprehensive medical report
        
        Args:
            report_data: Dictionary containing report information
            output_path: Output PDF file path
        
        Returns:
            Boolean indicating success
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Container for PDF elements
            elements = []
            
            # Add header
            elements.extend(self._create_header(report_data))
            elements.append(Spacer(1, 0.3*inch))
            
            # Add patient information
            elements.extend(self._create_patient_section(report_data))
            elements.append(Spacer(1, 0.2*inch))
            
            # Add scan information
            elements.extend(self._create_scan_section(report_data))
            elements.append(Spacer(1, 0.2*inch))
            
            # Add AI prediction
            elements.extend(self._create_prediction_section(report_data))
            elements.append(Spacer(1, 0.2*inch))
            
            # Add doctor diagnosis
            elements.extend(self._create_diagnosis_section(report_data))
            elements.append(Spacer(1, 0.2*inch))
            
            # Add prescription
            if 'prescription' in report_data and report_data['prescription']:
                elements.extend(self._create_prescription_section(report_data))
                elements.append(Spacer(1, 0.2*inch))
            
            # Add signature section
            elements.extend(self._create_signature_section(report_data))
            
            # Add QR code
            elements.append(Spacer(1, 0.2*inch))
            elements.extend(self._create_qr_section(report_data))
            
            # Build PDF
            doc.build(elements)
            return True
        
        except Exception as e:
            current_app.logger.error(f'Error generating PDF: {str(e)}')
            return False
    
    def _create_header(self, data):
        """Create report header"""
        elements = []
        
        # Hospital name and title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003366'),
            spaceAfter=6,
            alignment=1  # Center
        )
        
        elements.append(Paragraph('AI RADIOLOGY ASSISTANT', title_style))
        elements.append(Paragraph('Medical Scan Analysis Report', self.styles['Heading2']))
        
        # Date and report ID
        date_style = ParagraphStyle(
            'Date',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=1
        )
        elements.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            date_style
        ))
        
        if 'report_id' in data:
            elements.append(Paragraph(f"Report ID: {data['report_id']}", date_style))
        
        return elements
    
    def _create_patient_section(self, data):
        """Create patient information section"""
        elements = []
        elements.append(Paragraph('PATIENT INFORMATION', self.styles['Heading2']))
        
        patient_data = [
            ['Field', 'Value'],
            ['Name', data.get('patient_name', 'N/A')],
            ['Age', str(data.get('patient_age', 'N/A'))],
            ['Gender', data.get('patient_gender', 'N/A')],
            ['Patient ID', str(data.get('patient_id', 'N/A'))],
            ['Date of Scan', data.get('scan_date', 'N/A')],
        ]
        
        table = Table(patient_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_scan_section(self, data):
        """Create scan information section"""
        elements = []
        elements.append(Paragraph('SCAN INFORMATION', self.styles['Heading2']))
        
        scan_data = [
            ['Field', 'Value'],
            ['Scan Type', data.get('scan_type', 'N/A')],
            ['Scan Category', data.get('scan_category', 'N/A')],
            ['File Format', data.get('file_format', 'N/A')],
        ]
        
        table = Table(scan_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_prediction_section(self, data):
        """Create AI prediction section"""
        elements = []
        elements.append(Paragraph('AI PREDICTION RESULTS', self.styles['Heading2']))
        
        pred_style = ParagraphStyle(
            'Prediction',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#003366')
        )
        
        elements.append(Paragraph(
            f"<b>Predicted Disease:</b> {data.get('predicted_disease', 'N/A')}",
            pred_style
        ))
        elements.append(Paragraph(
            f"<b>Confidence Score:</b> {data.get('confidence_score', 0):.2%}",
            pred_style
        ))
        
        if 'top_5_predictions' in data:
            elements.append(Paragraph(
                f"<b>Top Predictions:</b> {data['top_5_predictions']}",
                pred_style
            ))
        
        return elements
    
    def _create_diagnosis_section(self, data):
        """Create doctor diagnosis section"""
        elements = []
        elements.append(Paragraph('DOCTOR DIAGNOSIS', self.styles['Heading2']))
        
        diag_style = ParagraphStyle(
            'Diagnosis',
            parent=self.styles['Normal'],
            fontSize=11
        )
        
        elements.append(Paragraph(
            f"<b>Doctor's Diagnosis:</b> {data.get('doctor_diagnosis', 'N/A')}",
            diag_style
        ))
        
        if 'clinical_findings' in data:
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(
                f"<b>Clinical Findings:</b>",
                diag_style
            ))
            elements.append(Paragraph(
                data.get('clinical_findings', 'N/A'),
                self.styles['Normal']
            ))
        
        return elements
    
    def _create_prescription_section(self, data):
        """Create prescription section"""
        elements = []
        elements.append(Paragraph('PRESCRIPTION', self.styles['Heading2']))
        
        prescription = data.get('prescription', {})
        
        presc_data = [
            ['Field', 'Value'],
            ['Medicine', prescription.get('medicine_name', 'N/A')],
            ['Dosage', prescription.get('dosage', 'N/A')],
            ['Frequency', prescription.get('frequency', 'N/A')],
            ['Duration', prescription.get('duration', 'N/A')],
            ['Instructions', prescription.get('instructions', 'N/A')],
        ]
        
        if prescription.get('followup_date'):
            presc_data.append(['Follow-up Date', prescription['followup_date']])
        
        table = Table(presc_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        return elements
    
    def _create_signature_section(self, data):
        """Create signature section"""
        elements = []
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph('DOCTOR SIGNATURE', self.styles['Heading2']))
        
        sig_data = [
            ['Doctor Name', 'Signature', 'Date'],
            [data.get('doctor_name', '_______________'), '______________', '_______________'],
        ]
        
        table = Table(sig_data)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))
        
        elements.append(table)
        return elements
    
    def _create_qr_section(self, data):
        """Create QR code section"""
        elements = []
        
        try:
            # Generate QR code
            qr_data = f"Report ID: {data.get('report_id', 'N/A')}"
            qr = qrcode.QRCode(version=1, box_size=5, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code to temporary file
            qr_path = os.path.join(current_app.config['REPORTS_FOLDER'], 'temp_qr.png')
            qr_image.save(qr_path)
            
            # Add QR code to PDF
            elements.append(Paragraph('Verification QR Code', self.styles['Heading3']))
            elements.append(Image(qr_path, width=1*inch, height=1*inch))
        
        except Exception as e:
            current_app.logger.error(f'Error creating QR code: {str(e)}')
        
        return elements
