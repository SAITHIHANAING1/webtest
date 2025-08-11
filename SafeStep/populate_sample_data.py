#!/usr/bin/env python3
"""
Sample Data Population Script for SafeStep Analytics
This script populates the database with realistic sample data for testing analytics features.
"""

import random
from datetime import datetime, timedelta
from app import app, db, IncidentRecord, PwidProfile

def generate_sample_data():
    """Generate realistic sample data for analytics testing"""
    
    with app.app_context():
        print("🔄 Populating SafeStep database with sample data...")
        
        # Clear existing data
        IncidentRecord.query.delete()
        PwidProfile.query.delete()
        db.session.commit()
        
        # Sample patient data
        patients_data = [
            {'patient_id': 'PWD001', 'name': 'John Smith', 'age': 34, 'seizure_frequency': 'weekly', 'risk_status': 'High'},
            {'patient_id': 'PWD002', 'name': 'Sarah Johnson', 'age': 28, 'seizure_frequency': 'monthly', 'risk_status': 'Medium'},
            {'patient_id': 'PWD003', 'name': 'Michael Brown', 'age': 45, 'seizure_frequency': 'daily', 'risk_status': 'Critical'},
            {'patient_id': 'PWD004', 'name': 'Emily Davis', 'age': 22, 'seizure_frequency': 'rare', 'risk_status': 'Low'},
            {'patient_id': 'PWD005', 'name': 'David Wilson', 'age': 38, 'seizure_frequency': 'weekly', 'risk_status': 'High'},
            {'patient_id': 'PWD006', 'name': 'Lisa Anderson', 'age': 31, 'seizure_frequency': 'monthly', 'risk_status': 'Medium'},
            {'patient_id': 'PWD007', 'name': 'Robert Taylor', 'age': 52, 'seizure_frequency': 'daily', 'risk_status': 'Critical'},
            {'patient_id': 'PWD008', 'name': 'Jennifer Martinez', 'age': 26, 'seizure_frequency': 'rare', 'risk_status': 'Low'},
            {'patient_id': 'PWD009', 'name': 'Christopher Lee', 'age': 41, 'seizure_frequency': 'weekly', 'risk_status': 'High'},
            {'patient_id': 'PWD010', 'name': 'Amanda White', 'age': 29, 'seizure_frequency': 'monthly', 'risk_status': 'Medium'}
        ]
        
        # Create patient profiles
        for patient_data in patients_data:
            profile = PwidProfile(
                patient_id=patient_data['patient_id'],
                name=patient_data['name'],
                age=patient_data['age'],
                gender=random.choice(['Male', 'Female']),
                epilepsy_type=random.choice(['focal', 'generalized', 'combined']),
                seizure_frequency=patient_data['seizure_frequency'],
                medication_regimen=f'{{"primary": "{random.choice(["Levetiracetam", "Carbamazepine", "Valproate", "Lamotrigine"])}", "dosage": "{random.randint(100, 1000)}mg"}}',
                risk_status=patient_data['risk_status'],
                risk_score=random.uniform(10, 90),
                recent_seizure_count=random.randint(0, 10),
                average_response_time=random.uniform(5, 20),
                electrode_implant=random.choice([True, False]),
                monitoring_type=random.choice(['scalp_eeg', 'ieeg', 'utah_array']),
                hfo_burden=random.uniform(0.1, 0.8)
            )
            db.session.add(profile)
        
        db.session.commit()
        print(f"✅ Created {len(patients_data)} patient profiles")
        
        # Generate incident records over the past 90 days
        environments = ['home', 'hospital', 'public', 'work', 'school']
        incident_types = ['seizure', 'fall', 'medication', 'emergency']
        
        incidents_created = 0
        
        for days_ago in range(90):
            incident_date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Generate 0-5 incidents per day (weighted towards fewer incidents)
            num_incidents = random.choices([0, 1, 2, 3, 4, 5], weights=[20, 35, 25, 15, 4, 1])[0]
            
            for _ in range(num_incidents):
                patient = random.choice(patients_data)
                
                # Adjust incident probability based on patient risk
                if patient['risk_status'] == 'Critical' and random.random() > 0.3:
                    continue
                elif patient['risk_status'] == 'High' and random.random() > 0.5:
                    continue
                elif patient['risk_status'] == 'Medium' and random.random() > 0.7:
                    continue
                elif patient['risk_status'] == 'Low' and random.random() > 0.9:
                    continue
                
                # Generate realistic incident time (more likely during day hours)
                hour_weights = [2, 1, 1, 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 18, 16, 14, 12, 10, 8, 6, 4, 3, 2]
                hour = random.choices(range(24), weights=hour_weights)[0]
                minute = random.randint(0, 59)
                
                incident_datetime = incident_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # Weight incident types based on frequency
                incident_type = random.choices(
                    incident_types, 
                    weights=[60, 20, 15, 5]  # seizures are most common
                )[0]
                
                # Weight environments
                environment = random.choices(
                    environments,
                    weights=[50, 15, 20, 10, 5]  # home is most common
                )[0]
                
                # Generate response time (varies by environment and severity)
                base_response_time = {
                    'home': random.uniform(5, 15),
                    'hospital': random.uniform(1, 5),
                    'public': random.uniform(8, 20),
                    'work': random.uniform(6, 12),
                    'school': random.uniform(4, 10)
                }[environment]
                
                # Adjust for patient risk level
                risk_multiplier = {
                    'Critical': 0.8,  # faster response for critical patients
                    'High': 0.9,
                    'Medium': 1.0,
                    'Low': 1.2
                }[patient['risk_status']]
                
                response_time = max(1, base_response_time * risk_multiplier + random.uniform(-2, 2))
                
                incident = IncidentRecord(
                    patient_id=patient['patient_id'],
                    age=patient['age'],
                    gender=random.choice(['M', 'F']),
                    incident_type=incident_type,
                    incident_date=incident_datetime,
                    severity=random.choice(['mild', 'moderate', 'severe', 'critical']),
                    duration_seconds=random.randint(30, 300) if incident_type == 'seizure' else None,
                    seizure_type=random.choice(['focal', 'generalized', 'absence', 'tonic-clonic']) if incident_type == 'seizure' else None,
                    consciousness_state=random.choice(['awake', 'asleep', 'impaired']) if incident_type == 'seizure' else None,
                    location=f"Sample location at {environment}",
                    environment=environment,
                    triggers='["stress", "sleep_deprivation", "medication_missed"]',
                    eeg_recorded=random.choice([True, False]),
                    sampling_rate=random.choice([256, 500, 1000]) if random.choice([True, False]) else None,
                    electrode_count=random.choice([16, 32, 64, 128]) if random.choice([True, False]) else None,
                    hfo_detected=random.choice([True, False]),
                    response_time_minutes=round(response_time, 1),
                    intervention_type=random.choice(['medication', 'emergency_services', 'observation', 'hospitalization']),
                    outcome=random.choice(['resolved', 'hospitalized', 'ongoing'])
                )
                
                db.session.add(incident)
                incidents_created += 1
        
        db.session.commit()
        print(f"✅ Created {incidents_created} incident records")
        
        # Verify data creation
        total_patients = PwidProfile.query.count()
        total_incidents = IncidentRecord.query.count()
        
        print(f"\n📊 Database Summary:")
        print(f"   Patients: {total_patients}")
        print(f"   Incidents: {total_incidents}")
        
        # Show sample statistics
        seizure_count = IncidentRecord.query.filter_by(incident_type='seizure').count()
        high_risk_count = PwidProfile.query.filter(PwidProfile.risk_status.in_(['High', 'Critical'])).count()
        
        print(f"   Seizure Events: {seizure_count}")
        print(f"   High-Risk Patients: {high_risk_count}")
        
        # Show environment distribution
        print(f"\n🏠 Environment Distribution:")
        for env in environments:
            count = IncidentRecord.query.filter_by(environment=env).count()
            print(f"   {env.title()}: {count}")
        
        print(f"\n✅ Sample data population completed successfully!")
        print(f"🌐 Analytics dashboard should now display data at: http://localhost:5000")

if __name__ == '__main__':
    generate_sample_data()