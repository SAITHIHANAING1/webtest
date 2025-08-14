#!/usr/bin/env python3
"""
WSGI entry point for SafeStep Flask Application
This file is used by Gunicorn and other WSGI servers for production deployment.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the Flask application
from app import app, db
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def create_default_users():
    """Create default admin and demo users if they don't exist"""
    try:
        # Import User model
        from app import User, ReportLog
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@safestep.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created successfully!")
        else:
            if not admin.is_active:
                admin.is_active = True
                db.session.commit()
                print("✅ Admin user activated!")
        
        # Create demo caregiver user
        demo_caregiver = User.query.filter_by(username='demo').first()
        if not demo_caregiver:
            demo_caregiver = User(
                username='demo',
                email='demo@safestep.com',
                password_hash=generate_password_hash('demo123'),
                first_name='Demo',
                last_name='Caregiver',
                role='caregiver',
                is_active=True
            )
            db.session.add(demo_caregiver)
            db.session.commit()
            print("✅ Default demo caregiver user created successfully!")
        else:
            if not demo_caregiver.is_active:
                demo_caregiver.is_active = True
                db.session.commit()
                print("✅ Demo caregiver user activated!")
        
        print(f"✅ Admin user exists: {admin.username} - Active: {admin.is_active}")
        print(f"✅ Demo caregiver exists: {demo_caregiver.username} - Active: {demo_caregiver.is_active}")
        
        # Create sample report logs if none exist
        existing_reports = ReportLog.query.count()
        if existing_reports == 0:
            sample_reports = [
                ReportLog(
                    user_id=admin.id,
                    report_type='PDF',
                    filename='analytics_export_2025_08_13.pdf',
                    filters_applied='{"dateRange": "30", "incidentType": "seizure"}',
                    record_count=45,
                    file_size_bytes=2048576,
                    status='completed',
                    export_timestamp=datetime.utcnow() - timedelta(hours=2)
                ),
                ReportLog(
                    user_id=admin.id,
                    report_type='CSV',
                    filename='patient_data_export.csv',
                    filters_applied='{"dateRange": "7", "location": "home"}',
                    record_count=23,
                    file_size_bytes=512000,
                    status='completed',
                    export_timestamp=datetime.utcnow() - timedelta(hours=5)
                ),
                ReportLog(
                    user_id=demo_caregiver.id,
                    report_type='JSON',
                    filename='incident_report.json',
                    filters_applied='{"severity": "high"}',
                    record_count=12,
                    file_size_bytes=256000,
                    status='failed',
                    error_message='Export timeout - data too large',
                    export_timestamp=datetime.utcnow() - timedelta(hours=1)
                )
            ]
            
            for report in sample_reports:
                db.session.add(report)
            db.session.commit()
            print("✅ Sample report logs created for testing")
            
    except Exception as e:
        print(f"❌ Default user setup failed: {e}")
        db.session.rollback()

# Initialize the application
with app.app_context():
    try:
        # Create database tables
        db.create_all()
        print("✅ Database tables created successfully")
        
        # Create default users
        create_default_users()
        
        print("✅ All models defined in app.py")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("🔄 Attempting to continue with existing database...")

print("\n✅ SafeStep Application Ready for Production")
print("=" * 50)
print("🌐 WSGI Application: Ready")
print("👤 Admin Login: admin / admin123")
print("👥 Caregiver Login: demo / demo123")
print("=" * 50)

# This is the WSGI application object that Gunicorn will use
application = app

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)