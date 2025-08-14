#!/usr/bin/env python3
"""
Check Supabase database schema and available data for analytics integration
"""

from app import app
from supabase_integration import get_supabase_client, supabase_available
import json
from datetime import datetime

def check_supabase_schema():
    """Check what tables and data are available in Supabase"""
    
    with app.app_context():
        print("🔍 Checking Supabase Database Schema and Data...\n")
        
        if not supabase_available:
            print("❌ Supabase is not available. Please check your configuration.")
            return
        
        supabase = get_supabase_client()
        if not supabase:
            print("❌ Could not get Supabase client")
            return
        
        # List of expected tables for analytics
        expected_tables = [
            'pwids',           # Patient profiles
            'incidents',       # Incident records
            'seizure_predictions',  # AI predictions
            'zones',           # GPS zones
            'users',           # User accounts
            'training_modules', # Training content
            'certificates',    # Training certificates
            'user_questionnaires'  # Risk assessments
        ]
        
        print("📊 Checking Tables and Data:")
        print("=" * 50)
        
        for table_name in expected_tables:
            try:
                # Try to get table info and sample data
                result = supabase.table(table_name).select('*').limit(5).execute()
                
                if result.data is not None:
                    count_result = supabase.table(table_name).select('*', count='exact').execute()
                    total_count = count_result.count if hasattr(count_result, 'count') else len(result.data)
                    
                    print(f"✅ {table_name}: {total_count} records")
                    
                    if result.data:
                        # Show sample record structure
                        sample = result.data[0]
                        print(f"   📋 Sample fields: {list(sample.keys())}")
                        
                        # Show some sample data for key fields
                        if table_name == 'pwids':
                            print(f"   👤 Sample patient: ID={sample.get('patient_id', 'N/A')}, Age={sample.get('age', 'N/A')}, Risk={sample.get('risk_status', 'N/A')}")
                        elif table_name == 'incidents':
                            print(f"   🚨 Sample incident: Type={sample.get('incident_type', 'N/A')}, Date={sample.get('incident_date', 'N/A')}, Severity={sample.get('severity', 'N/A')}")
                        elif table_name == 'seizure_predictions':
                            print(f"   🧠 Sample prediction: Risk={sample.get('risk_score', 'N/A')}, Level={sample.get('risk_level', 'N/A')}")
                    else:
                        print(f"   ℹ️ Table exists but is empty")
                else:
                    print(f"❌ {table_name}: No data or access denied")
                    
            except Exception as e:
                print(f"❌ {table_name}: Error - {str(e)}")
            
            print()
        
        # Check for analytics-specific data requirements
        print("\n🎯 Analytics Data Requirements Check:")
        print("=" * 50)
        
        # Check for recent incidents (needed for trends)
        try:
            recent_incidents = supabase.table('incidents').select('*').gte('incident_date', '2024-01-01').execute()
            if recent_incidents.data:
                print(f"✅ Recent incidents: {len(recent_incidents.data)} records since 2024")
                
                # Check incident types
                incident_types = set()
                locations = set()
                severities = set()
                
                for incident in recent_incidents.data:
                    if incident.get('incident_type'):
                        incident_types.add(incident['incident_type'])
                    if incident.get('environment'):
                        locations.add(incident['environment'])
                    if incident.get('severity'):
                        severities.add(incident['severity'])
                
                print(f"   📊 Incident types: {list(incident_types)}")
                print(f"   📍 Locations: {list(locations)}")
                print(f"   ⚠️ Severities: {list(severities)}")
            else:
                print("❌ No recent incidents found - analytics will show empty charts")
        except Exception as e:
            print(f"❌ Could not check recent incidents: {e}")
        
        # Check for patients with risk data
        try:
            risk_patients = supabase.table('pwids').select('risk_status, risk_score').execute()
            if risk_patients.data:
                risk_levels = {}
                for patient in risk_patients.data:
                    risk_level = patient.get('risk_status', 'Unknown')
                    risk_levels[risk_level] = risk_levels.get(risk_level, 0) + 1
                
                print(f"✅ Patient risk distribution: {risk_levels}")
            else:
                print("❌ No patient risk data found")
        except Exception as e:
            print(f"❌ Could not check patient risk data: {e}")
        
        # Check for prediction data
        try:
            predictions = supabase.table('seizure_predictions').select('*').limit(10).execute()
            if predictions.data:
                print(f"✅ AI predictions available: {len(predictions.data)} recent predictions")
            else:
                print("⚠️ No AI predictions found - prediction charts will be empty")
        except Exception as e:
            print(f"❌ Could not check prediction data: {e}")
        
        print("\n💡 Recommendations:")
        print("=" * 50)
        print("1. If tables are missing, create them in your Supabase dashboard")
        print("2. If tables are empty, run the data population scripts")
        print("3. For analytics to work properly, you need:")
        print("   - At least 10-20 incident records")
        print("   - Patient profiles with risk assessments")
        print("   - Recent data (within last 30-90 days)")
        print("\n🔗 Supabase Dashboard: https://app.supabase.com/project/YOUR_PROJECT_ID")

if __name__ == '__main__':
    check_supabase_schema()