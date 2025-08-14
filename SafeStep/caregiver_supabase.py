#!/usr/bin/env python3
"""
Caregiver Dashboard Supabase Integration
Handles data fetching for caregiver dashboard and related pages
"""

from supabase_integration import get_supabase_client, init_supabase
from datetime import datetime, timedelta
import json

def get_caregiver_dashboard_data(user_id):
    """Get comprehensive dashboard data for caregiver from Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return None
            
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        dashboard_data = {}
        
        # Get recent seizure sessions
        try:
            sessions_response = supabase.table('seizure_session').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
            dashboard_data['recent_sessions'] = sessions_response.data or []
        except Exception as e:
            print(f"Error fetching sessions: {e}")
            dashboard_data['recent_sessions'] = []
        
        # Get active safety zones count
        try:
            zones_response = supabase.table('zones').select('id').eq('is_active', True).eq('status', 'approved').execute()
            dashboard_data['active_zones'] = len(zones_response.data or [])
        except Exception as e:
            print(f"Error fetching zones: {e}")
            dashboard_data['active_zones'] = 0
        
        # Get training progress
        try:
            progress_response = supabase.table('training_progress').select('*').eq('user_id', user_id).eq('completed', True).execute()
            dashboard_data['completed_modules'] = len(progress_response.data or [])
            
            # Get total modules for completion percentage
            modules_response = supabase.table('training_modules').select('id').eq('is_active', True).execute()
            total_modules = len(modules_response.data or [])
            dashboard_data['total_modules'] = total_modules
            dashboard_data['training_completion_percentage'] = (dashboard_data['completed_modules'] / max(total_modules, 1)) * 100
        except Exception as e:
            print(f"Error fetching training progress: {e}")
            dashboard_data['completed_modules'] = 0
            dashboard_data['total_modules'] = 0
            dashboard_data['training_completion_percentage'] = 0
        
        # Get recent incidents/alerts
        try:
            incidents_response = supabase.table('incidents').select('*').order('incident_date', desc=True).limit(3).execute()
            dashboard_data['recent_incidents'] = incidents_response.data or []
        except Exception as e:
            print(f"Error fetching incidents: {e}")
            dashboard_data['recent_incidents'] = []
        
        # Get patient profiles (PWIDs)
        try:
            patients_response = supabase.table('pwids').select('*').execute()
            dashboard_data['active_patients'] = patients_response.data or []
            dashboard_data['total_patients'] = len(dashboard_data['active_patients'])
        except Exception as e:
            print(f"Error fetching patients: {e}")
            dashboard_data['active_patients'] = []
            dashboard_data['total_patients'] = 0
        
        # Calculate health metrics
        try:
            # Get prediction data for risk assessment
            predictions_response = supabase.table('prediction_job').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(10).execute()
            predictions = predictions_response.data or []
            
            if predictions:
                # Calculate average risk score
                risk_scores = [p.get('risk_score', 0) for p in predictions if p.get('risk_score') is not None]
                dashboard_data['average_risk_score'] = sum(risk_scores) / len(risk_scores) if risk_scores else 0
                
                # Get latest prediction
                dashboard_data['latest_prediction'] = predictions[0] if predictions else None
            else:
                dashboard_data['average_risk_score'] = 0
                dashboard_data['latest_prediction'] = None
                
        except Exception as e:
            print(f"Error fetching predictions: {e}")
            dashboard_data['average_risk_score'] = 0
            dashboard_data['latest_prediction'] = None
        
        # Get support tickets
        try:
            tickets_response = supabase.table('support_ticket').select('*').eq('user_id', user_id).eq('status', 'open').execute()
            dashboard_data['open_tickets'] = len(tickets_response.data or [])
        except Exception as e:
            print(f"Error fetching tickets: {e}")
            dashboard_data['open_tickets'] = 0
        
        print(f"✅ Dashboard data loaded for user {user_id}")
        return dashboard_data
        
    except Exception as e:
        print(f"❌ Error loading dashboard data: {e}")
        return None

def get_recent_activities(user_id, limit=10):
    """Get recent activities for activity feed"""
    try:
        if not init_supabase():
            return []
            
        supabase = get_supabase_client()
        if not supabase:
            return []
        
        activities = []
        
        # Get recent sessions
        sessions = supabase.table('seizure_session').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(3).execute()
        for session in (sessions.data or []):
            activities.append({
                'type': 'session',
                'title': 'Monitoring Session',
                'description': f"Severity: {session.get('severity', 'Unknown')}",
                'timestamp': session.get('created_at'),
                'icon': 'fas fa-heartbeat',
                'color': 'danger' if session.get('severity') == 'severe' else 'warning' if session.get('severity') == 'moderate' else 'info'
            })
        
        # Get recent training completions
        progress = supabase.table('training_progress').select('*, training_module(title)').eq('user_id', user_id).eq('completed', True).order('completed_at', desc=True).limit(3).execute()
        for prog in (progress.data or []):
            module_title = prog.get('training_module', {}).get('title', 'Unknown Module') if prog.get('training_module') else 'Training Module'
            activities.append({
                'type': 'training',
                'title': 'Training Completed',
                'description': f"Completed: {module_title}",
                'timestamp': prog.get('completed_at'),
                'icon': 'fas fa-graduation-cap',
                'color': 'success'
            })
        
        # Get recent incidents
        incidents = supabase.table('incidents').select('*').order('incident_date', desc=True).limit(2).execute()
        for incident in (incidents.data or []):
            activities.append({
                'type': 'incident',
                'title': 'Incident Recorded',
                'description': f"Type: {incident.get('incident_type', 'Unknown')}",
                'timestamp': incident.get('incident_date'),
                'icon': 'fas fa-exclamation-triangle',
                'color': 'warning'
            })
        
        # Sort by timestamp and limit
        activities.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return activities[:limit]
        
    except Exception as e:
        print(f"❌ Error loading recent activities: {e}")
        return []

def get_patient_status(patient_id):
    """Get current status of a specific patient"""
    try:
        if not init_supabase():
            return None
            
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Get patient info
        patient_response = supabase.table('pwids').select('*').eq('patient_id', patient_id).single().execute()
        patient = patient_response.data
        
        if not patient:
            return None
        
        # Get latest location
        location_response = supabase.table('location_tracking').select('*').eq('patient_id', patient_id).order('timestamp', desc=True).limit(1).execute()
        latest_location = location_response.data[0] if location_response.data else None
        
        # Get recent incidents
        incidents_response = supabase.table('incidents').select('*').eq('patient_id', patient_id).order('incident_date', desc=True).limit(3).execute()
        recent_incidents = incidents_response.data or []
        
        return {
            'patient': patient,
            'latest_location': latest_location,
            'recent_incidents': recent_incidents,
            'status': 'active' if patient.get('is_active') else 'inactive'
        }
        
    except Exception as e:
        print(f"❌ Error loading patient status: {e}")
        return None

if __name__ == "__main__":
    # Test the dashboard data functions
    print("🧪 Testing Caregiver Dashboard Supabase Integration...")
    
    # Test with user ID 1 (or 2 if you have data for that user)
    test_user_id = 2
    
    dashboard_data = get_caregiver_dashboard_data(test_user_id)
    if dashboard_data:
        print(f"✅ Dashboard data loaded:")
        print(f"   - Recent sessions: {len(dashboard_data.get('recent_sessions', []))}")
        print(f"   - Active zones: {dashboard_data.get('active_zones', 0)}")
        print(f"   - Completed modules: {dashboard_data.get('completed_modules', 0)}")
        print(f"   - Total patients: {dashboard_data.get('total_patients', 0)}")
    else:
        print("❌ Failed to load dashboard data")
    
    activities = get_recent_activities(test_user_id)
    print(f"✅ Recent activities loaded: {len(activities)} items")
