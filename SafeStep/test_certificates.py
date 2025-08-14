#!/usr/bin/env python3
"""
Test script to check certificate functionality
"""

from app import app, db, User, TrainingModule, TrainingProgress, Certificate
from datetime import datetime, timedelta
import json

def test_certificate_functionality():
    """Test certificate generation and display"""
    
    with app.app_context():
        try:
            # Get demo user
            demo_user = User.query.filter_by(username='demo').first()
            if not demo_user:
                print("❌ Demo user not found")
                return
            
            print(f"✅ Found demo user: {demo_user.username} (ID: {demo_user.id})")
            
            # Get all training modules
            modules = TrainingModule.query.filter_by(is_active=True).all()
            print(f"\n📚 Found {len(modules)} active training modules:")
            
            for module in modules:
                print(f"  - Module {module.id}: {module.title}")
                print(f"    Video URL: {module.video_url or 'None'}")
                print(f"    Quiz Questions: {'Yes' if module.quiz_questions else 'No'}")
                
                # Check progress for this module
                progress = TrainingProgress.query.filter_by(
                    user_id=demo_user.id, 
                    module_id=module.id
                ).first()
                
                if progress:
                    print(f"    Progress: {progress.completion_percentage}% - Status: {getattr(progress, 'status', 'N/A')}")
                    print(f"    Quiz Score: {progress.quiz_score or 'N/A'}")
                    print(f"    Completed: {progress.completed}")
                    
                    # Check certificate
                    certificate = Certificate.query.filter_by(
                        user_id=demo_user.id,
                        module_id=module.id
                    ).first()
                    
                    if certificate:
                        print(f"    Certificate: {certificate.certificate_code} (Active: {certificate.is_active})")
                    else:
                        print(f"    Certificate: None")
                        
                        # If completed with good score but no certificate, create one
                        if progress.completed and progress.quiz_score and progress.quiz_score >= 70:
                            print(f"    🔧 Creating missing certificate...")
                            import uuid
                            certificate_code = f"SAFE-{uuid.uuid4().hex[:8].upper()}"
                            
                            certificate = Certificate(
                                user_id=demo_user.id,
                                module_id=module.id,
                                certificate_code=certificate_code,
                                issued_date=datetime.utcnow(),
                                expiry_date=datetime.utcnow() + timedelta(days=365),
                                final_score=progress.quiz_score,
                                is_active=True
                            )
                            db.session.add(certificate)
                            db.session.commit()
                            print(f"    ✅ Certificate created: {certificate_code}")
                else:
                    print(f"    Progress: No progress found")
                    
                    # Create sample progress for first module if none exists
                    if module.id == 1:
                        print(f"    🔧 Creating sample progress for Module 1...")
                        progress = TrainingProgress(
                            user_id=demo_user.id,
                            module_id=module.id,
                            completed=True,
                            completion_percentage=100,
                            quiz_score=85,
                            completed_at=datetime.utcnow(),
                            status='completed'
                        )
                        db.session.add(progress)
                        db.session.commit()
                        print(f"    ✅ Sample progress created")
                
                print()
            
            # Summary
            total_progress = TrainingProgress.query.filter_by(user_id=demo_user.id).all()
            completed_modules = [p for p in total_progress if p.completed]
            certificates = Certificate.query.filter_by(user_id=demo_user.id).all()
            
            print(f"\n📊 Summary for {demo_user.username}:")
            print(f"  - Total modules with progress: {len(total_progress)}")
            print(f"  - Completed modules: {len(completed_modules)}")
            print(f"  - Certificates earned: {len(certificates)}")
            
            print(f"\n🎯 Test URLs:")
            print(f"  - Training page: http://localhost:8080/caregiver/training")
            print(f"  - Login as demo: http://localhost:8080/login (demo/demo123)")
            
            if certificates:
                for cert in certificates:
                    module = TrainingModule.query.get(cert.module_id)
                    print(f"  - Certificate for '{module.title}': http://localhost:8080/caregiver/training/{cert.module_id}/certificate")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_certificate_functionality()