#!/usr/bin/env python3
"""
Fresh database setup with correct schema
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import app, db, User, TrainingModule
from werkzeug.security import generate_password_hash

def setup_fresh_database():
    """Setup a completely fresh database"""
    print("🗄️ Setting up fresh database...")
    
    with app.app_context():
        # Drop all tables and recreate them
        print("🔄 Dropping all existing tables...")
        db.drop_all()
        
        print("🔄 Creating fresh tables with updated schema...")
        db.create_all()
        
        # Verify the TrainingModule table structure
        print("🔍 Verifying TrainingModule table structure...")
        try:
            # Try to create a test module to verify all columns exist
            test_module = TrainingModule(
                title="Test Module",
                description="Test Description",
                content="Test Content",
                duration_minutes=30,
                difficulty_level="beginner",
                module_type="video",
                is_active=True
            )
            db.session.add(test_module)
            db.session.commit()
            
            # Delete the test module
            db.session.delete(test_module)
            db.session.commit()
            
            print("✅ TrainingModule table structure verified!")
            
        except Exception as e:
            print(f"❌ Error verifying TrainingModule structure: {e}")
            return False
        
        # Create admin user
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
        
        # Create demo caregiver
        demo = User(
            username='demo',
            email='demo@safestep.com',
            password_hash=generate_password_hash('demo123'),
            first_name='Demo',
            last_name='Caregiver',
            role='caregiver',
            is_active=True
        )
        db.session.add(demo)
        
        # Create sample training modules
        modules = [
            {
                'title': 'Seizure First Aid Basics',
                'description': 'Learn the essential steps to provide immediate care during a seizure episode.',
                'content': 'This comprehensive module covers recognition, response, and recovery procedures...',
                'duration_minutes': 25,
                'difficulty_level': 'beginner',
                'module_type': 'video',
                'is_active': True
            },
            {
                'title': 'Safety Zone Management',
                'description': 'Advanced techniques for setting up and monitoring GPS safety zones.',
                'content': 'Safety zones are virtual boundaries that help protect individuals...',
                'duration_minutes': 40,
                'difficulty_level': 'intermediate',
                'module_type': 'interactive',
                'is_active': True
            },
            {
                'title': 'Understanding Epilepsy',
                'description': 'Comprehensive overview of epilepsy types, triggers, and management strategies.',
                'content': 'Epilepsy is a neurological disorder characterized by recurrent seizures...',
                'duration_minutes': 60,
                'difficulty_level': 'advanced',
                'module_type': 'reading',
                'is_active': False  # Draft
            }
        ]
        
        for module_data in modules:
            module = TrainingModule(**module_data)
            db.session.add(module)
        
        # Commit all changes
        try:
            db.session.commit()
            print("✅ All data committed successfully!")
        except Exception as e:
            print(f"❌ Error committing data: {e}")
            db.session.rollback()
            return False
        
        # Verify everything works
        print("🔍 Verifying database setup...")
        users_count = User.query.count()
        modules_count = TrainingModule.query.count()
        
        print(f"✅ Users created: {users_count}")
        print(f"✅ Training modules created: {modules_count}")
        
        # Test the admin training query specifically
        try:
            modules = TrainingModule.query.all()
            print(f"✅ Training modules query successful: {len(modules)} modules found")
            for module in modules:
                print(f"   - {module.title} ({module.difficulty_level}, {module.duration_minutes} min)")
        except Exception as e:
            print(f"❌ Training modules query failed: {e}")
            return False
        
        return True

if __name__ == '__main__':
    success = setup_fresh_database()
    if success:
        print("\n🎉 Fresh database setup completed successfully!")
        print("\nLogin credentials:")
        print("Admin: username=admin, password=admin123")
        print("Caregiver: username=demo, password=demo123")
    else:
        print("\n❌ Database setup failed!")
