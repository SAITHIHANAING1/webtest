#!/usr/bin/env python3
"""
Educational Content for SafeStep Epilepsy Caregiver Training
Simplified version that works with current database schema
"""

from app import app, db, TrainingModule
from datetime import datetime
import json

def create_basic_training_modules():
    """Create basic epilepsy education modules"""
    
    modules_data = [
        {
            'title': 'Understanding Epilepsy: Fundamentals for Caregivers',
            'description': 'Comprehensive introduction to epilepsy, its causes, types, and impact on daily life.',
            'video_url': 'https://www.youtube.com/watch?v=yWLgNdOOmNs',
            'category': 'fundamentals',
            'difficulty_level': 'beginner',
            'duration_minutes': 45,
            'learning_objectives': [
                'Define epilepsy and understand its neurological basis',
                'Identify different types of seizures and their characteristics',
                'Recognize common triggers and risk factors',
                'Understand the impact of epilepsy on quality of life'
            ],
            'content': '''
# Understanding Epilepsy: A Caregiver's Guide

## What is Epilepsy?

Epilepsy is a neurological disorder characterized by recurrent, unprovoked seizures. It affects over 50 million people worldwide and is one of the most common neurological conditions.

### Key Facts:
- Epilepsy affects people of all ages, races, and backgrounds
- It is not contagious and is not caused by mental illness
- Most people with epilepsy can live normal, productive lives
- Seizures are caused by sudden, abnormal electrical activity in the brain

## Types of Seizures

### Focal Seizures (Partial Seizures)
- **Simple Focal Seizures**: Person remains conscious
  - May experience unusual sensations, emotions, or movements
  - Can affect any part of the body
  - Usually last 1-2 minutes

- **Complex Focal Seizures**: Consciousness is impaired
  - Person may appear confused or dazed
  - May perform repetitive movements (automatisms)
  - Usually last 1-3 minutes

### Generalized Seizures
- **Tonic-Clonic Seizures** (formerly Grand Mal):
  - Loss of consciousness
  - Body stiffening (tonic phase) followed by jerking (clonic phase)
  - May last 1-3 minutes
  - Person may be confused afterward

- **Absence Seizures** (formerly Petit Mal):
  - Brief loss of consciousness (5-30 seconds)
  - Person appears to be staring or daydreaming
  - More common in children

- **Myoclonic Seizures**:
  - Brief muscle jerks
  - Can affect arms, legs, or entire body
  - Person usually remains conscious

## Common Triggers

Understanding triggers can help prevent seizures:

### Lifestyle Triggers
- **Sleep deprivation**: Most common trigger
- **Stress**: Emotional or physical stress
- **Missed medications**: Inconsistent medication timing
- **Alcohol**: Both consumption and withdrawal
- **Illness**: Fever, infections

### Environmental Triggers
- **Flashing lights**: Photosensitive epilepsy (rare)
- **Loud noises**: Sudden, unexpected sounds
- **Temperature changes**: Extreme heat or cold

### Hormonal Triggers
- **Menstrual cycle**: Catamenial epilepsy
- **Pregnancy**: Hormonal changes
- **Puberty**: Hormonal fluctuations

## Impact on Daily Life

### Physical Impact
- Risk of injury during seizures
- Fatigue and confusion after seizures
- Medication side effects
- Activity restrictions for safety

### Emotional Impact
- Anxiety about when seizures might occur
- Depression and mood changes
- Social isolation and stigma
- Impact on self-esteem and independence

### Social Impact
- Employment challenges
- Driving restrictions
- Educational accommodations
- Relationship effects

## The Caregiver's Role

As a caregiver, you play a crucial role in:
- **Safety**: Ensuring a safe environment
- **Support**: Providing emotional and practical support
- **Advocacy**: Helping navigate healthcare and social systems
- **Education**: Learning about epilepsy and teaching others
- **Emergency Response**: Knowing how to respond during seizures

## Myths vs. Facts

### Myth: You can swallow your tongue during a seizure
**Fact**: This is impossible. Never put anything in someone's mouth during a seizure.

### Myth: All seizures involve convulsions
**Fact**: Many seizures are subtle and may look like daydreaming or confusion.

### Myth: Epilepsy is a mental illness
**Fact**: Epilepsy is a neurological condition, not a mental illness.

### Myth: People with epilepsy can't live normal lives
**Fact**: With proper treatment, most people with epilepsy can live full, productive lives.

## Next Steps

This module provides the foundation for understanding epilepsy. In subsequent modules, you'll learn about:
- Seizure first aid and emergency response
- Medication management
- Safety planning
- Communication strategies
- Legal rights and advocacy

Remember: Every person with epilepsy is unique. Work with healthcare providers to develop individualized care plans.
            ''',
            'tags': ['epilepsy', 'fundamentals', 'seizures', 'caregiver', 'basics'],
            'quiz_questions': json.dumps([
                {
                    'question': 'What is the most common trigger for seizures?',
                    'options': ['Flashing lights', 'Sleep deprivation', 'Loud noises', 'Stress'],
                    'correct': 1,
                    'explanation': 'Sleep deprivation is the most common seizure trigger. Maintaining regular sleep schedules is crucial for seizure control.'
                },
                {
                    'question': 'During a tonic-clonic seizure, you should put something in the person\'s mouth to prevent them from swallowing their tongue.',
                    'options': ['True', 'False'],
                    'correct': 1,
                    'explanation': 'FALSE: Never put anything in someone\'s mouth during a seizure. It\'s impossible to swallow your tongue, and objects can cause injury.'
                },
                {
                    'question': 'Which type of seizure involves brief muscle jerks while the person usually remains conscious?',
                    'options': ['Absence seizures', 'Tonic-clonic seizures', 'Myoclonic seizures', 'Complex focal seizures'],
                    'correct': 2,
                    'explanation': 'Myoclonic seizures involve brief muscle jerks and the person usually remains conscious throughout the episode.'
                }
            ])
        },
        {
            'title': 'Seizure First Aid and Emergency Response',
            'description': 'Essential skills for responding to seizures safely and effectively.',
            'video_url': 'https://www.youtube.com/watch?v=WbTlxtOST_E',
            'category': 'emergency_response',
            'difficulty_level': 'beginner',
            'duration_minutes': 35,
            'learning_objectives': [
                'Demonstrate proper seizure first aid techniques',
                'Identify when to call emergency services',
                'Understand post-seizure care and recovery',
                'Know how to create a seizure action plan'
            ],
            'content': '''
# Seizure First Aid and Emergency Response

## The SAFE Approach to Seizure First Aid

### S - Stay Calm and Stay with the Person
- Remain calm and reassuring
- Note the time the seizure started
- Stay with the person throughout the seizure
- Speak calmly and reassuringly

### A - Assess the Situation
- Look for medical alert jewelry or cards
- Check if this is their first seizure
- Assess the environment for safety hazards
- Note seizure characteristics for medical team

### F - Focus on Safety
- Clear the area of hard or sharp objects
- Cushion their head with something soft
- Turn them on their side if possible (recovery position)
- Loosen tight clothing around the neck
- Do NOT restrain the person
- Do NOT put anything in their mouth

### E - Emergency Services (When to Call 911)
- Seizure lasts longer than 5 minutes
- Person has difficulty breathing or waking up after seizure
- Person is injured during the seizure
- Person has another seizure soon after the first
- Person has diabetes or is pregnant
- Seizure occurs in water
- This is the person's first seizure
- Person asks for medical help

## Step-by-Step Response Guide

### During the Seizure (1-3 minutes typically)

1. **Immediate Actions**:
   - Start timing the seizure
   - Ensure the person's safety
   - Clear the surrounding area
   - Place something soft under their head

2. **Positioning**:
   - If standing, help them sit or lie down
   - Turn them onto their side (recovery position)
   - Keep their airway clear

3. **What NOT to Do**:
   - Don't hold them down or restrain movements
   - Don't put anything in their mouth
   - Don't give water, pills, or food
   - Don't perform CPR unless they stop breathing after the seizure ends

### After the Seizure (Recovery Phase)

1. **Immediate Post-Seizure**:
   - Check for injuries
   - Keep them in recovery position until fully conscious
   - Speak calmly and reassuringly
   - Stay with them until they're fully alert

2. **Recovery Support**:
   - Help them sit up slowly when ready
   - Offer water if they're fully conscious
   - Help them get to a safe, comfortable place
   - Provide information about what happened

3. **Documentation**:
   - Record seizure details (time, duration, characteristics)
   - Note any triggers or unusual circumstances
   - Document recovery time and any injuries

## Special Situations

### Seizures in Water
- **Immediate Action**: Support their head above water
- **Get Help**: Call for assistance immediately
- **Remove from Water**: Once seizure ends, carefully remove from water
- **Always Call 911**: Water-related seizures require medical evaluation

### Status Epilepticus (Prolonged Seizures)
- **Definition**: Seizure lasting more than 5 minutes
- **Action**: Call 911 immediately
- **Continue First Aid**: Maintain safety and airway
- **Medical Emergency**: This requires immediate medical intervention

### Cluster Seizures
- **Definition**: Multiple seizures in a short period
- **Action**: Follow seizure action plan if available
- **Monitor Closely**: Watch for signs of status epilepticus
- **Medical Contact**: Contact healthcare provider

## Creating a Seizure Action Plan

### Essential Information
- Person's name and emergency contacts
- Type of seizures they typically have
- Seizure triggers to avoid
- Current medications and dosages
- When to call 911
- Special instructions for their seizures

### Sample Seizure Action Plan Template

**Name**: _______________
**Emergency Contact**: _______________
**Doctor**: _______________

**Typical Seizure Type**: _______________
**Usual Duration**: _______________
**Frequency**: _______________

**Call 911 if**:
- Seizure lasts longer than ___ minutes
- Person is injured
- Breathing problems
- Other: _______________

**Medications**:
- Emergency medication: _______________
- When to give: _______________
- How to give: _______________

**Special Instructions**: _______________

## Recovery and Follow-up

### Immediate Recovery
- Person may be confused or tired
- Allow time for full recovery
- Provide a quiet, safe environment
- Monitor for any delayed effects

### When to Seek Medical Attention
- First-time seizure
- Seizure characteristics change
- Injury occurred during seizure
- Prolonged confusion or unusual behavior
- Breathing difficulties

### Documentation for Healthcare Providers
- Date and time of seizure
- Duration of seizure
- Description of seizure activity
- Possible triggers
- Recovery time
- Any injuries or complications

## Building Confidence

Remember:
- Most seizures end naturally within 1-3 minutes
- Your calm presence is reassuring
- Proper first aid can prevent injuries
- Practice makes you more confident
- Every situation is a learning opportunity

## Practice Scenarios

Consider these situations and how you would respond:

1. **At Home**: Person has a seizure while cooking
2. **In Public**: Seizure occurs in a crowded restaurant
3. **At Work**: Colleague has a seizure during a meeting
4. **Outdoors**: Seizure happens while hiking

For each scenario, think about:
- Safety considerations
- How to clear the area
- When to call for help
- How to provide comfort and support

Proper seizure first aid can make a significant difference in outcomes and helps maintain the person's dignity during a vulnerable time.
            ''',
            'tags': ['first_aid', 'emergency', 'seizure_response', 'safety', 'caregiver'],
            'quiz_questions': json.dumps([
                {
                    'question': 'When should you call 911 during a seizure?',
                    'options': ['Immediately when any seizure starts', 'When the seizure lasts longer than 5 minutes', 'Only if the person stops breathing', 'Never, seizures always end naturally'],
                    'correct': 1,
                    'explanation': 'Call 911 if a seizure lasts longer than 5 minutes, if the person is injured, has breathing difficulties, or if it\'s their first seizure.'
                },
                {
                    'question': 'What is the correct position for someone having a seizure?',
                    'options': ['On their back with head elevated', 'Sitting upright in a chair', 'On their side (recovery position)', 'Standing with support'],
                    'correct': 2,
                    'explanation': 'The recovery position (on their side) helps keep the airway clear and prevents choking on saliva.'
                }
            ])
        },
        {
            'title': 'Medication Management for Epilepsy',
            'description': 'Understanding anti-seizure medications, adherence strategies, and side effect management.',
            'video_url': 'https://www.youtube.com/watch?v=QjQQhBtUQOI',
            'category': 'medication',
            'difficulty_level': 'intermediate',
            'duration_minutes': 50,
            'learning_objectives': [
                'Understand common anti-seizure medications and their mechanisms',
                'Implement strategies for medication adherence',
                'Recognize and manage common side effects',
                'Know when to contact healthcare providers about medication issues'
            ],
            'content': '''
# Medication Management for Epilepsy

## Understanding Anti-Seizure Medications (ASMs)

Anti-seizure medications are the primary treatment for epilepsy, helping to control seizures in about 70% of people with epilepsy.

### How ASMs Work
- **Stabilize electrical activity**: Prevent abnormal electrical discharges in the brain
- **Target specific mechanisms**: Different medications work through various pathways
- **Maintain therapeutic levels**: Consistent blood levels are crucial for effectiveness

### Common Anti-Seizure Medications

#### First-Generation ASMs

**Phenytoin (Dilantin)**
- **Uses**: Focal and generalized tonic-clonic seizures
- **Common side effects**: Gum overgrowth, hair growth, dizziness
- **Monitoring**: Regular blood level checks required
- **Special considerations**: Many drug interactions

**Carbamazepine (Tegretol)**
- **Uses**: Focal seizures, trigeminal neuralgia
- **Common side effects**: Dizziness, drowsiness, nausea
- **Monitoring**: Blood counts and liver function
- **Special considerations**: Can affect birth control effectiveness

**Valproic Acid (Depakote)**
- **Uses**: Multiple seizure types, especially generalized
- **Common side effects**: Weight gain, hair loss, tremor
- **Monitoring**: Liver function, blood counts
- **Special considerations**: Avoid in pregnancy (birth defects)

#### Newer ASMs

**Levetiracetam (Keppra)**
- **Uses**: Focal and generalized seizures
- **Common side effects**: Mood changes, fatigue, dizziness
- **Advantages**: Fewer drug interactions, no blood monitoring
- **Special considerations**: Can cause behavioral changes

**Lamotrigine (Lamictal)**
- **Uses**: Focal seizures, bipolar disorder
- **Common side effects**: Rash (can be serious), dizziness
- **Advantages**: Generally well-tolerated
- **Special considerations**: Slow dose escalation required

**Topiramate (Topamax)**
- **Uses**: Focal and generalized seizures, migraine prevention
- **Common side effects**: Cognitive effects, weight loss, kidney stones
- **Advantages**: May help with weight loss
- **Special considerations**: Can affect thinking and memory

## Medication Adherence Strategies

### Why Adherence Matters
- **Seizure control**: Missing doses can trigger breakthrough seizures
- **Withdrawal seizures**: Sudden discontinuation can cause severe seizures
- **Therapeutic levels**: Consistent dosing maintains effective blood levels
- **Quality of life**: Good control improves daily functioning

### Common Adherence Challenges
- **Complex schedules**: Multiple daily doses
- **Side effects**: Unpleasant effects reduce motivation
- **Forgetfulness**: Busy lifestyles and memory issues
- **Cost**: Financial barriers to obtaining medications
- **Stigma**: Embarrassment about taking medications

### Practical Adherence Solutions

#### Medication Organization
- **Pill organizers**: Weekly or monthly organizers
- **Blister packs**: Pre-packaged by pharmacy
- **Medication apps**: Digital reminders and tracking
- **Alarm systems**: Phone or watch alarms

#### Routine Development
- **Link to daily activities**: Take with meals or brushing teeth
- **Consistent timing**: Same times every day
- **Visual cues**: Place medications where you'll see them
- **Family involvement**: Support from family members

#### Technology Solutions
- **Smartphone apps**: Medication reminder apps
- **Smart pill bottles**: Bottles that track opening
- **Pharmacy services**: Automatic refills and delivery
- **Wearable devices**: Smartwatch reminders

## Managing Side Effects

### Common Side Effect Categories

#### Neurological Effects
- **Dizziness and drowsiness**:
  - Take medications at bedtime when possible
  - Avoid driving until effects are known
  - Stay hydrated and get adequate sleep

- **Cognitive effects** (memory, concentration):
  - Use memory aids and organizers
  - Break tasks into smaller steps
  - Discuss with doctor about dose adjustments

#### Physical Effects
- **Weight changes**:
  - Monitor diet and exercise
  - Work with nutritionist if needed
  - Discuss alternative medications if severe

- **Skin reactions**:
  - Report rashes immediately
  - Use gentle, fragrance-free products
  - Protect skin from sun exposure

#### Mood and Behavioral Effects
- **Depression or anxiety**:
  - Monitor mood changes closely
  - Seek counseling or therapy
  - Consider psychiatric consultation

- **Irritability or aggression**:
  - Identify triggers and patterns
  - Use stress management techniques
  - Communicate with healthcare team

### When to Contact Healthcare Providers

#### Immediate Contact Required
- Severe rash or allergic reactions
- Thoughts of self-harm or suicide
- Severe dizziness or coordination problems
- Unusual bleeding or bruising
- Severe nausea or vomiting

#### Routine Follow-up Needed
- Persistent mild side effects
- Questions about medication timing
- Need for dose adjustments
- Planning for pregnancy
- Drug interaction concerns

## Special Considerations

### Pregnancy and ASMs
- **Pre-conception planning**: Optimize medications before pregnancy
- **Folic acid supplementation**: Reduces birth defect risk
- **Medication adjustments**: Some ASMs safer than others
- **Monitoring**: More frequent blood level checks
- **Breastfeeding**: Most ASMs compatible with breastfeeding

### Drug Interactions
- **Other medications**: Many drugs can affect ASM levels
- **Herbal supplements**: Can interfere with ASM effectiveness
- **Birth control**: Some ASMs reduce contraceptive effectiveness
- **Alcohol**: Can lower seizure threshold and affect medication

### Generic vs. Brand Name
- **Bioequivalence**: Generic versions should work the same
- **Consistency**: Stick with same manufacturer when possible
- **Monitoring**: Watch for changes when switching
- **Cost considerations**: Generics typically less expensive

## Emergency Medications

### Rescue Medications
- **Diazepam (Diastat)**: Rectal gel for prolonged seizures
- **Midazolam (Nayzilam)**: Nasal spray for cluster seizures
- **Lorazepam**: Injectable for emergency use

### When to Use
- Seizures lasting longer than usual
- Cluster seizures (multiple seizures)
- As directed in seizure action plan
- When unable to reach medical care

### Administration Training
- Learn proper technique from healthcare provider
- Practice with training devices
- Keep instructions easily accessible
- Ensure multiple caregivers are trained

## Medication Safety

### Storage Guidelines
- **Temperature**: Store at room temperature unless specified
- **Moisture**: Keep in dry place, not bathroom
- **Light**: Protect from direct sunlight
- **Children**: Use child-resistant containers
- **Expiration**: Check dates regularly and dispose safely

### Travel Considerations
- **Carry-on luggage**: Keep medications accessible
- **Extra supply**: Bring more than needed
- **Prescription labels**: Keep original containers
- **Time zones**: Adjust timing gradually
- **International travel**: Research medication availability

## Working with Your Healthcare Team

### Regular Monitoring
- **Blood levels**: For medications requiring monitoring
- **Liver function**: For medications affecting liver
- **Blood counts**: For medications affecting blood cells
- **Seizure frequency**: Track seizure patterns

### Communication Tips
- **Keep seizure diary**: Record seizures and medication times
- **List all medications**: Include over-the-counter and supplements
- **Report side effects**: Even if they seem minor
- **Ask questions**: Understand your treatment plan
- **Bring support**: Include family members in discussions

## Building a Support System

### Family and Friends
- **Education**: Teach them about medications
- **Emergency plans**: Ensure they know what to do
- **Reminder systems**: Help with adherence
- **Emotional support**: Understanding and encouragement

### Healthcare Team
- **Neurologist**: Specialist in epilepsy care
- **Pharmacist**: Medication expert and counselor
- **Primary care**: Overall health management
- **Mental health**: Support for emotional aspects

Remember: Medication management is a partnership between you, your loved one, and the healthcare team. Open communication and consistent adherence are key to successful seizure control.
            ''',
            'tags': ['medication', 'adherence', 'side_effects', 'safety', 'management'],
            'quiz_questions': json.dumps([
                {
                    'question': 'What is the most important factor in medication effectiveness for epilepsy?',
                    'options': ['Taking the highest possible dose', 'Consistent timing and adherence', 'Taking medication only when needed', 'Avoiding all side effects'],
                    'correct': 1,
                    'explanation': 'Consistent timing and adherence are crucial for maintaining therapeutic blood levels and preventing breakthrough seizures.'
                },
                {
                    'question': 'When should you contact a healthcare provider about medication side effects?',
                    'options': ['Only for life-threatening reactions', 'For any rash or mood changes', 'Never, side effects are expected', 'Only after trying to manage them yourself'],
                    'correct': 1,
                    'explanation': 'Any rash could be serious, and mood changes can indicate dangerous side effects. Always report these to your healthcare provider.'
                }
            ])
        }
    ]
    
    return modules_data

def populate_database():
    """Populate database with basic educational content"""
    
    with app.app_context():
        try:
            # Create training modules
            modules_data = create_basic_training_modules()
            
            for module_data in modules_data:
                # Check if module already exists
                existing_module = TrainingModule.query.filter_by(title=module_data['title']).first()
                if existing_module:
                    print(f"Module '{module_data['title']}' already exists, updating with video URL...")
                    existing_module.video_url = module_data.get('video_url', '')
                    db.session.commit()
                    continue
                    
                # Create training module
                module = TrainingModule(
                    title=module_data['title'],
                    description=module_data['description'],
                    content=module_data['content'],
                    video_url=module_data.get('video_url', ''),
                    category=module_data['category'],
                    difficulty_level=module_data['difficulty_level'],
                    duration_minutes=module_data['duration_minutes'],
                    learning_objectives=json.dumps(module_data['learning_objectives']),
                    tags=json.dumps(module_data['tags']),
                    quiz_questions=module_data['quiz_questions'],
                    module_type='interactive',
                    is_active=True
                )
                
                db.session.add(module)
                print(f"Created module: {module_data['title']}")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ Successfully populated database with educational content!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error populating database: {str(e)}")
            raise

if __name__ == '__main__':
    populate_database()