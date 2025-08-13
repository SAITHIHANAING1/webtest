#!/usr/bin/env python3
"""
SafeStep Enhanced Flask Routes
Provides comprehensive API endpoints for all SafeStep features using Supabase.

This module implements routes for:
- Medication Management
- Healthcare Provider Management
- Care Plan Management
- Emergency Response System
- Enhanced Analytics
- Real-time Features
"""

from flask import Blueprint, request, jsonify, session, render_template
from functools import wraps
import json
from datetime import datetime, timedelta
from supabase_enhanced import get_supabase_enhanced
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
enhanced_bp = Blueprint('enhanced', __name__, url_prefix='/api/enhanced')

# Get Supabase client
sb = get_supabase_enhanced()

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Admin authentication decorator
def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# MEDICATION MANAGEMENT ROUTES
# ============================================================================

@enhanced_bp.route('/medications', methods=['POST'])
@require_auth
def create_medication():
    """Create a new medication record"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Add audit fields
        data['created_by'] = session.get('user_id')
        
        result = sb.create_medication(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'medication_management',
            'action': 'create',
            'metadata': {'medication_name': data.get('medication_name')}
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating medication: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/medications/patient/<patient_id>', methods=['GET'])
@require_auth
def get_patient_medications(patient_id):
    """Get all medications for a patient"""
    try:
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        result = sb.get_patient_medications(patient_id, active_only)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'medication_management',
            'action': 'view',
            'metadata': {'patient_id': patient_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting patient medications: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/medications/<medication_id>', methods=['PUT'])
@require_auth
def update_medication(medication_id):
    """Update a medication record"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Add audit fields
        data['updated_by'] = session.get('user_id')
        
        result = sb.update_medication(medication_id, data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'medication_management',
            'action': 'update',
            'metadata': {'medication_id': medication_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error updating medication: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/medications/log', methods=['POST'])
@require_auth
def log_medication_taken():
    """Log when a medication is taken"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.log_medication_taken(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'medication_logging',
            'action': 'create',
            'metadata': {'medication_id': data.get('medication_id')}
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error logging medication: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/medications/adherence/<patient_id>', methods=['GET'])
@require_auth
def get_medication_adherence(patient_id):
    """Get medication adherence for a patient"""
    try:
        days = int(request.args.get('days', 30))
        result = sb.get_medication_adherence(patient_id, days)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'medication_adherence',
            'action': 'view',
            'metadata': {'patient_id': patient_id, 'days': days}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting medication adherence: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# HEALTHCARE PROVIDER MANAGEMENT ROUTES
# ============================================================================

@enhanced_bp.route('/providers', methods=['POST'])
@require_admin
def create_healthcare_provider():
    """Create a new healthcare provider"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.create_healthcare_provider(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'provider_management',
            'action': 'create',
            'metadata': {'provider_name': data.get('name')}
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating healthcare provider: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/providers', methods=['GET'])
@require_auth
def get_healthcare_providers():
    """Get healthcare providers with optional filtering"""
    try:
        specialty = request.args.get('specialty')
        active_only = request.args.get('active_only', 'true').lower() == 'true'
        
        result = sb.get_healthcare_providers(specialty, active_only)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'provider_management',
            'action': 'view',
            'metadata': {'specialty': specialty}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting healthcare providers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/providers/assign', methods=['POST'])
@require_auth
def assign_provider_to_patient():
    """Assign a healthcare provider to a patient"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.assign_provider_to_patient(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'provider_assignment',
            'action': 'create',
            'metadata': {
                'patient_id': data.get('patient_id'),
                'provider_id': data.get('provider_id'),
                'relationship_type': data.get('relationship_type')
            }
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error assigning provider to patient: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/providers/patient/<patient_id>', methods=['GET'])
@require_auth
def get_patient_providers(patient_id):
    """Get all healthcare providers for a patient"""
    try:
        result = sb.get_patient_providers(patient_id)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'provider_assignment',
            'action': 'view',
            'metadata': {'patient_id': patient_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting patient providers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# CARE PLAN MANAGEMENT ROUTES
# ============================================================================

@enhanced_bp.route('/care-plans', methods=['POST'])
@require_auth
def create_care_plan():
    """Create a new care plan"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.create_care_plan(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'care_plan_management',
            'action': 'create',
            'metadata': {
                'patient_id': data.get('patient_id'),
                'plan_name': data.get('plan_name')
            }
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating care plan: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/care-plans/patient/<patient_id>', methods=['GET'])
@require_auth
def get_patient_care_plans(patient_id):
    """Get care plans for a patient"""
    try:
        status = request.args.get('status')
        result = sb.get_patient_care_plans(patient_id, status)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'care_plan_management',
            'action': 'view',
            'metadata': {'patient_id': patient_id, 'status': status}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting patient care plans: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/care-plans/tasks', methods=['POST'])
@require_auth
def create_care_plan_task():
    """Create a new care plan task"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.create_care_plan_task(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'care_plan_tasks',
            'action': 'create',
            'metadata': {
                'care_plan_id': data.get('care_plan_id'),
                'task_name': data.get('task_name')
            }
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating care plan task: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/care-plans/tasks/<task_id>/status', methods=['PUT'])
@require_auth
def update_task_status(task_id):
    """Update the status of a care plan task"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        result = sb.update_task_status(
            task_id, 
            data['status'], 
            data.get('completion_notes')
        )
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'care_plan_tasks',
            'action': 'update',
            'metadata': {
                'task_id': task_id,
                'new_status': data['status']
            }
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error updating task status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/care-plans/<care_plan_id>/progress', methods=['GET'])
@require_auth
def get_care_plan_progress(care_plan_id):
    """Get progress summary for a care plan"""
    try:
        result = sb.get_care_plan_progress(care_plan_id)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'care_plan_progress',
            'action': 'view',
            'metadata': {'care_plan_id': care_plan_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting care plan progress: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# EMERGENCY RESPONSE SYSTEM ROUTES
# ============================================================================

@enhanced_bp.route('/emergency/contacts', methods=['POST'])
@require_auth
def create_emergency_contact():
    """Create a new emergency contact"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.create_emergency_contact(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'emergency_contacts',
            'action': 'create',
            'metadata': {
                'patient_id': data.get('patient_id'),
                'contact_name': data.get('name')
            }
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating emergency contact: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/emergency/contacts/patient/<patient_id>', methods=['GET'])
@require_auth
def get_patient_emergency_contacts(patient_id):
    """Get emergency contacts for a patient"""
    try:
        result = sb.get_patient_emergency_contacts(patient_id)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'emergency_contacts',
            'action': 'view',
            'metadata': {'patient_id': patient_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting patient emergency contacts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/emergency/alerts', methods=['POST'])
@require_auth
def create_emergency_alert():
    """Create a new emergency alert"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        result = sb.create_emergency_alert(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'emergency_alerts',
            'action': 'create',
            'metadata': {
                'patient_id': data.get('patient_id'),
                'alert_type': data.get('alert_type'),
                'severity': data.get('severity')
            }
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating emergency alert: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/emergency/alerts/<alert_id>/resolve', methods=['PUT'])
@require_auth
def resolve_emergency_alert(alert_id):
    """Resolve an emergency alert"""
    try:
        data = request.get_json()
        resolved_by = session.get('user_id')
        resolution_notes = data.get('resolution_notes') if data else None
        
        result = sb.resolve_emergency_alert(alert_id, resolved_by, resolution_notes)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'emergency_alerts',
            'action': 'resolve',
            'metadata': {'alert_id': alert_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error resolving emergency alert: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/emergency/alerts/unresolved', methods=['GET'])
@require_auth
def get_unresolved_alerts():
    """Get unresolved emergency alerts"""
    try:
        patient_id = request.args.get('patient_id')
        result = sb.get_unresolved_alerts(patient_id)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'emergency_alerts',
            'action': 'view',
            'metadata': {'patient_id': patient_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting unresolved alerts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# ENHANCED ANALYTICS ROUTES
# ============================================================================

@enhanced_bp.route('/analytics/patient/<patient_id>/risk-summary', methods=['GET'])
@require_auth
def get_patient_risk_summary(patient_id):
    """Get comprehensive risk summary for a patient"""
    try:
        result = sb.get_patient_risk_summary(patient_id)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'risk_analytics',
            'action': 'view',
            'metadata': {'patient_id': patient_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting patient risk summary: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/analytics/dashboard', methods=['GET'])
@require_auth
def get_dashboard_data():
    """Get dashboard data for patients"""
    try:
        patient_id = request.args.get('patient_id')
        result = sb.get_patient_dashboard_data(patient_id)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'dashboard_analytics',
            'action': 'view',
            'metadata': {'patient_id': patient_id}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/analytics/predictions', methods=['POST'])
@require_auth
def create_prediction_result():
    """Store AI prediction results"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Add audit fields
        data['created_by'] = session.get('user_id')
        
        result = sb.create_prediction_result(data)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'ai_predictions',
            'action': 'create',
            'metadata': {
                'patient_id': data.get('patient_id'),
                'risk_score': data.get('risk_score')
            }
        })
        
        return jsonify(result), 201 if result['success'] else 400
    except Exception as e:
        logger.error(f"Error creating prediction result: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/analytics/predictions', methods=['GET'])
@require_auth
def get_latest_predictions():
    """Get latest prediction results"""
    try:
        patient_id = request.args.get('patient_id')
        limit = int(request.args.get('limit', 10))
        
        result = sb.get_latest_predictions(patient_id, limit)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'ai_predictions',
            'action': 'view',
            'metadata': {'patient_id': patient_id, 'limit': limit}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting latest predictions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# BATCH OPERATIONS ROUTES
# ============================================================================

@enhanced_bp.route('/batch/medication-adherence', methods=['POST'])
@require_admin
def batch_update_medication_adherence():
    """Update medication adherence scores for all active medications"""
    try:
        result = sb.batch_update_medication_adherence()
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'batch_operations',
            'action': 'medication_adherence_update',
            'metadata': {'updated_count': result.get('data', {}).get('updated_count', 0)}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in batch medication adherence update: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# UTILITY ROUTES
# ============================================================================

@enhanced_bp.route('/health', methods=['GET'])
def health_check():
    """Check Supabase connection health"""
    try:
        result = sb.health_check()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@enhanced_bp.route('/stats/<table_name>', methods=['GET'])
@require_admin
def get_table_stats(table_name):
    """Get basic statistics for a table"""
    try:
        result = sb.get_table_stats(table_name)
        
        # Log feature usage
        sb.log_feature_usage({
            'user_id': session.get('user_id'),
            'feature_name': 'table_statistics',
            'action': 'view',
            'metadata': {'table_name': table_name}
        })
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error getting table stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# WEB INTERFACE ROUTES (HTML TEMPLATES)
# ============================================================================

@enhanced_bp.route('/ui/medications')
@require_auth
def medications_ui():
    """Medication management UI"""
    if session.get('role') == 'admin':
        return render_template('admin/medications_admin.html')
    return render_template('caregiver/medications.html')

@enhanced_bp.route('/ui/providers')
@require_auth
def providers_ui():
    """Healthcare provider management UI"""
    if session.get('role') == 'admin':
        return render_template('admin/providers_admin.html')
    return render_template('caregiver/healthcare_providers.html')

@enhanced_bp.route('/ui/care-plans')
@require_auth
def care_plans_ui():
    """Care plan management UI"""
    if session.get('role') == 'admin':
        return render_template('admin/care_plans_admin.html')
    return render_template('caregiver/care_plans.html')

@enhanced_bp.route('/ui/emergency')
@require_auth
def emergency_ui():
    """Emergency contacts management UI"""
    if session.get('role') == 'admin':
        return render_template('admin/emergency_admin.html')
    return render_template('caregiver/emergency_contacts.html')



# Error handlers
@enhanced_bp.errorhandler(400)
def bad_request(error):
    return jsonify({'success': False, 'error': 'Bad request'}), 400

@enhanced_bp.errorhandler(401)
def unauthorized(error):
    return jsonify({'success': False, 'error': 'Unauthorized'}), 401

@enhanced_bp.errorhandler(403)
def forbidden(error):
    return jsonify({'success': False, 'error': 'Forbidden'}), 403

@enhanced_bp.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404

@enhanced_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Register blueprint function
def register_enhanced_routes(app):
    """Register the enhanced routes blueprint with the Flask app"""
    app.register_blueprint(enhanced_bp)
    logger.info("Enhanced routes registered successfully")

if __name__ == "__main__":
    print("Enhanced routes module loaded successfully!")
    print("Available endpoints:")
    print("- Medication Management: /api/enhanced/medications/*")
    print("- Healthcare Providers: /api/enhanced/providers/*")
    print("- Care Plans: /api/enhanced/care-plans/*")
    print("- Emergency Response: /api/enhanced/emergency/*")
    print("- Analytics: /api/enhanced/analytics/*")
    print("- Batch Operations: /api/enhanced/batch/*")
    print("- Utilities: /api/enhanced/health, /api/enhanced/stats/*")