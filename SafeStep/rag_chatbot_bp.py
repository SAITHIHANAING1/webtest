"""
RAG Chatbot Blueprint for SafeStep
Simple Gemini API-based chatbot with RAG capabilities
"""

from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
import google.generativeai as genai
import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import math

# Lightweight semantic retrieval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
rag_chatbot_bp = Blueprint('rag_chatbot', __name__)

class RAGChatbot:
    def __init__(self, api_key: str):
        """Initialize the RAG chatbot with Gemini API"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model (configurable)
        self.model_primary_name = os.environ.get('GEMINI_MODEL', 'gemini-1.5-pro')
        self.model_fallback_name = os.environ.get('GEMINI_FALLBACK_MODEL', 'gemini-1.5-flash')
        self.model = genai.GenerativeModel(self.model_primary_name)
        self.model_fallback = genai.GenerativeModel(self.model_fallback_name)
        
        # Knowledge base (simple in-memory storage)
        self.knowledge_base = []
        self._kb_texts: List[str] = []
        self._kb_vectorizer: Optional[TfidfVectorizer] = None
        self._kb_matrix = None

        # Short conversation memory (last N exchanges)
        self.conversation_history: List[Tuple[str, str]] = []  # (user, assistant)
        self.max_history = 6
        # Lightweight response cache to reduce API calls
        self.answer_cache: Dict[str, str] = {}
        self.max_cache_entries = 100
        
    def load_knowledge_base(self):
        """Load knowledge base from application data"""
        try:
            # Load from various data sources
            self._load_user_data()
            self._load_training_data()
            self._load_analytics_data()
            self._load_safety_protocols()
            
            logger.info(f"Loaded {len(self.knowledge_base)} knowledge base entries")

            # Build TF-IDF index for better retrieval
            self._kb_texts = [entry['content'] for entry in self.knowledge_base]
            if self._kb_texts:
                self._kb_vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
                self._kb_matrix = self._kb_vectorizer.fit_transform(self._kb_texts)
            
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
    
    def _load_user_data(self):
        """Load user-related data for RAG"""
        try:
            # Load from SQLite database
            conn = sqlite3.connect('instance/safestep.db')
            cursor = conn.cursor()
            
            # Get user statistics
            cursor.execute("SELECT COUNT(*) FROM user WHERE is_active = 1")
            active_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM seizure_session")
            total_sessions = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM safety_zone")
            total_zones = cursor.fetchone()[0]
            
            conn.close()
            
            # Add to knowledge base
            self.knowledge_base.append({
                'type': 'user_stats',
                'content': f'There are {active_users} active users in the system. '
                          f'Total monitoring sessions: {total_sessions}. '
                          f'Total safety zones created: {total_zones}.'
            })
            
        except Exception as e:
            logger.error(f"Error loading user data: {str(e)}")
    
    def _load_training_data(self):
        """Load training module data"""
        try:
            conn = sqlite3.connect('instance/safestep.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT title, content FROM training_module WHERE is_active = 1")
            modules = cursor.fetchall()
            
            for title, content in modules:
                self.knowledge_base.append({
                    'type': 'training',
                    'content': f'Training Module: {title}. Content: {content[:200]}...'
                })
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error loading training data: {str(e)}")
    
    def _load_analytics_data(self):
        """Load analytics and research data for comprehensive answers"""
        try:
            # Add SafeStep analytics information
            analytics_info = [
                {
                    'type': 'analytics_features',
                    'content': 'SafeStep Analytics Dashboard provides real-time KPI metrics, interactive filters (date range, patient filter, location, incident type), dynamic charts showing seizure risk trends and location distribution, AI-powered prediction engine, and PDF export functionality. All data is based on real 2025 epilepsy research datasets.'
                },
                {
                    'type': 'ai_prediction',
                    'content': 'SafeStep AI Prediction Engine analyzes seizure patterns using clinical algorithms. It identifies high-risk patients (>3 seizures in 7 days), detects seizure clustering, analyzes duration trends, and considers environmental factors. The system automatically updates patient risk status and is based on peer-reviewed research from Nature Scientific Data 2025.'
                },
                {
                    'type': 'research_datasets',
                    'content': 'SafeStep uses data patterns from 4 real research datasets: (1) Nature Scientific Data 2025 - EEG dataset with 84 patients and 2,516 seizure epochs, (2) Long-term multi-site LFP activity dataset with 15 subjects and 717 seizures, (3) Mesoscale epileptic networks dataset with intracranial recordings, (4) SzCORE seizure detection challenge with 65 subjects and 4,360 hours of EEG data.'
                },
                {
                    'type': 'seizure_types',
                    'content': 'SafeStep monitors various seizure types including focal seizures (60%), generalized seizures (25%), absence seizures (8%), tonic-clonic seizures (5%), and myoclonic seizures (2%). The system tracks seizure onset patterns: LVFA (35%), rhythmic spikes (30%), theta/alpha sharp activity (20%), and beta/gamma sharp activity (15%).'
                },
                {
                    'type': 'filtering_capabilities',
                    'content': 'The analytics dashboard supports advanced filtering: Date ranges (7, 30, 90, 365 days), Patient filters (all patients, high-risk only, recent incidents), Location filters (home, hospital, public, work), and Incident type filters (all incidents, seizures only, falls, medication issues). All KPIs, charts, and predictions update dynamically with filter changes.'
                }
            ]
            
            self.knowledge_base.extend(analytics_info)
            
        except Exception as e:
            logger.error(f"Error loading analytics data: {str(e)}")
    
    def _load_safety_protocols(self):
        """Load safety protocols and guidelines"""
        safety_protocols = [
            {
                'type': 'protocol',
                'content': 'Seizure Response Protocol: 1) Stay calm and ensure safety. 2) Clear the area of hazards. 3) Time the seizure. 4) Do not restrain the person. 5) Call emergency services if seizure lasts more than 5 minutes.'
            },
            {
                'type': 'protocol', 
                'content': 'Safety Zone Protocol: Safety zones are virtual boundaries that alert caregivers when a person with intellectual disability leaves the designated area. Zones can be customized with different radius settings.'
            },
            {
                'type': 'protocol',
                'content': 'Monitoring Protocol: The system continuously monitors for seizure activity and zone breaches. Alerts are sent to caregivers immediately when incidents are detected.'
            },
            {
                'type': 'protocol',
                'content': 'Training Protocol: All caregivers must complete mandatory training modules covering seizure recognition, response procedures, and safety zone management.'
            },
            {
                'type': 'epilepsy_info',
                'content': 'Epilepsy Overview: Epilepsy affects over 50 million people worldwide. It is characterized by recurrent seizures due to abnormal electrical activity in the brain. Types include focal seizures (partial), generalized seizures, and unknown onset seizures. Common triggers include stress, sleep deprivation, missed medications, flashing lights, and hormonal changes.'
            },
            {
                'type': 'medication_info',
                'content': 'Epilepsy Medications: Common anti-seizure medications include Levetiracetam, Carbamazepine, Valproate, Lamotrigine, Phenytoin, and Topiramate. Medication adherence is crucial for seizure control. Never stop medications suddenly without medical supervision as this can trigger status epilepticus.'
            },
            {
                'type': 'monitoring_tech',
                'content': 'EEG Monitoring Technology: SafeStep uses advanced EEG monitoring including scalp EEG (19-32 channels), intracranial EEG (iEEG), and high-density arrays (96-128 channels). Sampling rates range from 256Hz to 30kHz. The system detects interictal epileptiform discharges (IEDs) and high-frequency oscillations (HFOs) as biomarkers.'
            },
            {
                'type': 'seizure_classification',
                'content': 'Seizure Classification: Focal seizures originate in one brain region and may remain localized or spread. Generalized seizures involve both brain hemispheres from onset. Absence seizures cause brief lapses in awareness. Tonic-clonic seizures involve muscle stiffening and rhythmic jerking. Myoclonic seizures are brief muscle jerks.'
            }
        ]
        
        self.knowledge_base.extend(safety_protocols)
    
    def search_knowledge_base(self, query: str, user_role: str = 'caregiver') -> List[str]:
        """Search knowledge base for relevant information"""
        relevant_info: List[str] = []

        # Prefer semantic TF-IDF retrieval; fallback to keyword
        try:
            if self._kb_vectorizer is not None and self._kb_matrix is not None and len(self._kb_texts) > 0:
                q_vec = self._kb_vectorizer.transform([query])
                sims = cosine_similarity(q_vec, self._kb_matrix).flatten()
                top_idx = sims.argsort()[::-1][:5]
                for idx in top_idx:
                    if sims[idx] > 0:
                        relevant_info.append(self._kb_texts[idx])
        except Exception:
            pass

        if not relevant_info:
            # Simple keyword fallback
            ql = query.lower()
            for entry in self.knowledge_base:
                content = entry['content']
                if any(k in content.lower() for k in ql.split()):
                    relevant_info.append(content)

        # Add role-specific information
        if user_role == 'caregiver':
            relevant_info.append("As a caregiver, you have access to monitoring tools, safety zones, and training modules.")
        elif user_role == 'admin':
            relevant_info.append("As an administrator, you have access to user management, analytics, and system monitoring tools.")
        
        return relevant_info[:5]  # Limit to 5 most relevant pieces

    # --- Tooling for complex queries ---
    def _supabase_client(self):
        try:
            from supabase_integration import get_supabase_client
            return get_supabase_client()
        except Exception:
            return None

    def tool_get_high_risk_patients(self, limit: int = 5) -> Dict:
        client = self._supabase_client()
        if not client:
            return {'success': False, 'error': 'Supabase not available'}
        try:
            resp = client.table('pwids').select('patient_id,risk_status,risk_score,recent_seizure_count,last_risk_update') \
                .in_('risk_status', ['High', 'Critical']).order('risk_score', desc=True).limit(limit).execute()
            return {'success': True, 'data': resp.data}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def tool_incident_stats(self, days: int = 30) -> Dict:
        client = self._supabase_client()
        if not client:
            return {'success': False, 'error': 'Supabase not available'}
        try:
            since = (datetime.utcnow() - timedelta(days=days)).isoformat()
            resp = client.table('incidents').select('incident_type,severity,environment,response_time_minutes,incident_date') \
                .gte('incident_date', since).execute()
            rows = resp.data or []
            total = len(rows)
            seizures = sum(1 for r in rows if (r.get('incident_type') or '').lower() == 'seizure')
            avg_resp = None
            rt = [r.get('response_time_minutes') for r in rows if r.get('response_time_minutes') is not None]
            if rt:
                avg_resp = round(sum(rt) / len(rt), 2)
            env_counts: Dict[str, int] = {}
            for r in rows:
                env = (r.get('environment') or 'unknown').lower()
                env_counts[env] = env_counts.get(env, 0) + 1
            return {'success': True, 'data': {
                'total_incidents': total,
                'seizure_count': seizures,
                'avg_response_time': avg_resp,
                'by_environment': env_counts
            }}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def tool_predict_patient(self, patient_id: str) -> Dict:
        try:
            # Reuse prediction engine directly for best results
            from prediction_model import prediction_engine
            client = self._supabase_client()
            if not client:
                return {'success': False, 'error': 'Supabase not available'}
            result = prediction_engine.predict_patient_risk(patient_id, client)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _detect_intents(self, query: str) -> Dict:
        q = query.lower()
        intents = {
            'list_high_risk': any(k in q for k in ['high risk', 'critical patients', 'list high-risk', 'top risk']),
            'incident_stats': any(k in q for k in ['incidents last', 'incident stats', 'how many incidents', 'seizures last']),
            'predict_patient': any(k in q for k in ['predict', 'risk for patient'])
        }
        # Extract patient id for prediction
        pid = None
        if intents['predict_patient']:
            for token in q.replace('#', ' ').replace('-', ' ').split():
                if token.startswith('sub') or token.startswith('pwid'):
                    pid = token
                    break
        return {'intents': intents, 'patient_id': pid}
    
    def generate_response(self, query: str, user_role: str = 'caregiver') -> str:
        """Generate response using Gemini API with RAG"""
        try:
            # 1) Tool-augmented reasoning for complex queries
            plan = self._detect_intents(query)
            tool_context_parts: List[str] = []

            # Only admins can access live data/tools
            if user_role == 'admin':
                if plan['intents'].get('list_high_risk'):
                    res = self.tool_get_high_risk_patients(limit=5)
                    if res.get('success'):
                        pts = res['data']
                        summary = '\n'.join([f"- {p.get('patient_id')}: {p.get('risk_status')} ({p.get('risk_score')}) seizures7d={p.get('recent_seizure_count')}" for p in pts])
                        tool_context_parts.append(f"High-risk patients (top 5):\n{summary}")

                if plan['intents'].get('incident_stats'):
                    res = self.tool_incident_stats(days=30)
                    if res.get('success'):
                        d = res['data']
                        envs = ', '.join([f"{k}:{v}" for k,v in d.get('by_environment', {}).items()])
                        tool_context_parts.append(
                            f"Incident stats (30d): total={d.get('total_incidents')}, seizures={d.get('seizure_count')}, avg_response={d.get('avg_response_time')} min, envs=[{envs}]"
                        )

                if plan['intents'].get('predict_patient') and plan.get('patient_id'):
                    res = self.tool_predict_patient(plan['patient_id'])
                    if res.get('success'):
                        pred = res.get('prediction', {})
                        tool_context_parts.append(
                            f"Prediction for {plan['patient_id']}: level={pred.get('risk_level')}, score={pred.get('risk_score')}, confidence={pred.get('confidence')}%"
                        )

            # Search knowledge base
            relevant_info = self.search_knowledge_base(query, user_role)
            
            # Build context
            context_sections = []
            if relevant_info:
                context_sections.append("Knowledge Base:\n" + "\n".join(relevant_info))
            if tool_context_parts:
                context_sections.append("Live Data:\n" + "\n".join(tool_context_parts))
            context = "\n\n".join(context_sections) if context_sections else "No specific information found in knowledge base."
            
            # Create prompt with context (truncate to control tokens)
            def _truncate(txt: str, max_chars: int = 6000) -> str:
                return txt if len(txt) <= max_chars else (txt[:max_chars] + "\n...[truncated]")

            prompt = f"""
            You are a helpful AI assistant for the SafeStep application, which helps caregivers monitor people with intellectual disabilities.
            
            Context from knowledge base:
            {_truncate(context, 6000)}
            
            User Role: {user_role}
            User Question: {query}
            
            Requirements:
            - Provide a helpful, accurate response using the context and clinical best practices.
            - If live data is provided, prioritize it and summarize concisely.
            - If an action is requested but not available, describe exactly how to perform it in the UI.
            - Keep responses structured with short bullets when listing items.
            Keep responses concise and practical. If you don't have specific information, say so and suggest contacting support.
            """
            
            # Cache lookup to avoid duplicate API calls
            cache_key = f"{user_role}|{query.strip().lower()}"
            if cache_key in self.answer_cache:
                return self.answer_cache[cache_key]

            # Generate response with automatic fallback on quota (429)
            try:
                response = self.model.generate_content(prompt)
                text = response.text
            except Exception as e:
                emsg = str(e).lower()
                if '429' in emsg or 'quota' in emsg or 'rate limit' in emsg:
                    try:
                        response = self.model_fallback.generate_content(prompt)
                        text = response.text
                    except Exception as e2:
                        raise e2
                else:
                    raise

            # Update short conversation memory
            self.conversation_history.append((query, text))
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]

            # Update cache (simple size cap)
            if len(self.answer_cache) >= self.max_cache_entries:
                # Remove an arbitrary old item
                self.answer_cache.pop(next(iter(self.answer_cache)))
            self.answer_cache[cache_key] = text

            return text
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"API Key configured: {bool(self.api_key)}")
            # Return a more helpful error message with debugging info
            return (
                "Chatbot Error: "
                + str(e)
                + ". Tip: reduce request rate/size, or set GEMINI_MODEL=gemini-1.5-flash for lower quota usage."
            )

# Global chatbot instance
chatbot = None

def init_chatbot():
    """Initialize the chatbot with API key"""
    global chatbot
    
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        chatbot = RAGChatbot(api_key)
        chatbot.load_knowledge_base()
        logger.info("Chatbot initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing chatbot: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        logger.error(f"API Key (first 10 chars): {api_key[:10] if api_key else 'None'}...")
        return False

@rag_chatbot_bp.route('/api/chatbot/ask', methods=['POST'])
def ask_chatbot():
    """Handle chatbot questions"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        user_role = data.get('user_role', 'caregiver')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        if not chatbot:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        # Generate response
        response = chatbot.generate_response(question, user_role)
        
        # Log the interaction
        logger.info(f"Chatbot Q&A - Role: {user_role}, Q: {question[:50]}..., A: {response[:50]}...")
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chatbot endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@rag_chatbot_bp.route('/api/chatbot/status', methods=['GET'])
def chatbot_status():
    """Check chatbot status"""
    api_key_configured = bool(os.environ.get('GEMINI_API_KEY'))
    
    return jsonify({
        'success': True,
        'data': {
            'initialized': chatbot is not None,
            'status': 'active' if chatbot else 'inactive',
            'knowledge_base_size': len(chatbot.knowledge_base) if chatbot else 0,
            'model': 'gemini-1.5-flash' if chatbot else None,
            'api_key_configured': api_key_configured,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@rag_chatbot_bp.route('/api/chatbot/reload', methods=['POST'])
def reload_knowledge_base():
    """Reload knowledge base"""
    try:
        if not chatbot:
            return jsonify({'error': 'Chatbot not initialized'}), 500
        
        chatbot.load_knowledge_base()
        
        return jsonify({
            'success': True,
            'message': 'Knowledge base reloaded successfully',
            'knowledge_base_size': len(chatbot.knowledge_base)
        })
        
    except Exception as e:
        logger.error(f"Error reloading knowledge base: {str(e)}")
        return jsonify({'error': 'Failed to reload knowledge base'}), 500
