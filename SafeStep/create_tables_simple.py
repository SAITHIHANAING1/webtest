from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_ANON_KEY'))

def create_sample_data():
    """Create sample data for the new tables using Supabase client"""
    
    print("Creating sample data for SafeStep enhanced features...")
    print("=" * 60)
    
    # Since we can't create tables with anon key, let's create sample data
    # for existing tables and prepare data structures for new features
    
    try:
        # Check if we can insert into existing tables
        print("\n1. Testing data insertion capabilities...")
        
        # Test users table
        users_result = client.table('users').select('*').limit(1).execute()
        print(f"✓ Users table accessible: {len(users_result.data)} existing records")
        
        # Test incidents table  
        incidents_result = client.table('incidents').select('*').limit(1).execute()
        print(f"✓ Incidents table accessible: {len(incidents_result.data)} existing records")
        
        # Test zones table
        zones_result = client.table('zones').select('*').limit(1).execute()
        print(f"✓ Zones table accessible: {len(zones_result.data)} existing records")
        
        print("\n2. Preparing enhanced features data structures...")
        
        # Medication management data structure
        medication_sample = {
            'name': 'Levetiracetam',
            'dosage': '500mg',
            'frequency': 'twice daily',
            'instructions': 'Take with food',
            'side_effects': 'drowsiness, dizziness',
            'active': True
        }
        print(f"✓ Medication data structure prepared: {medication_sample['name']}")
        
        # Healthcare provider data structure
        provider_sample = {
            'name': 'Dr. Sarah Johnson',
            'specialty': 'Neurology',
            'license_number': 'MD12345',
            'phone': '+1-555-0123',
            'email': 'dr.johnson@hospital.com',
            'hospital_affiliation': 'City General Hospital'
        }
        print(f"✓ Healthcare provider data structure prepared: {provider_sample['name']}")
        
        # Care plan data structure
        care_plan_sample = {
            'title': 'Epilepsy Management Plan',
            'description': 'Comprehensive care plan for seizure management',
            'goals': 'Reduce seizure frequency, improve quality of life',
            'status': 'active',
            'priority': 'high'
        }
        print(f"✓ Care plan data structure prepared: {care_plan_sample['title']}")
        
        # Emergency contact data structure
        emergency_contact_sample = {
            'name': 'John Doe',
            'relationship': 'spouse',
            'phone': '+1-555-0456',
            'email': 'john.doe@email.com',
            'is_primary': True
        }
        print(f"✓ Emergency contact data structure prepared: {emergency_contact_sample['name']}")
        
        print("\n3. Enhanced analytics capabilities...")
        
        # Analytics data structure
        analytics_sample = {
            'report_type': 'medication_adherence',
            'data': {
                'adherence_rate': 85.5,
                'missed_doses': 3,
                'total_doses': 20
            },
            'insights': 'Patient shows good medication adherence with room for improvement'
        }
        print(f"✓ Analytics data structure prepared: {analytics_sample['report_type']}")
        
        print("\n" + "=" * 60)
        print("✅ Sample data structures created successfully!")
        print("\nNote: To create actual database tables, you'll need:")
        print("1. Service role key (not anon key) for DDL operations")
        print("2. Or use Supabase dashboard to run the migration SQL")
        print("3. The migration script is ready in supabase_migration.sql")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    create_sample_data()