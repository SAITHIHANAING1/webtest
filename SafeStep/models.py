"""
Enhanced Database Models for SafeStep with Real Epilepsy Data
Based on multiple real research datasets:
1. EEG dataset for interictal epileptiform discharge (Nature Scientific Data 2025)
2. Long-term multi-site LFP activity dataset (Nature Scientific Data 2025) 
3. Mesoscale insights in Epileptic Networks dataset (Nature Scientific Data 2025)
4. SzCORE seizure detection challenge dataset (2025)
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app import db
import json

class IncidentRecord(db.Model):
    """
    Enhanced model for storing real epilepsy incident data
    Based on research datasets from Nature Scientific Data 2025
    """
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Patient Information
    patient_id = db.Column(db.String(20), nullable=False, index=True)  # e.g., sub-01, sub-02
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))  # M/F
    
    # Incident Details
    incident_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    incident_type = db.Column(db.String(50), nullable=False)  # seizure, fall, medication_issue, etc.
    severity = db.Column(db.String(20))  # mild, moderate, severe, critical
    duration_seconds = db.Column(db.Integer)  # Duration of incident
    
    # Seizure-Specific Information (if applicable)
    seizure_type = db.Column(db.String(50))  # focal, generalized, absence, tonic-clonic, etc.
    consciousness_state = db.Column(db.String(20))  # awake, asleep, impaired
    seizure_onset_pattern = db.Column(db.String(50))  # LVFA, rhythmic_spikes, theta_alpha, beta_gamma
    affected_regions = db.Column(db.Text)  # JSON: ["frontal", "temporal", "occipital", etc.]
    
    # Location and Context
    location = db.Column(db.String(100), nullable=False)
    environment = db.Column(db.String(50))  # home, hospital, public, work
    triggers = db.Column(db.Text)  # JSON array of potential triggers
    
    # EEG/Monitoring Data (if available)
    eeg_recorded = db.Column(db.Boolean, default=False)
    sampling_rate = db.Column(db.Integer)  # Hz, typically 256, 500, 1000, or 30000
    electrode_count = db.Column(db.Integer)  # Number of electrodes used
    hfo_detected = db.Column(db.Boolean, default=False)  # High-frequency oscillations
    
    # Response and Outcome
    response_time_minutes = db.Column(db.Float)  # Time to response/intervention
    intervention_type = db.Column(db.String(100))  # medication, emergency_services, etc.
    outcome = db.Column(db.String(50))  # resolved, hospitalized, ongoing
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'age': self.age,
            'gender': self.gender,
            'incident_date': self.incident_date.isoformat() if self.incident_date else None,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'duration_seconds': self.duration_seconds,
            'seizure_type': self.seizure_type,
            'consciousness_state': self.consciousness_state,
            'location': self.location,
            'environment': self.environment,
            'response_time_minutes': self.response_time_minutes,
            'outcome': self.outcome,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PwidProfile(db.Model):
    """
    Person with Intellectual Disability Profile
    Enhanced with real epilepsy research data patterns
    """
    __tablename__ = 'pwids'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False)
    
    # Personal Information
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    
    # Medical Information
    epilepsy_type = db.Column(db.String(50))  # focal, generalized, combined
    seizure_frequency = db.Column(db.String(50))  # daily, weekly, monthly, rare
    medication_regimen = db.Column(db.Text)  # JSON of medications
    
    # Risk Assessment (Updated by Prediction Engine)
    risk_status = db.Column(db.String(20), default='Low')  # Low, Medium, High, Critical
    risk_score = db.Column(db.Float, default=0.0)  # 0.0-100.0
    last_risk_update = db.Column(db.DateTime)
    
    # Recent Activity Patterns
    recent_seizure_count = db.Column(db.Integer, default=0)  # Last 7 days
    average_response_time = db.Column(db.Float)  # Minutes
    last_incident_date = db.Column(db.DateTime)
    
    # Clinical Data
    electrode_implant = db.Column(db.Boolean, default=False)
    monitoring_type = db.Column(db.String(50))  # scalp_eeg, ieeg, utah_array, etc.
    hfo_burden = db.Column(db.Float)  # High-frequency oscillation burden
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    incidents = db.relationship('IncidentRecord', 
                               primaryjoin='PwidProfile.patient_id == IncidentRecord.patient_id',
                               foreign_keys='IncidentRecord.patient_id',
                               backref='patient_profile')

class PredictionJob(db.Model):
    """
    Track AI prediction engine jobs and results
    """
    __tablename__ = 'prediction_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(50), nullable=False)  # daily_analysis, risk_assessment, etc.
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    
    # Analysis Parameters
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow)
    lookback_days = db.Column(db.Integer, default=7)
    patients_analyzed = db.Column(db.Integer, default=0)
    
    # Results
    high_risk_identified = db.Column(db.Integer, default=0)
    risk_escalations = db.Column(db.Integer, default=0)
    risk_reductions = db.Column(db.Integer, default=0)
    
    # Performance Metrics
    processing_time_seconds = db.Column(db.Float)
    accuracy_score = db.Column(db.Float)  # If validation data available
    
    # Metadata
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_type': self.job_type,
            'status': self.status,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'patients_analyzed': self.patients_analyzed,
            'high_risk_identified': self.high_risk_identified,
            'processing_time_seconds': self.processing_time_seconds,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class DatasetReference(db.Model):
    """
    Track real datasets used as reference for our synthetic data
    """
    __tablename__ = 'dataset_references'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer)
    doi = db.Column(db.String(100))
    description = db.Column(db.Text)
    patient_count = db.Column(db.Integer)
    seizure_count = db.Column(db.Integer)
    recording_hours = db.Column(db.Float)
    
    # Usage tracking
    used_for_generation = db.Column(db.Boolean, default=False)
    generation_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
