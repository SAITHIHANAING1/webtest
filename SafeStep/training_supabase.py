#!/usr/bin/env python3
"""
Supabase Training Module Integration
Handles training modules and progress using Supabase
"""

from supabase_integration import get_supabase_client, init_supabase
from datetime import datetime
import json

def create_training_module_supabase(module_data):
    """Create a training module in Supabase"""
    try:
        # Try to get admin client first (service key)
        from supabase_integration import get_supabase_admin_client, get_supabase_client
        
        supabase = None
        try:
            supabase = get_supabase_admin_client()  # Try service key first
            print("🔑 Using admin client (service key)")
        except Exception:
            supabase = get_supabase_client()  # Fallback to regular client
            print("🔑 Using regular client")
        
        if not supabase:
            return None
        
        # Prepare module data for Supabase (remove timestamps, let DB handle them)
        supabase_data = {
            'title': module_data.get('title'),
            'description': module_data.get('description'),
            'content': module_data.get('content'),
            'video_url': module_data.get('video_url'),
            'duration_minutes': module_data.get('duration_minutes', 30),
            'difficulty_level': module_data.get('difficulty_level', 'beginner'),
            'module_type': module_data.get('module_type', 'video'),
            'quiz_questions': module_data.get('quiz_questions'),
            'learning_objectives': module_data.get('learning_objectives'),
            'is_active': True
            # Let database handle created_at and updated_at with DEFAULT NOW()
        }
        
        # Insert into Supabase
        result = supabase.table('training_modules').insert(supabase_data).execute()
        
        if result.data:
            print(f"✅ Training module created in Supabase: {result.data[0].get('id')}")
            return result.data[0]
        else:
            print("❌ Failed to create training module in Supabase")
            print(f"Result: {result}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating training module in Supabase: {e}")
        return None

def get_all_training_modules_supabase():
    """Get all active training modules from Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            print("❌ Failed to initialize Supabase")
            return []
            
        supabase = get_supabase_client()
        if not supabase:
            print("❌ Supabase client is None")
            return []
        
        print("🔍 Querying training modules...")
        result = supabase.table('training_modules').select('*').eq('is_active', True).order('created_at', desc=True).execute()
        
        print(f"🔍 Query result: {len(result.data) if result.data else 0} modules")
        
        if result.data:
            print(f"✅ Found {len(result.data)} training modules")
            return result.data
        else:
            print("❌ No modules found in result.data")
            return []
            
    except Exception as e:
        print(f"❌ Error getting training modules from Supabase: {e}")
        return []

def get_training_module_supabase(module_id):
    """Get a specific training module from Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return None
            
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        result = supabase.table('training_modules').select('*').eq('id', module_id).single().execute()
        
        if result.data:
            return result.data
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error getting training module from Supabase: {e}")
        return None

def create_user_progress_supabase(user_id, module_id):
    """Create or get user training progress in Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return None
            
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Check if progress already exists
        existing = supabase.table('training_progress').select('*').eq('user_id', user_id).eq('module_id', module_id).execute()
        
        if existing.data:
            print(f"✅ Progress already exists for user {user_id}, module {module_id}")
            return existing.data[0]
        
        # Create new progress record (let database handle timestamps)
        progress_data = {
            'user_id': user_id,
            'module_id': module_id,
            'completion_percentage': 0,
            'status': 'not_started'
        }
        
        result = supabase.table('training_progress').insert(progress_data).execute()
        
        if result.data:
            print(f"✅ Created new progress record for user {user_id}, module {module_id}")
            return result.data[0]
        else:
            print("❌ No data returned when creating progress")
            return None
            
    except Exception as e:
        print(f"❌ Error creating training progress in Supabase: {e}")
        return None

def update_training_progress_supabase(user_id, module_id, progress_data):
    """Update user training progress in Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return False
            
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Don't add manual timestamps - let database handle them
        result = supabase.table('training_progress').update(progress_data).eq('user_id', user_id).eq('module_id', module_id).execute()
        
        if result.data:
            print(f"✅ Training progress updated in Supabase for user {user_id}, module {module_id}")
            return True
        else:
            print(f"❌ Failed to update training progress in Supabase - no data returned")
            return False
            
    except Exception as e:
        print(f"❌ Error updating training progress in Supabase: {e}")
        return False

