#!/usr/bin/env python3
"""
SafeStep Enhanced Supabase Integration Module
Provides comprehensive CRUD operations for all SafeStep features using Supabase.

This module implements:
- Medication Management
- Healthcare Provider Management
- Care Plan Management
- Emergency Response System
- Enhanced Analytics
- Real-time Features
"""

import os
import json
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from supabase import create_client, Client
from postgrest.exceptions import APIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseEnhanced:
    """Enhanced Supabase client for SafeStep application"""
    
    def __init__(self):
        """Initialize Supabase client with environment variables"""
        self.url = os.getenv('SUPABASE_URL')
        # Check for both SUPABASE_ANON_KEY and SUPABASE_KEY for compatibility
        self.key = os.getenv('SUPABASE_ANON_KEY') or os.getenv('SUPABASE_KEY')
        self.service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY (or SUPABASE_KEY) must be set")
        
        self.client: Client = create_client(self.url, self.key)
        
        # Service client for admin operations
        if self.service_key:
            self.service_client: Client = create_client(self.url, self.service_key)
        else:
            self.service_client = self.client
            logger.warning("Service key not provided, using anon key for all operations")
    
    def _handle_error(self, operation: str, error: Exception) -> Dict[str, Any]:
        """Handle and log errors consistently"""
        error_msg = f"Error in {operation}: {str(error)}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg, 'data': None}
    
    def _format_response(self, data: Any, success: bool = True, message: str = None) -> Dict[str, Any]:
        """Format consistent API responses"""
        return {
            'success': success,
            'data': data,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }

    # ============================================================================
    # MEDICATION MANAGEMENT
    # ============================================================================
    
    def create_medication(self, medication_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new medication record"""
        try:
            # Validate required fields
            required_fields = ['patient_id', 'medication_name', 'dosage', 'frequency', 'start_date']
            for field in required_fields:
                if field not in medication_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('medications').insert(medication_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Medication created successfully")
        except Exception as e:
            return self._handle_error('create_medication', e)
    
    def get_patient_medications(self, patient_id: str, active_only: bool = True) -> Dict[str, Any]:
        """Get all medications for a patient"""
        try:
            query = self.client.table('medications').select('*').eq('patient_id', patient_id)
            if active_only:
                query = query.eq('is_active', True)
            
            result = query.order('created_at', desc=True).execute()
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} medications")
        except Exception as e:
            return self._handle_error('get_patient_medications', e)
    
    def update_medication(self, medication_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a medication record"""
        try:
            # Add updated_at timestamp
            update_data['updated_at'] = datetime.utcnow().isoformat()
            
            result = self.client.table('medications').update(update_data).eq('id', medication_id).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Medication updated successfully")
        except Exception as e:
            return self._handle_error('update_medication', e)
    
    def log_medication_taken(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log when a medication is taken"""
        try:
            required_fields = ['medication_id', 'taken_at']
            for field in required_fields:
                if field not in log_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('medication_logs').insert(log_data).execute()
            
            # Update medication adherence score
            self._update_medication_adherence(log_data['medication_id'])
            
            return self._format_response(result.data[0] if result.data else None, True, "Medication log created successfully")
        except Exception as e:
            return self._handle_error('log_medication_taken', e)
    
    def get_medication_adherence(self, patient_id: str, days: int = 30) -> Dict[str, Any]:
        """Calculate medication adherence for a patient"""
        try:
            # Call the database function
            start_date = (datetime.now() - timedelta(days=days)).date()
            end_date = datetime.now().date()
            
            result = self.client.rpc('calculate_medication_adherence', {
                'patient_uuid': patient_id,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }).execute()
            
            adherence_score = result.data if result.data is not None else 0.0
            return self._format_response({
                'patient_id': patient_id,
                'adherence_score': adherence_score,
                'period_days': days,
                'calculated_at': datetime.utcnow().isoformat()
            }, True, f"Adherence calculated: {adherence_score}%")
        except Exception as e:
            return self._handle_error('get_medication_adherence', e)
    
    def _update_medication_adherence(self, medication_id: str):
        """Internal method to update medication adherence score"""
        try:
            # Get medication details
            med_result = self.client.table('medications').select('patient_id').eq('id', medication_id).execute()
            if not med_result.data:
                return
            
            patient_id = med_result.data[0]['patient_id']
            adherence_data = self.get_medication_adherence(patient_id)
            
            if adherence_data['success']:
                adherence_score = adherence_data['data']['adherence_score']
                self.client.table('medications').update({
                    'adherence_score': adherence_score,
                    'updated_at': datetime.utcnow().isoformat()
                }).eq('id', medication_id).execute()
        except Exception as e:
            logger.error(f"Error updating medication adherence: {e}")

    # ============================================================================
    # HEALTHCARE PROVIDER MANAGEMENT
    # ============================================================================
    
    def create_healthcare_provider(self, provider_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new healthcare provider"""
        try:
            required_fields = ['name', 'specialty']
            for field in required_fields:
                if field not in provider_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('healthcare_providers').insert(provider_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Healthcare provider created successfully")
        except Exception as e:
            return self._handle_error('create_healthcare_provider', e)
    
    def get_healthcare_providers(self, specialty: str = None, active_only: bool = True) -> Dict[str, Any]:
        """Get healthcare providers with optional filtering"""
        try:
            query = self.client.table('healthcare_providers').select('*')
            
            if specialty:
                query = query.eq('specialty', specialty)
            if active_only:
                query = query.eq('is_active', True)
            
            result = query.order('name').execute()
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} providers")
        except Exception as e:
            return self._handle_error('get_healthcare_providers', e)
    
    def assign_provider_to_patient(self, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assign a healthcare provider to a patient"""
        try:
            required_fields = ['patient_id', 'provider_id', 'relationship_type', 'assigned_date']
            for field in required_fields:
                if field not in assignment_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('patient_provider_assignments').insert(assignment_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Provider assigned successfully")
        except Exception as e:
            return self._handle_error('assign_provider_to_patient', e)
    
    def get_patient_providers(self, patient_id: str) -> Dict[str, Any]:
        """Get all healthcare providers for a patient"""
        try:
            result = self.client.table('patient_provider_assignments').select(
                '*, healthcare_providers(*)'
            ).eq('patient_id', patient_id).eq('is_active', True).execute()
            
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} provider assignments")
        except Exception as e:
            return self._handle_error('get_patient_providers', e)

    # ============================================================================
    # CARE PLAN MANAGEMENT
    # ============================================================================
    
    def create_care_plan(self, care_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new care plan"""
        try:
            required_fields = ['patient_id', 'plan_name', 'start_date']
            for field in required_fields:
                if field not in care_plan_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('care_plans').insert(care_plan_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Care plan created successfully")
        except Exception as e:
            return self._handle_error('create_care_plan', e)
    
    def get_patient_care_plans(self, patient_id: str, status: str = None) -> Dict[str, Any]:
        """Get care plans for a patient"""
        try:
            query = self.client.table('care_plans').select('*').eq('patient_id', patient_id)
            
            if status:
                query = query.eq('status', status)
            
            result = query.order('created_at', desc=True).execute()
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} care plans")
        except Exception as e:
            return self._handle_error('get_patient_care_plans', e)
    
    def create_care_plan_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new care plan task"""
        try:
            required_fields = ['care_plan_id', 'task_name']
            for field in required_fields:
                if field not in task_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('care_plan_tasks').insert(task_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Care plan task created successfully")
        except Exception as e:
            return self._handle_error('create_care_plan_task', e)
    
    def update_task_status(self, task_id: str, status: str, completion_notes: str = None) -> Dict[str, Any]:
        """Update the status of a care plan task"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.utcnow().isoformat()
            }
            
            if status == 'completed':
                update_data['completed_at'] = datetime.utcnow().isoformat()
                if completion_notes:
                    update_data['completion_notes'] = completion_notes
            
            result = self.client.table('care_plan_tasks').update(update_data).eq('id', task_id).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Task status updated successfully")
        except Exception as e:
            return self._handle_error('update_task_status', e)
    
    def get_care_plan_progress(self, care_plan_id: str) -> Dict[str, Any]:
        """Get progress summary for a care plan"""
        try:
            result = self.client.table('care_plan_progress_view').select('*').eq('care_plan_id', care_plan_id).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Care plan progress retrieved")
        except Exception as e:
            return self._handle_error('get_care_plan_progress', e)

    # ============================================================================
    # EMERGENCY RESPONSE SYSTEM
    # ============================================================================
    
    def create_emergency_contact(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new emergency contact"""
        try:
            required_fields = ['patient_id', 'name', 'relationship', 'phone_primary', 'priority_order']
            for field in required_fields:
                if field not in contact_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('emergency_contacts').insert(contact_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Emergency contact created successfully")
        except Exception as e:
            return self._handle_error('create_emergency_contact', e)
    
    def get_patient_emergency_contacts(self, patient_id: str) -> Dict[str, Any]:
        """Get emergency contacts for a patient"""
        try:
            result = self.client.table('emergency_contacts').select('*').eq(
                'patient_id', patient_id
            ).order('priority_order').execute()
            
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} emergency contacts")
        except Exception as e:
            return self._handle_error('get_patient_emergency_contacts', e)
    
    def create_emergency_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new emergency alert"""
        try:
            required_fields = ['patient_id', 'alert_type', 'severity', 'message']
            for field in required_fields:
                if field not in alert_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('emergency_alerts').insert(alert_data).execute()
            
            # Trigger real-time notification
            self._trigger_emergency_notification(result.data[0] if result.data else None)
            
            return self._format_response(result.data[0] if result.data else None, True, "Emergency alert created successfully")
        except Exception as e:
            return self._handle_error('create_emergency_alert', e)
    
    def resolve_emergency_alert(self, alert_id: str, resolved_by: str, resolution_notes: str = None) -> Dict[str, Any]:
        """Resolve an emergency alert"""
        try:
            update_data = {
                'resolved_at': datetime.utcnow().isoformat(),
                'resolved_by': resolved_by,
                'resolution_notes': resolution_notes
            }
            
            result = self.client.table('emergency_alerts').update(update_data).eq('id', alert_id).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Emergency alert resolved successfully")
        except Exception as e:
            return self._handle_error('resolve_emergency_alert', e)
    
    def get_unresolved_alerts(self, patient_id: str = None) -> Dict[str, Any]:
        """Get unresolved emergency alerts"""
        try:
            query = self.client.table('emergency_alerts').select('*').is_('resolved_at', 'null')
            
            if patient_id:
                query = query.eq('patient_id', patient_id)
            
            result = query.order('created_at', desc=True).execute()
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} unresolved alerts")
        except Exception as e:
            return self._handle_error('get_unresolved_alerts', e)
    
    def _trigger_emergency_notification(self, alert_data: Dict[str, Any]):
        """Trigger real-time emergency notification"""
        try:
            if not alert_data:
                return
            
            # Publish to real-time channel
            channel_name = f"emergency_alerts:{alert_data['patient_id']}"
            self.client.realtime.channel(channel_name).send({
                'type': 'emergency_alert',
                'payload': alert_data
            })
            
            logger.info(f"Emergency notification sent for alert {alert_data['id']}")
        except Exception as e:
            logger.error(f"Error sending emergency notification: {e}")

    # ============================================================================
    # ENHANCED ANALYTICS
    # ============================================================================
    
    def get_patient_risk_summary(self, patient_id: str) -> Dict[str, Any]:
        """Get comprehensive risk summary for a patient"""
        try:
            result = self.client.rpc('get_patient_risk_summary', {
                'patient_uuid': patient_id
            }).execute()
            
            return self._format_response(result.data, True, "Patient risk summary retrieved")
        except Exception as e:
            return self._handle_error('get_patient_risk_summary', e)
    
    def get_patient_dashboard_data(self, patient_id: str = None) -> Dict[str, Any]:
        """Get dashboard data for patients"""
        try:
            query = self.client.table('patient_dashboard_view').select('*')
            
            if patient_id:
                query = query.eq('id', patient_id)
            
            result = query.execute()
            return self._format_response(result.data, True, "Dashboard data retrieved")
        except Exception as e:
            return self._handle_error('get_patient_dashboard_data', e)
    
    def create_prediction_result(self, prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store AI prediction results"""
        try:
            required_fields = ['patient_id', 'model_version', 'risk_score', 'confidence_level']
            for field in required_fields:
                if field not in prediction_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('prediction_results').insert(prediction_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Prediction result stored successfully")
        except Exception as e:
            return self._handle_error('create_prediction_result', e)
    
    def get_latest_predictions(self, patient_id: str = None, limit: int = 10) -> Dict[str, Any]:
        """Get latest prediction results"""
        try:
            query = self.client.table('prediction_results').select('*')
            
            if patient_id:
                query = query.eq('patient_id', patient_id)
            
            result = query.order('prediction_date', desc=True).limit(limit).execute()
            return self._format_response(result.data, True, f"Retrieved {len(result.data)} predictions")
        except Exception as e:
            return self._handle_error('get_latest_predictions', e)
    
    def log_feature_usage(self, usage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log feature usage for analytics"""
        try:
            required_fields = ['user_id', 'feature_name', 'action']
            for field in required_fields:
                if field not in usage_data:
                    return self._format_response(None, False, f"Missing required field: {field}")
            
            result = self.client.table('feature_usage_logs').insert(usage_data).execute()
            return self._format_response(result.data[0] if result.data else None, True, "Feature usage logged")
        except Exception as e:
            return self._handle_error('log_feature_usage', e)

    # ============================================================================
    # REAL-TIME FEATURES
    # ============================================================================
    
    def subscribe_to_patient_updates(self, patient_id: str, callback_function):
        """Subscribe to real-time updates for a patient"""
        try:
            channel = self.client.realtime.channel(f"patient_updates:{patient_id}")
            
            # Subscribe to various table changes
            channel.on('postgres_changes', {
                'event': '*',
                'schema': 'public',
                'table': 'incidents',
                'filter': f'patient_id=eq.{patient_id}'
            }, callback_function)
            
            channel.on('postgres_changes', {
                'event': '*',
                'schema': 'public',
                'table': 'emergency_alerts',
                'filter': f'patient_id=eq.{patient_id}'
            }, callback_function)
            
            channel.subscribe()
            return channel
        except Exception as e:
            logger.error(f"Error subscribing to patient updates: {e}")
            return None
    
    def subscribe_to_emergency_alerts(self, callback_function):
        """Subscribe to real-time emergency alerts"""
        try:
            channel = self.client.realtime.channel('emergency_alerts')
            
            channel.on('postgres_changes', {
                'event': 'INSERT',
                'schema': 'public',
                'table': 'emergency_alerts'
            }, callback_function)
            
            channel.subscribe()
            return channel
        except Exception as e:
            logger.error(f"Error subscribing to emergency alerts: {e}")
            return None

    # ============================================================================
    # BATCH OPERATIONS
    # ============================================================================
    
    def batch_update_medication_adherence(self) -> Dict[str, Any]:
        """Update medication adherence scores for all active medications"""
        try:
            result = self.service_client.rpc('update_medication_adherence_scores').execute()
            updated_count = result.data if result.data is not None else 0
            
            return self._format_response({
                'updated_count': updated_count
            }, True, f"Updated adherence scores for {updated_count} medications")
        except Exception as e:
            return self._handle_error('batch_update_medication_adherence', e)
    
    def bulk_insert(self, table_name: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bulk insert records into a table"""
        try:
            if not records:
                return self._format_response([], True, "No records to insert")
            
            result = self.client.table(table_name).insert(records).execute()
            return self._format_response(result.data, True, f"Inserted {len(result.data)} records")
        except Exception as e:
            return self._handle_error('bulk_insert', e)

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def health_check(self) -> Dict[str, Any]:
        """Check Supabase connection health"""
        try:
            # Simple query to test connection
            result = self.client.table('pwids').select('id').limit(1).execute()
            
            return self._format_response({
                'status': 'healthy',
                'connection': 'active',
                'timestamp': datetime.utcnow().isoformat()
            }, True, "Supabase connection is healthy")
        except Exception as e:
            return self._handle_error('health_check', e)
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Get basic statistics for a table"""
        try:
            # Get total count
            count_result = self.client.table(table_name).select('id', count='exact').execute()
            total_count = count_result.count if hasattr(count_result, 'count') else 0
            
            # Get recent records
            recent_result = self.client.table(table_name).select('created_at').order(
                'created_at', desc=True
            ).limit(1).execute()
            
            last_created = None
            if recent_result.data:
                last_created = recent_result.data[0].get('created_at')
            
            return self._format_response({
                'table_name': table_name,
                'total_records': total_count,
                'last_created': last_created
            }, True, f"Statistics for {table_name} retrieved")
        except Exception as e:
            return self._handle_error('get_table_stats', e)

# Global instance
supabase_enhanced = None

def get_supabase_enhanced() -> SupabaseEnhanced:
    """Get or create the global Supabase enhanced instance"""
    global supabase_enhanced
    if supabase_enhanced is None:
        supabase_enhanced = SupabaseEnhanced()
    return supabase_enhanced

# Example usage and testing
if __name__ == "__main__":
    # Initialize client
    sb = get_supabase_enhanced()
    
    # Test connection
    health = sb.health_check()
    print(f"Health check: {health}")
    
    # Example: Create a medication
    medication_data = {
        'patient_id': 'example-patient-id',
        'medication_name': 'Levetiracetam',
        'dosage': '500mg',
        'frequency': 'twice daily',
        'start_date': '2024-01-01',
        'prescribing_doctor': 'Dr. Smith'
    }
    
    # result = sb.create_medication(medication_data)
    # print(f"Create medication result: {result}")
    
    print("Supabase Enhanced module loaded successfully!")