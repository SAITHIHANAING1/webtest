#!/usr/bin/env python3
"""
Deployment script for SafeStep on Render
This script initializes the database and creates sample data
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Create and configure the Flask app for deployment"""
    from app import app, db
    
    # Set deployment environment variables
    os.environ.setdefault('FLASK_ENV', 'production')
    os.environ.setdefault('SECRET_KEY', os.urandom(24).hex())
    
    with app.app_context():
        print("🔄 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create admin user if it doesn't exist
        from app import User, generate_password_hash
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@safestep.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                role='admin',
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ Admin user created (username: admin, password: admin123)")
        
        print("🚀 Deployment setup complete!")
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