def get_user_training_progress_supabase(user_id):
    """Get all training progress for a user from Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return {}
            
        supabase = get_supabase_client()
        if not supabase:
            return {}
        
        result = supabase.table('training_progress').select('*').eq('user_id', user_id).execute()
        
        if result.data:
            # Convert to dictionary keyed by module_id for easy lookup
            return {p['module_id']: p for p in result.data}
        else:
            return {}
            
    except Exception as e:
        print(f"❌ Error getting user training progress from Supabase: {e}")
        return {}

def create_demo_advanced_module():
    """Create a polished advanced demo module"""
    demo_module = {
        'title': 'Advanced Seizure Response & Risk Assessment',
        'description': 'Comprehensive advanced training covering complex seizure scenarios, risk assessment protocols, and emergency decision-making for experienced caregivers.',
        'difficulty_level': 'advanced',
        'duration_minutes': 45,
        'module_type': 'comprehensive',
        'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Demo video
        'content': '''
# Advanced Seizure Response & Risk Assessment

## Module Overview
This advanced module is designed for experienced caregivers who need to handle complex seizure scenarios and make critical decisions under pressure.

## Learning Objectives
By the end of this module, you will be able to:
- Assess seizure severity and complications in real-time
- Implement advanced emergency protocols
- Make informed decisions about when to call emergency services
- Recognize and respond to status epilepticus
- Manage multiple patients during seizure events
- Document incidents for medical review

## Module Content

### Section 1: Advanced Risk Assessment
Learn to quickly evaluate seizure severity using the modified SUDEP risk assessment scale:

**High-Risk Indicators:**
- Seizure duration > 5 minutes
- Cyanosis or breathing difficulties
- Injury during seizure
- Post-ictal confusion > 30 minutes
- Multiple seizures in 24 hours

**Assessment Protocol:**
1. **Immediate Safety** - Ensure environment is safe
2. **Timing** - Start timing the seizure immediately
3. **Breathing** - Monitor airway and breathing
4. **Recovery** - Assess post-ictal state
5. **Documentation** - Record all observations

### Section 2: Complex Seizure Types
Understanding different seizure presentations:

**Focal Seizures with Secondary Generalization**
- Often start with aura or warning signs
- May progress to generalized tonic-clonic
- Require careful monitoring of progression

**Status Epilepticus**
- Medical emergency requiring immediate intervention
- Continuous seizure activity > 5 minutes
- Call emergency services immediately

**Cluster Seizures**
- Multiple seizures within 24 hours
- May indicate medication issues
- Requires medical consultation

### Section 3: Emergency Decision Making
Critical decision points during seizure events:

**When to Call 911:**
- First seizure ever
- Seizure lasts > 5 minutes
- Difficulty breathing
- Injury occurred
- Person doesn't regain consciousness
- Pregnant woman
- Diabetes or other medical conditions

**When to Administer Rescue Medication:**
- If prescribed by physician
- Seizure exceeds prescribed time limit
- Follow exact dosing instructions
- Document administration time

### Section 4: Advanced Safety Protocols
Environmental management for high-risk situations:

**Home Safety Assessment:**
- Remove sharp objects and hazards
- Ensure clear pathways
- Install safety equipment
- Create emergency action plans

**Public Space Management:**
- Crowd control techniques
- Protecting dignity and privacy
- Communicating with bystanders
- Managing emergency services arrival

### Section 5: Technology Integration
Using SafeStep's advanced features:

**GPS Safety Zones:**
- Setting up complex zone patterns
- Managing multiple patient zones
- Understanding alert priorities
- Customizing notification settings

**Incident Documentation:**
- Using voice-to-text features
- Capturing video for medical review
- Timestamping critical events
- Sharing data with healthcare team

## Practical Scenarios

### Scenario 1: Restaurant Emergency
You're dining with a person with epilepsy who begins having a focal seizure that progresses to generalized. The restaurant is crowded, and other patrons are staring.

**Your Response:**
1. Stay calm and time the seizure
2. Gently guide person to floor if safe
3. Clear immediate area
4. Politely ask others to give space
5. Monitor breathing and recovery
6. Be prepared to call 911 if needed

### Scenario 2: Multiple Patients
You're supervising a group activity when two individuals have seizures simultaneously.

**Your Response:**
1. Prioritize based on seizure severity
2. Call for additional help immediately
3. Ensure both individuals are safe
4. Monitor both for complications
5. Document both incidents thoroughly

### Scenario 3: Medication Timing
A person's seizure reaches the 3-minute mark, and you have rescue medication available.

**Your Response:**
1. Continue timing the seizure
2. Prepare medication according to protocol
3. Administer if seizure reaches prescribed threshold
4. Call emergency services
5. Monitor for medication effects

## Assessment and Certification
This module includes:
- 15 multiple-choice questions
- 3 scenario-based assessments
- Video analysis exercise
- Emergency protocol checklist

**Passing Score:** 85% or higher
**Certification:** Valid for 2 years
**Continuing Education:** 8 hours credit

## Resources and References
- Epilepsy Foundation Guidelines
- International League Against Epilepsy protocols
- SafeStep Emergency Response Manual
- Local emergency services contacts

## Support and Follow-up
After completing this module:
- Schedule practice sessions with supervisor
- Review emergency protocols monthly
- Attend quarterly skills refresher
- Participate in peer support groups
        ''',
        'learning_objectives': json.dumps([
            'Assess seizure severity using advanced risk indicators',
            'Implement complex emergency response protocols',
            'Make critical decisions about emergency service activation',
            'Manage multiple patient scenarios effectively',
            'Utilize SafeStep technology for optimal care',
            'Document incidents comprehensively for medical review'
        ]),
        'quiz_questions': json.dumps([
            {
                'question': 'What is the primary indicator for status epilepticus?',
                'options': [
                    'Seizure lasting more than 2 minutes',
                    'Continuous seizure activity for 5+ minutes',
                    'Multiple seizures in one day',
                    'Loss of consciousness during seizure'
                ],
                'correct': 1,
                'explanation': 'Status epilepticus is defined as continuous seizure activity lasting 5 minutes or longer, requiring immediate emergency medical intervention.'
            },
            {
                'question': 'When managing two simultaneous seizures, your first priority is:',
                'options': [
                    'Call 911 immediately',
                    'Try to stop both seizures',
                    'Assess which person needs more immediate attention',
                    'Document both incidents'
                ],
                'correct': 2,
                'explanation': 'Triage principles apply - assess severity and prioritize care based on immediate medical need while calling for additional help.'
            },
            {
                'question': 'High-risk indicators for seizure complications include all EXCEPT:',
                'options': [
                    'Cyanosis during seizure',
                    'Brief post-ictal confusion',
                    'Injury occurred during seizure',
                    'Seizure duration over 5 minutes'
                ],
                'correct': 1,
                'explanation': 'Brief post-ictal confusion is normal. Extended confusion (>30 minutes), cyanosis, injury, and prolonged seizures are all high-risk indicators.'
            }
        ])
    }
    
    return demo_module

def setup_training_tables_supabase():
    """Create necessary training tables in Supabase if they don't exist"""
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Check if training_modules table exists
        try:
            result = supabase.table('training_modules').select('id').limit(1).execute()
            print("✅ training_modules table exists")
        except Exception:
            print("❌ training_modules table doesn't exist - please create it in Supabase")
            return False
        
        # Check if training_progress table exists  
        try:
            result = supabase.table('training_progress').select('id').limit(1).execute()
            print("✅ training_progress table exists")
        except Exception:
            print("❌ training_progress table doesn't exist - please create it in Supabase")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking training tables: {e}")
        return False

