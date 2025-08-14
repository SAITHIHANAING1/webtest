#!/usr/bin/env python3
"""
Fix training progress data - set completed=True for modules with 100% completion and good quiz scores
"""

from app import app, db, User, TrainingModule, TrainingProgress, Certificate
from datetime import datetime, timedelta
import uuid

def fix_training_progress():
    """Fix training progress and create missing certificates"""
    
    with app.app_context():
        try:
            # Get demo user
            demo_user = User.query.filter_by(username='demo').first()
            if not demo_user:
                print("❌ Demo user not found")
                return
            
            print(f"✅ Found demo user: {demo_user.username} (ID: {demo_user.id})")
            
            # Get all progress records for demo user
            progress_records = TrainingProgress.query.filter_by(user_id=demo_user.id).all()
            
            for progress in progress_records:
                module = TrainingModule.query.get(progress.module_id)
                print(f"\n📚 Module {progress.module_id}: {module.title if module else 'Unknown'}")
                print(f"  Current state: {progress.completion_percentage}% complete, Quiz: {progress.quiz_score}, Completed: {progress.completed}")
                
                # Fix completed field if needed
                if progress.completion_percentage == 100 and progress.quiz_score and progress.quiz_score >= 70 and not progress.completed:
                    print(f"  🔧 Fixing completed field...")
                    progress.completed = True
                    if not progress.completed_at:
                        progress.completed_at = datetime.utcnow()
                    if not hasattr(progress, 'status') or not progress.status:
                        progress.status = 'completed'
                    db.session.commit()
                    print(f"  ✅ Fixed completed field")
                
                # Check if certificate exists
                certificate = Certificate.query.filter_by(
                    user_id=demo_user.id,
                    module_id=progress.module_id
                ).first()
                
                if not certificate and progress.completed and progress.quiz_score >= 70:
                    print(f"  🔧 Creating missing certificate...")
                    certificate_code = f"SAFE-{uuid.uuid4().hex[:8].upper()}"
                    
                    certificate = Certificate(
                        user_id=demo_user.id,
                        module_id=progress.module_id,
                        certificate_code=certificate_code,
                        issued_date=datetime.utcnow(),
                        expiry_date=datetime.utcnow() + timedelta(days=365),
                        final_score=progress.quiz_score,
                        is_active=True
                    )
                    db.session.add(certificate)
                    db.session.commit()
                    print(f"  ✅ Certificate created: {certificate_code}")
                elif certificate:
                    print(f"  ✅ Certificate exists: {certificate.certificate_code}")
                else:
                    print(f"  ℹ️ No certificate needed (not completed or score < 70%)")
            
            # Final summary
            print(f"\n📊 Final Summary:")
            completed_progress = TrainingProgress.query.filter_by(user_id=demo_user.id, completed=True).all()
            certificates = Certificate.query.filter_by(user_id=demo_user.id).all()
            
            print(f"  - Completed modules: {len(completed_progress)}")
            print(f"  - Certificates: {len(certificates)}")
            
            print(f"\n🎯 Certificate URLs:")
            for cert in certificates:
                module = TrainingModule.query.get(cert.module_id)
                print(f"  - {module.title}: http://localhost:8080/caregiver/training/{cert.module_id}/certificate")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    fix_training_progress()