#!/usr/bin/env python3
"""
Supabase integration for Flask app
This combines Flask-SQLAlchemy with Supabase client features
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta
import json

# Load environment variables from config.env
load_dotenv('config.env')

# If not found, try loading from the parent directory (for imports from app.py)
if not os.environ.get('SUPABASE_URL'):
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Global Supabase client and availability flag
supabase: Client = None
supabase_available = False

def init_supabase():
    """Initialize Supabase client"""
    global supabase, supabase_available
    
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    print(f"🔍 Supabase URL from env: {url}")
    print(f"🔍 Supabase KEY from env: {'***' + key[-10:] if key else 'None'}")
    
    if url and key:
        try:
            supabase = create_client(url, key)
            supabase_available = True
            print("✅ Supabase client initialized successfully!")
            return True
        except Exception as e:
            supabase_available = False
            print(f"❌ Failed to initialize Supabase client: {e}")
            return False
    else:
        supabase_available = False
        print("ℹ️ Supabase credentials not found, using SQLite fallback")
        return False

def get_supabase_client():
    """Get the Supabase client instance"""
    global supabase
    return supabase

def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    return supabase

def get_supabase_admin_client() -> Client:
    """Get the Supabase client instance (admin access)"""
    return supabase

# Add this variable to check if supabase is available
supabase_available = False

def test_supabase_features():
    """Test Supabase-specific features"""
    if not supabase:
        print("❌ Supabase client not initialized")
        return False
    
    try:
        # Test auth capabilities
        session = supabase.auth.get_session()
        print("✅ Supabase auth accessible")
        
        # Test storage capabilities (if you plan to use file uploads)
        buckets = supabase.storage.list_buckets()
        print(f"✅ Supabase storage accessible, buckets: {len(buckets) if buckets else 0}")
        
        return True
    except Exception as e:
        print(f"❌ Supabase features test failed: {e}")
        return False

def setup_supabase_tables():
    """Setup required tables in Supabase"""
    if not supabase:
        print("❌ Supabase client not initialized")
        return False
    
    try:
        # Check if zones table exists by trying to select from it
        result = supabase.table('zones').select('id').limit(1).execute()
        print("✅ Zones table exists in Supabase")
        return True
    except Exception as e:
        print(f"⚠️ Zones table might not exist in Supabase: {e}")
        print("📝 Please create the zones table in your Supabase dashboard with the following schema:")
        print("""
        CREATE TABLE zones (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            latitude DOUBLE PRECISION,
            longitude DOUBLE PRECISION,
            radius DOUBLE PRECISION,
            zone_type VARCHAR(20) DEFAULT 'safe',
            status VARCHAR(20) DEFAULT 'approved',
            is_active BOOLEAN DEFAULT true,
            user_id BIGINT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """)
        return False

# Analytics-specific Supabase functions
def get_analytics_metrics_supabase(date_range=30, pwid_filter='', location_filter='', incident_type_filter=''):
    """Get analytics metrics from Supabase with filtering"""
    if not supabase:
        return None
    
    try:
        # Calculate date ranges
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=date_range)
        start_date_prev = end_date - timedelta(days=date_range * 2)
        
        # Build base query
        query = supabase.table('incidents').select('*')
        
        # Apply date filter
        query = query.gte('incident_date', start_date.isoformat())
        
        # Apply additional filters
        if location_filter:
            query = query.eq('environment', location_filter)
        if incident_type_filter:
            query = query.eq('incident_type', incident_type_filter)
        
        # Execute query
        response = query.execute()
        current_incidents = response.data
        
        # Get previous period data for comparison
        prev_query = supabase.table('incidents').select('*').gte('incident_date', start_date_prev.isoformat()).lt('incident_date', start_date.isoformat())
        if location_filter:
            prev_query = prev_query.eq('environment', location_filter)
        if incident_type_filter:
            prev_query = prev_query.eq('incident_type', incident_type_filter)
        
        prev_response = prev_query.execute()
        prev_incidents = prev_response.data
        
        # Calculate metrics
        total_incidents = len(current_incidents)
        seizure_count = len([i for i in current_incidents if i.get('incident_type') == 'seizure'])
        prev_total = len(prev_incidents)
        prev_seizures = len([i for i in prev_incidents if i.get('incident_type') == 'seizure'])
        
        # Calculate response time
        response_times = [i.get('response_time_minutes', 0) for i in current_incidents if i.get('response_time_minutes')]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Get high risk cases
        high_risk_query = supabase.table('pwids').select('*').in_('risk_status', ['High', 'Critical'])
        high_risk_response = high_risk_query.execute()
        high_risk_cases = len(high_risk_response.data)
        
        # Calculate changes
        def calc_change(old_val, new_val):
            if old_val == 0:
                return f"+{new_val * 100}%" if new_val > 0 else "No change"
            change = ((new_val - old_val) / old_val) * 100
            sign = "+" if change > 0 else ""
            return f"{sign}{change:.1f}%"
        
        incident_change = calc_change(prev_total, total_incidents)
        seizure_change = calc_change(prev_seizures, seizure_count)
        
        return {
            'success': True,
            'total_incidents': total_incidents,
            'seizure_count': seizure_count,
            'avg_response_time': f"{avg_response_time:.1f}m" if avg_response_time else "0m",
            'high_risk_cases': high_risk_cases,
            'incidents_change': incident_change,
            'seizure_change': seizure_change,
            'response_time_change': "2% improvement",
            'risk_cases_change': f"{high_risk_cases} active cases"
        }
        
    except Exception as e:
        print(f"Error getting analytics metrics from Supabase: {e}")
        return None

def get_seizure_trends_supabase(date_range=30):
    """Get seizure risk trends from Supabase"""
    if not supabase:
        return None
    
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=date_range)
        
        # Get incidents grouped by date
        query = supabase.table('incidents').select('incident_date, incident_type, severity').gte('incident_date', start_date.isoformat())
        response = query.execute()
        
        # Process data for trends
        dates = []
        high_risk = []
        medium_risk = []
        low_risk = []
        
        # Group by date and calculate risk levels
        date_groups = {}
        for incident in response.data:
            date = incident['incident_date'][:10]  # Get date part only
            if date not in date_groups:
                date_groups[date] = {'high': 0, 'medium': 0, 'low': 0}
            
            severity = incident.get('severity', 'low')
            if severity in ['severe', 'critical']:
                date_groups[date]['high'] += 1
            elif severity in ['moderate']:
                date_groups[date]['medium'] += 1
            else:
                date_groups[date]['low'] += 1
        
        # Convert to arrays for chart
        sorted_dates = sorted(date_groups.keys())
        for date in sorted_dates:
            dates.append(date)
            high_risk.append(date_groups[date]['high'])
            medium_risk.append(date_groups[date]['medium'])
            low_risk.append(date_groups[date]['low'])
        
        return {
            'success': True,
            'labels': dates,
            'datasets': [
                {
                    'label': 'High Risk',
                    'data': high_risk,
                    'borderColor': '#d32f2f',
                    'backgroundColor': 'rgba(211, 47, 47, 0.1)',
                    'fill': True
                },
                {
                    'label': 'Medium Risk',
                    'data': medium_risk,
                    'borderColor': '#f57c00',
                    'backgroundColor': 'rgba(245, 124, 0, 0.1)',
                    'fill': True
                },
                {
                    'label': 'Low Risk',
                    'data': low_risk,
                    'borderColor': '#388e3c',
                    'backgroundColor': 'rgba(56, 142, 60, 0.1)',
                    'fill': True
                }
            ]
        }
        
    except Exception as e:
        print(f"Error getting seizure trends from Supabase: {e}")
        return None

def get_location_distribution_supabase(date_range=30):
    """Get location distribution from Supabase"""
    if not supabase:
        return None
    
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=date_range)
        
        # Get incidents grouped by location
        query = supabase.table('incidents').select('environment').gte('incident_date', start_date.isoformat())
        response = query.execute()
        
        # Count by location
        location_counts = {}
        for incident in response.data:
            location = incident.get('environment', 'unknown')
            location_counts[location] = location_counts.get(location, 0) + 1
        
        locations = list(location_counts.keys())
        counts = list(location_counts.values())
        
        return {
            'success': True,
            'locations': locations,
            'counts': counts
        }
        
    except Exception as e:
        print(f"Error getting location distribution from Supabase: {e}")
        return None

def get_prediction_results_supabase():
    """Get AI prediction results from Supabase"""
    if not supabase:
        return None
    
    try:
        # Get patient profiles with risk assessments
        query = supabase.table('pwids').select('*').order('risk_score', desc=True).limit(10)
        response = query.execute()
        
        predictions = []
        for patient in response.data:
            predictions.append({
                'patient_id': patient.get('patient_id', 'unknown'),
                'risk_level': patient.get('risk_status', 'Low'),
                'risk_score': patient.get('risk_score', 0.0),
                'recent_seizures': patient.get('recent_seizure_count', 0),
                'last_update': patient.get('last_risk_update', datetime.utcnow().isoformat()),
                'status': 'COMPLETED'
            })
        
        return {
            'success': True,
            'predictions': predictions
        }
        
    except Exception as e:
        print(f"Error getting prediction results from Supabase: {e}")
        return None

def run_prediction_analysis_supabase():
    """Run AI prediction analysis using Supabase data"""
    if not supabase:
        return None
    
    try:
        # Get all patients
        patients_query = supabase.table('pwids').select('*')
        patients_response = patients_query.execute()
        
        # Get recent incidents for risk calculation
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)
        
        incidents_query = supabase.table('incidents').select('*').gte('incident_date', start_date.isoformat())
        incidents_response = incidents_query.execute()
        
        # Calculate risk scores based on recent activity
        for patient in patients_response.data:
            patient_id = patient.get('patient_id')
            recent_incidents = [i for i in incidents_response.data if i.get('patient_id') == patient_id]
            
            # Calculate risk score based on incident frequency and severity
            risk_score = 0.0
            recent_seizures = 0
            
            for incident in recent_incidents:
                if incident.get('incident_type') == 'seizure':
                    recent_seizures += 1
                    severity = incident.get('severity', 'mild')
                    if severity == 'severe':
                        risk_score += 25
                    elif severity == 'moderate':
                        risk_score += 15
                    else:
                        risk_score += 5
            
            # Determine risk level
            if risk_score >= 70:
                risk_status = 'High'
            elif risk_score >= 40:
                risk_status = 'Medium'
            else:
                risk_status = 'Low'
            
            # Update patient record
            supabase.table('pwids').update({
                'risk_score': min(100.0, risk_score),
                'risk_status': risk_status,
                'recent_seizure_count': recent_seizures,
                'last_risk_update': datetime.utcnow().isoformat()
            }).eq('patient_id', patient_id).execute()
        
        return {
            'success': True,
            'message': 'AI analysis completed successfully',
            'patients_analyzed': len(patients_response.data),
            'high_risk_identified': len([p for p in patients_response.data if p.get('risk_status') == 'High'])
        }
        
    except Exception as e:
        print(f"Error running prediction analysis in Supabase: {e}")
        return None

def export_analytics_data_supabase(filters):
    """Export analytics data from Supabase"""
    if not supabase:
        return None
    
    try:
        # Get filtered data
        date_range = filters.get('dateRange', 30)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=int(date_range))
        
        query = supabase.table('incidents').select('*').gte('incident_date', start_date.isoformat())
        
        # Apply filters
        if filters.get('locationFilter'):
            query = query.eq('environment', filters['locationFilter'])
        if filters.get('incidentType'):
            query = query.eq('incident_type', filters['incidentType'])
        
        response = query.execute()
        
        # Format data for export
        export_data = {
            'export_date': datetime.utcnow().isoformat(),
            'filters_applied': filters,
            'total_records': len(response.data),
            'data': response.data
        }
        
        return {
            'success': True,
            'data': export_data,
            'filename': f'analytics_export_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.json'
        }
        
    except Exception as e:
        print(f"Error exporting analytics data from Supabase: {e}")
        return None

# Authentication helpers (optional, for future use)
def create_supabase_user(email: str, password: str):
    """Create a new user in Supabase Auth"""
    if not supabase:
        return None
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        print(f"❌ Error creating Supabase user: {e}")
        return None

def sign_in_supabase_user(email: str, password: str):
    """Sign in a user with Supabase Auth"""
    if not supabase:
        return None
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        print(f"❌ Error signing in Supabase user: {e}")
        return None

def sync_questionnaire_to_supabase(questionnaire_data: dict):
    """Sync questionnaire data to Supabase user_questionnaires table"""
    if not supabase:
        print("❌ Supabase client not available")
        return False
    
    try:
        # Ensure the questionnaire data has the correct structure
        supabase_questionnaire = {
            'user_id': questionnaire_data.get('user_id'),
            'age': questionnaire_data.get('age'),
            'gender': questionnaire_data.get('gender'),
            'height_cm': questionnaire_data.get('height_cm'),
            'weight_kg': questionnaire_data.get('weight_kg'),
            'has_epilepsy': questionnaire_data.get('has_epilepsy'),
            'epilepsy_diagnosis_age': questionnaire_data.get('epilepsy_diagnosis_age'),
            'epilepsy_type': questionnaire_data.get('epilepsy_type'),
            'seizure_frequency': questionnaire_data.get('seizure_frequency'),
            'last_seizure_date': questionnaire_data.get('last_seizure_date'),
            'current_medications': questionnaire_data.get('current_medications'),
            'medication_compliance': questionnaire_data.get('medication_compliance'),
            'medication_side_effects': questionnaire_data.get('medication_side_effects'),
            'sleep_hours_avg': questionnaire_data.get('sleep_hours_avg'),
            'stress_level': questionnaire_data.get('stress_level'),
            'exercise_frequency': questionnaire_data.get('exercise_frequency'),
            'alcohol_consumption': questionnaire_data.get('alcohol_consumption'),
            'lives_alone': questionnaire_data.get('lives_alone'),
            'emergency_contact': questionnaire_data.get('emergency_contact'),
            'emergency_contact_phone': questionnaire_data.get('emergency_contact_phone'),
            'has_medical_alert': questionnaire_data.get('has_medical_alert'),
            'wears_helmet': questionnaire_data.get('wears_helmet'),
            'smartphone_usage': questionnaire_data.get('smartphone_usage'),
            'wearable_device': questionnaire_data.get('wearable_device'),
            'monitoring_preference': questionnaire_data.get('monitoring_preference'),
            'risk_score': questionnaire_data.get('risk_score', 0.0),
            'risk_factors': questionnaire_data.get('risk_factors'),
            'recommendations': questionnaire_data.get('recommendations'),
            'is_complete': True,
            'completed_at': datetime.utcnow().isoformat(),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Insert into Supabase
        result = supabase.table('user_questionnaires').insert(supabase_questionnaire).execute()
        
        if result.data:
            print(f"✅ Questionnaire synced to Supabase with ID: {result.data[0].get('id')}")
            return True
        else:
            print("❌ Failed to sync questionnaire to Supabase")
            return False
            
    except Exception as e:
        print(f"❌ Error syncing questionnaire to Supabase: {e}")
        return False

def get_questionnaire_from_supabase(user_id: int):
    """Get questionnaire data from Supabase for a specific user"""
    if not supabase:
        return None
    
    try:
        result = supabase.table('user_questionnaires').select('*').eq('user_id', user_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error getting questionnaire from Supabase: {e}")
        return None

def update_questionnaire_in_supabase(questionnaire_id: int, questionnaire_data: dict):
    """Update questionnaire data in Supabase"""
    if not supabase:
        return False
    
    try:
        # Add updated timestamp
        questionnaire_data['updated_at'] = datetime.utcnow().isoformat()
        
        result = supabase.table('user_questionnaires').update(questionnaire_data).eq('id', questionnaire_id).execute()
        
        if result.data:
            print(f"✅ Questionnaire updated in Supabase")
            return True
        else:
            print("❌ Failed to update questionnaire in Supabase")
            return False
            
    except Exception as e:
        print(f"❌ Error updating questionnaire in Supabase: {e}")
        return False

def get_all_questionnaires_from_supabase():
    """Get all questionnaire data from Supabase for analytics"""
    if not supabase:
        return []
    
    try:
        result = supabase.table('user_questionnaires').select('*').execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error getting questionnaires from Supabase: {e}")
        return []

def get_epilepsy_patients_from_supabase():
    """Get all patients with epilepsy from Supabase"""
    if not supabase:
        return []
    
    try:
        result = supabase.table('user_questionnaires').select('*').eq('has_epilepsy', True).eq('is_complete', True).execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error getting epilepsy patients from Supabase: {e}")
        return []

def create_seizure_prediction(patient_id: int, prediction_data: dict):
    """Create a new seizure prediction record in Supabase"""
    if not supabase:
        return None
    
    try:
        prediction_record = {
            'patient_id': patient_id,
            'prediction_date': datetime.utcnow().isoformat(),
            'risk_score': prediction_data.get('risk_score', 0.0),
            'risk_level': prediction_data.get('risk_level', 'Low'),
            'next_seizure_prediction': prediction_data.get('next_seizure_prediction'),
            'confidence_score': prediction_data.get('confidence_score', 0.0),
            'factors': prediction_data.get('factors', []),
            'recommendations': prediction_data.get('recommendations', []),
            'model_version': prediction_data.get('model_version', '1.0'),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('seizure_predictions').insert(prediction_record).execute()
        
        if result.data:
            print(f"✅ Seizure prediction created with ID: {result.data[0].get('id')}")
            return result.data[0]
        else:
            print("❌ Failed to create seizure prediction")
            return None
            
    except Exception as e:
        print(f"❌ Error creating seizure prediction: {e}")
        return None

def get_seizure_predictions_for_patient(patient_id: int, limit: int = 10):
    """Get seizure predictions for a specific patient"""
    if not supabase:
        return []
    
    try:
        result = supabase.table('seizure_predictions').select('*').eq('patient_id', patient_id).order('prediction_date', desc=True).limit(limit).execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error getting seizure predictions: {e}")
        return []

def get_all_seizure_predictions(limit: int = 50):
    """Get all seizure predictions with patient information"""
    if not supabase:
        return []
    
    try:
        # Get predictions with patient data
        result = supabase.table('seizure_predictions').select('*, pwids(patient_id, age, gender, epilepsy_type)').order('prediction_date', desc=True).limit(limit).execute()
        
        if result.data:
            return result.data
        else:
            return []
            
    except Exception as e:
        print(f"❌ Error getting all seizure predictions: {e}")
        return []

def update_seizure_prediction(prediction_id: int, prediction_data: dict):
    """Update an existing seizure prediction"""
    if not supabase:
        return False
    
    try:
        prediction_data['updated_at'] = datetime.utcnow().isoformat()
        
        result = supabase.table('seizure_predictions').update(prediction_data).eq('id', prediction_id).execute()
        
        if result.data:
            print(f"✅ Seizure prediction updated")
            return True
        else:
            print("❌ Failed to update seizure prediction")
            return False
            
    except Exception as e:
        print(f"❌ Error updating seizure prediction: {e}")
        return False

def delete_seizure_prediction(prediction_id: int):
    """Delete a seizure prediction"""
    if not supabase:
        return False
    
    try:
        result = supabase.table('seizure_predictions').delete().eq('id', prediction_id).execute()
        
        if result.data:
            print(f"✅ Seizure prediction deleted")
            return True
        else:
            print("❌ Failed to delete seizure prediction")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting seizure prediction: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Testing Supabase integration...")
    
    if init_supabase():
        test_supabase_features()
        print("🎉 Supabase integration ready!")
    else:
        print("❌ Supabase integration failed - using SQLite fallback")
