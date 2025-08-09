#!/usr/bin/env python3
"""
Epilepsy Risk Prediction Model
Uses machine learning to predict seizure risk and provide recommendations
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
import joblib
import json
import os
from typing import Dict, List, Tuple, Optional

class EpilepsyPredictionModel:
    """
    Machine Learning model for epilepsy risk prediction
    """
    
    def __init__(self):
        self.risk_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.risk_regressor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        
    def prepare_features(self, patient_data: Dict, incident_history: List[Dict]) -> np.ndarray:
        """
        Prepare features for prediction from patient and incident data
        """
        features = []
        
        # Patient demographics
        features.extend([
            patient_data.get('age', 0),
            1 if patient_data.get('gender') == 'M' else 0,
        ])
        
        # Epilepsy type encoding
        epilepsy_type = patient_data.get('epilepsy_type', 'unknown')
        if epilepsy_type == 'focal':
            features.extend([1, 0, 0])
        elif epilepsy_type == 'generalized':
            features.extend([0, 1, 0])
        elif epilepsy_type == 'combined':
            features.extend([0, 0, 1])
        else:
            features.extend([0, 0, 0])
        
        # Seizure frequency
        freq = patient_data.get('seizure_frequency', 'unknown')
        if freq == 'daily':
            features.extend([1, 0, 0, 0])
        elif freq == 'weekly':
            features.extend([0, 1, 0, 0])
        elif freq == 'monthly':
            features.extend([0, 0, 1, 0])
        elif freq == 'rare':
            features.extend([0, 0, 0, 1])
        else:
            features.extend([0, 0, 0, 0])
        
        # Medication count
        meds = patient_data.get('medication_regimen', '[]')
        try:
            med_list = json.loads(meds) if isinstance(meds, str) else meds
            features.append(len(med_list))
        except:
            features.append(0)
        
        # Recent activity
        features.extend([
            patient_data.get('recent_seizure_count', 0),
            patient_data.get('average_response_time', 0),
            patient_data.get('hfo_burden', 0),
            1 if patient_data.get('electrode_implant') else 0
        ])
        
        # Incident history features
        if incident_history:
            recent_incidents = [inc for inc in incident_history 
                              if (datetime.now() - datetime.fromisoformat(inc['incident_date'])).days <= 30]
            
            features.extend([
                len(recent_incidents),
                sum(1 for inc in recent_incidents if inc.get('severity') == 'severe'),
                sum(1 for inc in recent_incidents if inc.get('severity') == 'critical'),
                np.mean([inc.get('response_time_minutes', 0) for inc in recent_incidents]),
                sum(1 for inc in recent_incidents if inc.get('environment') == 'hospital'),
                sum(1 for inc in recent_incidents if inc.get('outcome') == 'hospitalized')
            ])
        else:
            features.extend([0, 0, 0, 0, 0, 0])
        
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data: List[Dict]) -> Dict:
        """
        Train the prediction model with historical data
        """
        X = []
        y_risk_level = []
        y_risk_score = []
        
        for patient in training_data:
            features = self.prepare_features(patient['profile'], patient['incidents'])
            X.append(features.flatten())
            
            # Risk level classification (Low, Medium, High, Critical)
            risk_level = patient['profile'].get('risk_status', 'Low')
            y_risk_level.append(risk_level)
            
            # Risk score regression (0-100)
            risk_score = patient['profile'].get('risk_score', 0)
            y_risk_score.append(risk_score)
        
        X = np.array(X)
        
        # Train risk level classifier
        self.risk_classifier.fit(X, y_risk_level)
        
        # Train risk score regressor
        self.risk_regressor.fit(X, y_risk_score)
        
        # Scale features for future predictions
        self.scaler.fit(X)
        
        self.is_trained = True
        
        # Calculate training metrics
        y_pred_level = self.risk_classifier.predict(X)
        y_pred_score = self.risk_regressor.predict(X)
        
        accuracy = accuracy_score(y_risk_level, y_pred_level)
        mse = mean_squared_error(y_risk_score, y_pred_score)
        
        return {
            'accuracy': accuracy,
            'mse': mse,
            'training_samples': len(training_data)
        }
    
    def predict_risk(self, patient_data: Dict, incident_history: List[Dict]) -> Dict:
        """
        Predict risk level and score for a patient
        """
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        features = self.prepare_features(patient_data, incident_history)
        features_scaled = self.scaler.transform(features)
        
        # Predict risk level
        risk_level = self.risk_classifier.predict(features_scaled)[0]
        risk_level_proba = self.risk_classifier.predict_proba(features_scaled)[0]
        
        # Predict risk score
        risk_score = self.risk_regressor.predict(features_scaled)[0]
        risk_score = max(0, min(100, risk_score))  # Clamp between 0-100
        
        # Calculate confidence
        confidence = max(risk_level_proba)
        
        return {
            'risk_level': risk_level,
            'risk_score': round(risk_score, 1),
            'confidence': round(confidence * 100, 1),
            'risk_factors': self._identify_risk_factors(patient_data, incident_history),
            'recommendations': self._generate_recommendations(risk_level, risk_score, patient_data)
        }
    
    def _identify_risk_factors(self, patient_data: Dict, incident_history: List[Dict]) -> List[str]:
        """
        Identify key risk factors for the patient
        """
        factors = []
        
        # High seizure frequency
        if patient_data.get('seizure_frequency') in ['daily', 'weekly']:
            factors.append('High seizure frequency')
        
        # Recent severe incidents
        recent_incidents = [inc for inc in incident_history 
                          if (datetime.now() - datetime.fromisoformat(inc['incident_date'])).days <= 7]
        severe_count = sum(1 for inc in recent_incidents if inc.get('severity') in ['severe', 'critical'])
        if severe_count > 0:
            factors.append(f'{severe_count} recent severe incidents')
        
        # Poor medication compliance
        meds = patient_data.get('medication_regimen', '[]')
        try:
            med_list = json.loads(meds) if isinstance(meds, str) else meds
            if len(med_list) > 2:
                factors.append('Complex medication regimen')
        except:
            pass
        
        # High response times
        if patient_data.get('average_response_time', 0) > 15:
            factors.append('Slow emergency response times')
        
        # Hospital admissions
        hospital_incidents = [inc for inc in incident_history if inc.get('outcome') == 'hospitalized']
        if len(hospital_incidents) > 0:
            factors.append('Recent hospital admissions')
        
        return factors
    
    def _generate_recommendations(self, risk_level: str, risk_score: float, patient_data: Dict) -> List[str]:
        """
        Generate personalized recommendations based on risk assessment
        """
        recommendations = []
        
        if risk_level in ['High', 'Critical']:
            recommendations.extend([
                'Increase monitoring frequency',
                'Review medication compliance',
                'Consider emergency response plan',
                'Schedule immediate medical consultation'
            ])
        
        if risk_score > 70:
            recommendations.append('Implement 24/7 monitoring')
        
        if patient_data.get('average_response_time', 0) > 10:
            recommendations.append('Improve emergency response protocols')
        
        if patient_data.get('recent_seizure_count', 0) > 3:
            recommendations.append('Adjust medication dosage')
        
        # Environment-specific recommendations
        recent_incidents = patient_data.get('recent_incidents', [])
        if any(inc.get('environment') == 'public' for inc in recent_incidents):
            recommendations.append('Limit public outings during high-risk periods')
        
        return recommendations
    
    def save_model(self, filepath: str):
        """
        Save the trained model to disk
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'risk_classifier': self.risk_classifier,
            'risk_regressor': self.risk_regressor,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath: str):
        """
        Load a trained model from disk
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.risk_classifier = model_data['risk_classifier']
        self.risk_regressor = model_data['risk_regressor']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.is_trained = model_data['is_trained']

class PredictionEngine:
    """
    High-level prediction engine that integrates with Supabase
    """
    
    def __init__(self):
        self.model = EpilepsyPredictionModel()
        self.model_path = 'prediction/epilepsy_model.pkl'
        
        # Try to load existing model
        try:
            self.model.load_model(self.model_path)
        except:
            pass
    
    def train_from_supabase(self, supabase_client):
        """
        Train the model using data from Supabase
        """
        try:
            # Fetch all patients and their incidents
            patients_response = supabase_client.table('pwids').select('*').execute()
            incidents_response = supabase_client.table('incidents').select('*').execute()
            
            if not patients_response.data or not incidents_response.data:
                return {'error': 'No data available for training'}
            
            # Group incidents by patient
            incidents_by_patient = {}
            for incident in incidents_response.data:
                patient_id = incident['patient_id']
                if patient_id not in incidents_by_patient:
                    incidents_by_patient[patient_id] = []
                incidents_by_patient[patient_id].append(incident)
            
            # Prepare training data
            training_data = []
            for patient in patients_response.data:
                patient_incidents = incidents_by_patient.get(patient['patient_id'], [])
                training_data.append({
                    'profile': patient,
                    'incidents': patient_incidents
                })
            
            # Train the model
            metrics = self.model.train(training_data)
            
            # Save the trained model
            os.makedirs('prediction', exist_ok=True)
            self.model.save_model(self.model_path)
            
            return {
                'success': True,
                'metrics': metrics,
                'message': f'Model trained with {len(training_data)} patients'
            }
            
        except Exception as e:
            return {'error': f'Training failed: {str(e)}'}
    
    def predict_patient_risk(self, patient_id: str, supabase_client):
        """
        Predict risk for a specific patient
        """
        try:
            # Fetch patient data
            patient_response = supabase_client.table('pwids').select('*').eq('patient_id', patient_id).execute()
            incidents_response = supabase_client.table('incidents').select('*').eq('patient_id', patient_id).execute()
            
            if not patient_response.data:
                return {'error': 'Patient not found'}
            
            patient_data = patient_response.data[0]
            incident_history = incidents_response.data
            
            # Make prediction
            prediction = self.model.predict_risk(patient_data, incident_history)
            
            return {
                'success': True,
                'patient_id': patient_id,
                'prediction': prediction
            }
            
        except Exception as e:
            return {'error': f'Prediction failed: {str(e)}'}
    
    def update_all_risk_scores(self, supabase_client):
        """
        Update risk scores for all patients
        """
        try:
            # Fetch all patients
            patients_response = supabase_client.table('pwids').select('*').execute()
            incidents_response = supabase_client.table('incidents').select('*').execute()
            
            if not patients_response.data:
                return {'error': 'No patients found'}
            
            # Group incidents by patient
            incidents_by_patient = {}
            for incident in incidents_response.data:
                patient_id = incident['patient_id']
                if patient_id not in incidents_by_patient:
                    incidents_by_patient[patient_id] = []
                incidents_by_patient[patient_id].append(incident)
            
            updated_count = 0
            
            for patient in patients_response.data:
                patient_id = patient['patient_id']
                patient_incidents = incidents_by_patient.get(patient_id, [])
                
                # Make prediction
                prediction = self.model.predict_risk(patient, patient_incidents)
                
                if 'error' not in prediction:
                    # Update patient record
                    supabase_client.table('pwids').update({
                        'risk_status': prediction['risk_level'],
                        'risk_score': prediction['risk_score'],
                        'last_risk_update': datetime.now().isoformat()
                    }).eq('patient_id', patient_id).execute()
                    
                    updated_count += 1
            
            return {
                'success': True,
                'updated_count': updated_count,
                'message': f'Updated risk scores for {updated_count} patients'
            }
            
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}

# Global prediction engine instance
prediction_engine = PredictionEngine()
