import os
import json
import csv
import io
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import numpy as np
from io import BytesIO
import base64

class AnalyticsExporter:
    """Handles export functionality for analytics data"""
    
    def __init__(self, supabase_client=None):
        self.supabase = supabase_client
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        )
        
        self.table_style = ParagraphStyle(
            'CustomTable',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=3
        )
    
    def generate_analytics_pdf(self, filters, data, charts_data=None):
        """Generate a comprehensive PDF report for analytics data"""
        try:
            # Create a temporary file for the PDF
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f'analytics_report_{timestamp}.pdf'
            filepath = os.path.join('static', 'reports', filename)
            
            # Ensure reports directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Add title page
            story.extend(self.create_title_page(filters))
            
            # Add summary section
            story.extend(self.create_summary_section(data))
            
            # Add charts section if data available
            if charts_data:
                story.extend(self.create_charts_section(charts_data))
            
            # Add detailed data section
            story.extend(self.create_data_section(data))
            
            # Add recommendations section
            story.extend(self.create_recommendations_section(data))
            
            # Build PDF
            doc.build(story)
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': filename,
                'download_url': f'/static/reports/{filename}'
            }
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_title_page(self, filters):
        """Create the title page of the report"""
        elements = []
        
        # Title
        title = Paragraph("SafeStep Analytics Report", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 30))
        
        # Report metadata
        metadata = [
            ["Report Generated:", datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')],
            ["Report Period:", f"Last {filters.get('dateRange', '30')} days"],
            ["Data Source:", "Supabase PostgreSQL Database"],
            ["Filters Applied:", json.dumps(filters, indent=2)]
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(metadata_table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def create_summary_section(self, data):
        """Create the summary section with key metrics"""
        elements = []
        
        # Section heading
        heading = Paragraph("Executive Summary", self.heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        # Key metrics table
        metrics_data = [
            ["Metric", "Value", "Change"],
            ["Total Incidents", str(data.get('total_incidents', 0)), "N/A"],
            ["Seizure Events", str(data.get('seizure_count', 0)), "N/A"],
            ["High-Risk Patients", str(data.get('high_risk_patients', 0)), "N/A"],
            ["Average Response Time", f"{data.get('avg_response_time', 0):.1f} min", "N/A"],
            ["Active Monitoring", str(data.get('active_monitoring', 0)), "N/A"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def create_charts_section(self, charts_data):
        """Create charts section with visualizations"""
        elements = []
        
        heading = Paragraph("Data Visualizations", self.heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        # Generate and add charts
        if 'trends' in charts_data:
            trend_chart = self.generate_trend_chart(charts_data['trends'])
            if trend_chart:
                elements.append(Paragraph("Seizure Trends", self.normal_style))
                elements.append(trend_chart)
                elements.append(Spacer(1, 12))
        
        if 'distribution' in charts_data:
            dist_chart = self.generate_distribution_chart(charts_data['distribution'])
            if dist_chart:
                elements.append(Paragraph("Location Distribution", self.normal_style))
                elements.append(dist_chart)
                elements.append(Spacer(1, 12))
        
        return elements
    
    def create_data_section(self, data):
        """Create detailed data section"""
        elements = []
        
        heading = Paragraph("Detailed Data Analysis", self.heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        # Recent incidents table
        if 'recent_incidents' in data and data['recent_incidents']:
            elements.append(Paragraph("Recent Incidents", self.normal_style))
            
            incident_headers = ["Date", "Patient ID", "Type", "Severity", "Location"]
            incident_rows = [incident_headers]
            
            for incident in data['recent_incidents'][:10]:  # Show last 10
                incident_rows.append([
                    incident.get('incident_date', 'N/A'),
                    incident.get('patient_id', 'N/A'),
                    incident.get('incident_type', 'N/A'),
                    incident.get('severity', 'N/A'),
                    incident.get('location', 'N/A')
                ])
            
            incident_table = Table(incident_rows, colWidths=[1*inch, 1*inch, 1*inch, 0.8*inch, 1.2*inch])
            incident_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
            ]))
            
            elements.append(incident_table)
            elements.append(Spacer(1, 20))
        
        return elements
    
    def create_recommendations_section(self, data):
        """Create recommendations section"""
        elements = []
        
        heading = Paragraph("Recommendations & Next Steps", self.heading_style)
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        recommendations = [
            "• Continue monitoring high-risk patients closely",
            "• Review and update safety protocols based on incident patterns",
            "• Schedule regular risk assessments for all patients",
            "• Implement additional safety measures in high-incident locations",
            "• Consider enhanced monitoring for patients with frequent seizures",
            "• Review medication compliance and adjust dosages if necessary"
        ]
        
        for rec in recommendations:
            elements.append(Paragraph(rec, self.normal_style))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def generate_trend_chart(self, trends_data):
        """Generate a trend chart for the PDF"""
        try:
            plt.figure(figsize=(8, 4))
            
            dates = [item['date'] for item in trends_data]
            values = [item['count'] for item in trends_data]
            
            plt.plot(dates, values, marker='o', linewidth=2, markersize=4)
            plt.title('Seizure Trends Over Time', fontsize=12, fontweight='bold')
            plt.xlabel('Date')
            plt.ylabel('Number of Seizures')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # Save to bytes buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            # Convert to ReportLab image
            img = Image(buffer)
            img.drawHeight = 3*inch
            img.drawWidth = 6*inch
            
            return img
            
        except Exception as e:
            print(f"Error generating trend chart: {e}")
            return None
    
    def generate_distribution_chart(self, dist_data):
        """Generate a distribution chart for the PDF"""
        try:
            plt.figure(figsize=(6, 4))
            
            locations = [item['location'] for item in dist_data]
            counts = [item['count'] for item in dist_data]
            
            plt.pie(counts, labels=locations, autopct='%1.1f%%', startangle=90)
            plt.title('Incident Distribution by Location', fontsize=12, fontweight='bold')
            plt.axis('equal')
            plt.tight_layout()
            
            # Save to bytes buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            plt.close()
            
            # Convert to ReportLab image
            img = Image(buffer)
            img.drawHeight = 3*inch
            img.drawWidth = 4*inch
            
            return img
            
        except Exception as e:
            print(f"Error generating distribution chart: {e}")
            return None
    
    def export_to_csv(self, data, filename=None):
        """Export data to CSV format"""
        try:
            if not filename:
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                filename = f'analytics_export_{timestamp}.csv'
            
            # Create CSV data
            csv_data = []
            
            # Add summary metrics
            csv_data.append(['METRICS SUMMARY'])
            csv_data.append(['Metric', 'Value'])
            csv_data.append(['Total Incidents', data.get('total_incidents', 0)])
            csv_data.append(['Seizure Events', data.get('seizure_count', 0)])
            csv_data.append(['High-Risk Patients', data.get('high_risk_patients', 0)])
            csv_data.append([])
            
            # Add incidents data
            if 'recent_incidents' in data and data['recent_incidents']:
                csv_data.append(['RECENT INCIDENTS'])
                csv_data.append(['Date', 'Patient ID', 'Type', 'Severity', 'Location', 'Environment'])
                
                for incident in data['recent_incidents']:
                    csv_data.append([
                        incident.get('incident_date', ''),
                        incident.get('patient_id', ''),
                        incident.get('incident_type', ''),
                        incident.get('severity', ''),
                        incident.get('location', ''),
                        incident.get('environment', '')
                    ])
                csv_data.append([])
            
            # Add patients data
            if 'patients' in data and data['patients']:
                csv_data.append(['PATIENT PROFILES'])
                csv_data.append(['Patient ID', 'Age', 'Gender', 'Epilepsy Type', 'Risk Level', 'Risk Score'])
                
                for patient in data['patients']:
                    csv_data.append([
                        patient.get('patient_id', ''),
                        patient.get('age', ''),
                        patient.get('gender', ''),
                        patient.get('epilepsy_type', ''),
                        patient.get('risk_status', ''),
                        patient.get('risk_score', '')
                    ])
            
            # Write to string buffer
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(csv_data)
            
            return {
                'success': True,
                'data': output.getvalue(),
                'filename': filename
            }
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def export_patient_report(self, patient_id, patient_data, incidents_data):
        """Generate a patient-specific report"""
        try:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f'patient_report_{patient_id}_{timestamp}.pdf'
            filepath = os.path.join('static', 'reports', filename)
            
            # Ensure reports directory exists
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Create PDF document
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            story = []
            
            # Patient information
            story.append(Paragraph(f"Patient Report - {patient_id}", self.title_style))
            story.append(Spacer(1, 20))
            
            # Patient details table
            patient_info = [
                ["Patient ID:", patient_data.get('patient_id', 'N/A')],
                ["Age:", str(patient_data.get('age', 'N/A'))],
                ["Gender:", patient_data.get('gender', 'N/A')],
                ["Epilepsy Type:", patient_data.get('epilepsy_type', 'N/A')],
                ["Risk Level:", patient_data.get('risk_status', 'N/A')],
                ["Risk Score:", f"{patient_data.get('risk_score', 0):.1f}/100"]
            ]
            
            patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
            patient_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(patient_table)
            story.append(Spacer(1, 20))
            
            # Recent incidents
            if incidents_data:
                story.append(Paragraph("Recent Incidents", self.heading_style))
                
                incident_headers = ["Date", "Type", "Severity", "Location", "Duration"]
                incident_rows = [incident_headers]
                
                for incident in incidents_data[:10]:
                    incident_rows.append([
                        incident.get('incident_date', 'N/A'),
                        incident.get('incident_type', 'N/A'),
                        incident.get('severity', 'N/A'),
                        incident.get('location', 'N/A'),
                        f"{incident.get('duration_seconds', 0)}s"
                    ])
                
                incident_table = Table(incident_rows, colWidths=[1.2*inch, 1*inch, 0.8*inch, 1.5*inch, 0.7*inch])
                incident_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey)
                ]))
                
                story.append(incident_table)
            
            # Build PDF
            doc.build(story)
            
            return {
                'success': True,
                'filepath': filepath,
                'filename': filename,
                'download_url': f'/static/reports/{filename}'
            }
            
        except Exception as e:
            print(f"Error generating patient report: {e}")
            return {
                'success': False,
                'error': str(e)
            }
