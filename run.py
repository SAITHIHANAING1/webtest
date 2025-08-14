"""
Simple startup script for Railway deployment
No shebang lines or shell commands to avoid Docker issues
"""

import os
import sys

# Import the Flask application
from app import app, db
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def create_default_users():
    """Create default admin and demo users if they don't exist"""
    try:
        # Import User model
        from app import User
        
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
            
    except Exception as e:
        print(f"❌ Default user setup failed: {e}")
        db.session.rollback()

if __name__ == "__main__":
    # Initialize the application
    with app.app_context():
        try:
            # Create database tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create default users
            create_default_users()
            
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            print("🔄 Attempting to continue with existing database...")

    print("\n✅ SafeStep Application Starting")
    print("=" * 50)
    print("👤 Admin Login: admin / admin123")
    print("👥 Caregiver Login: demo / demo123")
    print("=" * 50)

    # Start the Flask application
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