def update_training_module_supabase(module_id, module_data):
    """Update a training module in Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return False
            
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        # Update the module in Supabase (let database handle updated_at timestamp)
        result = supabase.table('training_modules').update(module_data).eq('id', module_id).execute()
        
        if result.data:
            print(f"✅ Training module {module_id} updated in Supabase")
            return True
        else:
            print(f"❌ Failed to update training module {module_id} in Supabase - no data returned")
            return False
            
    except Exception as e:
        print(f"❌ Error updating training module in Supabase: {e}")
        return False

def create_certificate_supabase(user_id, module_id, quiz_score):
    """Create a certificate in Supabase for completed module"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return None
            
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Check if certificate already exists in the existing 'certificates' table
        existing = supabase.table('certificates').select('*').eq('user_id', user_id).eq('module_id', module_id).execute()
        
        if existing.data:
            print(f"✅ Certificate already exists for user {user_id}, module {module_id}")
            return existing.data[0]
        
        # Generate unique certificate code
        import uuid
        certificate_code = f"SAFE-{uuid.uuid4().hex[:8].upper()}"
        
        # Create new certificate record using existing table structure
        from datetime import datetime, timedelta
        certificate_data = {
            'user_id': user_id,
            'module_id': module_id,
            'certificate_code': certificate_code,
            'issued_date': datetime.utcnow().isoformat(),
            'expiry_date': (datetime.utcnow() + timedelta(days=365)).isoformat(),  # 1 year expiry
            'final_score': quiz_score,
            'verification_url': None,
            'is_active': True
        }
        
        result = supabase.table('certificates').insert(certificate_data).execute()
        
        if result.data:
            print(f"✅ Created certificate for user {user_id}, module {module_id}: {certificate_code}")
            return result.data[0]
        else:
            print("❌ No data returned when creating certificate")
            return None
            
    except Exception as e:
        print(f"❌ Error creating certificate in Supabase: {e}")
        return None

def get_certificate_supabase(user_id, module_id):
    """Get certificate for user and module from Supabase"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            return None
            
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        # Use existing 'certificates' table
        result = supabase.table('certificates').select('*').eq('user_id', user_id).eq('module_id', module_id).execute()
        
        if result.data:
            return result.data[0]
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error getting certificate from Supabase: {e}")
        return None

if __name__ == "__main__":
    # Test the training system
    print("🧪 Testing Supabase Training Integration...")
    
    if init_supabase():
        if setup_training_tables_supabase():
            print("✅ Training system ready!")
            
            # Create demo module
            demo_module = create_demo_advanced_module()
            result = create_training_module_supabase(demo_module)
            
            if result:
                print(f"✅ Demo advanced module created with ID: {result.get('id')}")
            else:
                print("❌ Failed to create demo module")
        else:
            print("❌ Training tables not ready")
    else:
        print("❌ Supabase not available")
