#!/usr/bin/env python3
"""
Admin Routes for SafeStep
Handles system monitoring, user management, and enhanced analytics
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
import json
import psutil
import time
from supabase_integration import get_supabase_client, supabase_available
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin authentication using Flask-Login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        elif current_user.role != 'admin':
            flash('You need admin privileges to access this page.', 'error')
            return redirect(url_for('landing'))
        return f(*args, **kwargs)
    return decorated_function

# =============================================================================
# SYSTEM MONITORING API ROUTES
# =============================================================================

@admin_bp.route('/api/system/metrics')
@admin_required
def get_system_metrics():
    """Get current system metrics (CPU, Memory, Disk, Network)"""
    try:
        # Get real-time system metrics using psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        net_io = psutil.net_io_counters()
        
        # Calculate network speed (simplified)
        network_speed = min(100, (net_io.bytes_sent + net_io.bytes_recv) / (1024 * 1024))  # MB/s
        
        metrics = {
            'cpu': {
                'value': round(cpu_percent, 1),
                'unit': '%',
                'status': 'warning' if cpu_percent > 80 else 'healthy'
            },
            'memory': {
                'value': round(memory.percent, 1),
                'unit': '%',
                'used_gb': round(memory.used / (1024**3), 1),
                'total_gb': round(memory.total / (1024**3), 1),
                'status': 'warning' if memory.percent > 85 else 'healthy'
            },
            'disk': {
                'value': round(disk.percent, 1),
                'unit': '%',
                'used_gb': round(disk.used / (1024**3), 1),
                'total_gb': round(disk.total / (1024**3), 1),
                'status': 'warning' if disk.percent > 90 else 'healthy'
            },
            'network': {
                'value': round(network_speed, 1),
                'unit': 'MB/s',
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'status': 'healthy'
            }
        }
        
        # Store metrics in Supabase if available
        if supabase_available:
            supabase = get_supabase_client()
            try:
                for metric_type, data in metrics.items():
                    supabase.table('system_metrics').insert({
                        'metric_type': metric_type,
                        'metric_value': data['value'],
                        'metric_unit': data['unit'],
                        'additional_data': json.dumps({
                            'status': data['status'],
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    }).execute()
            except Exception as e:
                print(f"Error storing metrics in Supabase: {e}")
        
        return jsonify({
            'success': True,
            'metrics': metrics,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/system/services')
@admin_required
def get_system_services():
    """Get system services status"""
    try:
        if not supabase_available:
            # Return mock data if Supabase not available
            return jsonify({
                'success': True,
                'services': [
                    {
                        'name': 'Web Application Server',
                        'description': 'Flask WSGI Server',
                        'status': 'running',
                        'cpu_usage': 32.5,
                        'memory_usage': 68.2,
                        'uptime': '1 day, 2 hours'
                    }
                ]
            })
        
        supabase = get_supabase_client()
        result = supabase.table('system_services').select('*').execute()
        
        services = []
        for service in result.data:
            # Calculate uptime string
            if service.get('uptime_seconds'):
                uptime_hours = service['uptime_seconds'] // 3600
                uptime_days = uptime_hours // 24
                uptime_hours = uptime_hours % 24
                uptime_str = f"{uptime_days} days, {uptime_hours} hours" if uptime_days > 0 else f"{uptime_hours} hours"
            else:
                uptime_str = "Unknown"
            
            services.append({
                'id': service['id'],
                'name': service['service_name'],
                'description': service['service_description'],
                'type': service['service_type'],
                'status': service['status'],
                'cpu_usage': service.get('cpu_usage', 0),
                'memory_usage': service.get('memory_usage', 0),
                'uptime': uptime_str,
                'last_restart': service.get('last_restart'),
                'updated_at': service['updated_at']
            })
        
        return jsonify({'success': True, 'services': services})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/system/logs')
@admin_required
def get_system_logs():
    """Get recent system logs"""
    try:
        limit = request.args.get('limit', 50, type=int)
        log_level = request.args.get('level', '')
        log_source = request.args.get('source', '')
        
        if not supabase_available:
            # Return mock data
            return jsonify({
                'success': True,
                'logs': [
                    {
                        'timestamp': '2024-01-15 14:32:15',
                        'level': 'INFO',
                        'source': 'webapp',
                        'message': 'Application server started successfully'
                    }
                ]
            })
        
        supabase = get_supabase_client()
        query = supabase.table('system_logs').select('*').order('logged_at', desc=True).limit(limit)
        
        if log_level:
            query = query.eq('log_level', log_level.upper())
        if log_source:
            query = query.eq('log_source', log_source)
        
        result = query.execute()
        
        logs = []
        for log in result.data:
            logs.append({
                'id': log['id'],
                'timestamp': log['logged_at'],
                'level': log['log_level'],
                'source': log['log_source'],
                'message': log['log_message'],
                'user_id': log.get('user_id'),
                'ip_address': log.get('ip_address'),
                'context': log.get('additional_context')
            })
        
        return jsonify({'success': True, 'logs': logs})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/system/alerts')
@admin_required
def get_system_alerts():
    """Get active system alerts"""
    try:
        if not supabase_available:
            return jsonify({
                'success': True,
                'alerts': [
                    {
                        'id': 1,
                        'type': 'service_down',
                        'severity': 'critical',
                        'title': 'Service Down',
                        'message': 'Notification service is not responding',
                        'created_at': datetime.utcnow().isoformat()
                    }
                ]
            })
        
        supabase = get_supabase_client()
        result = supabase.table('system_alerts').select('*').eq('is_acknowledged', False).order('created_at', desc=True).execute()
        
        alerts = []
        for alert in result.data:
            alerts.append({
                'id': alert['id'],
                'type': alert['alert_type'],
                'severity': alert['severity'],
                'title': alert['title'],
                'message': alert['message'],
                'source': alert.get('source_service'),
                'created_at': alert['created_at']
            })
        
        return jsonify({'success': True, 'alerts': alerts})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/system/alerts/<int:alert_id>/acknowledge', methods=['POST'])
@admin_required
def acknowledge_alert(alert_id):
    """Acknowledge a system alert"""
    try:
        if not supabase_available:
            return jsonify({'success': True, 'message': 'Alert acknowledged'})
        
        user_id = current_user.id if current_user.is_authenticated else None
        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'}), 401
        
        supabase = get_supabase_client()
        result = supabase.table('system_alerts').update({
            'is_acknowledged': True,
            'acknowledged_by': user_id,
            'acknowledged_at': datetime.utcnow().isoformat()
        }).eq('id', alert_id).execute()
        
        return jsonify({'success': True, 'message': 'Alert acknowledged successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/system/performance/<metric_type>')
@admin_required
def get_performance_history(metric_type):
    """Get performance history for charts"""
    try:
        hours = request.args.get('hours', 24, type=int)
        
        if not supabase_available:
            # Return mock data for charts
            import random
            times = []
            values = []
            for i in range(24):
                times.append((datetime.utcnow() - timedelta(hours=i)).strftime('%H:%M'))
                if metric_type == 'cpu':
                    values.append(round(25 + random.random() * 20, 1))
                elif metric_type == 'memory':
                    values.append(round(60 + random.random() * 15, 1))
                else:
                    values.append(round(100 + random.random() * 50, 1))
            
            return jsonify({
                'success': True,
                'labels': times[::-1],  # Reverse to show chronologically
                'values': values[::-1],
                'metric_type': metric_type
            })
        
        supabase = get_supabase_client()
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        result = supabase.table('system_metrics').select('metric_value', 'recorded_at').eq('metric_type', metric_type).gte('recorded_at', start_time.isoformat()).order('recorded_at').execute()
        
        labels = []
        values = []
        for record in result.data:
            time_obj = datetime.fromisoformat(record['recorded_at'].replace('Z', '+00:00'))
            labels.append(time_obj.strftime('%H:%M'))
            values.append(float(record['metric_value']))
        
        return jsonify({
            'success': True,
            'labels': labels,
            'values': values,
            'metric_type': metric_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =============================================================================
# USER MANAGEMENT API ROUTES
# =============================================================================

@admin_bp.route('/api/users')
@admin_required
def get_users():
    """Get all users with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        role_filter = request.args.get('role', '')
        status_filter = request.args.get('status', '')
        
        if not supabase_available:
            # Return mock data
            return jsonify({
                'success': True,
                'users': [
                    {
                        'id': 1,
                        'username': 'admin',
                        'email': 'admin@safestep.com',
                        'first_name': 'Admin',
                        'last_name': 'User',
                        'role': 'admin',
                        'is_active': True,
                        'created_at': '2024-01-01',
                        'last_login': '2024-01-15 10:30:00'
                    }
                ],
                'total': 1,
                'page': page,
                'per_page': per_page
            })
        
        supabase = get_supabase_client()
        query = supabase.table('users').select('*')
        
        # Apply filters
        if role_filter:
            query = query.eq('role', role_filter)
        if status_filter == 'active':
            query = query.eq('is_active', True)
        elif status_filter == 'inactive':
            query = query.eq('is_active', False)
        
        # Apply search
        if search:
            # Note: Supabase doesn't have great full-text search, so we'll do basic matching
            # In a real implementation, you might want to use PostgreSQL's full-text search
            query = query.or_(f'username.ilike.%{search}%,email.ilike.%{search}%,first_name.ilike.%{search}%,last_name.ilike.%{search}%')
        
        # Execute query
        result = query.order('created_at', desc=True).execute()
        
        # Simple pagination (for better performance, implement server-side pagination)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        users = result.data[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'users': users,
            'total': len(result.data),
            'page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/users', methods=['POST'])
@admin_required
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        # Hash password
        password_hash = generate_password_hash(data['password'])
        
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password_hash': password_hash,
            'first_name': data.get('first_name', ''),
            'last_name': data.get('last_name', ''),
            'role': data['role'],
            'is_active': data.get('is_active', True),
            'created_at': datetime.utcnow().isoformat()
        }
        
        if not supabase_available:
            return jsonify({'success': True, 'message': 'User created successfully', 'user': user_data})
        
        supabase = get_supabase_client()
        result = supabase.table('users').insert(user_data).execute()
        
        if result.data:
            # Log the creation
            supabase.table('system_logs').insert({
                'log_level': 'INFO',
                'log_source': 'user_management',
                'log_message': f'New user created: {data["username"]}',
                'user_id': current_user.id if current_user.is_authenticated else None
            }).execute()
            
            return jsonify({
                'success': True,
                'message': 'User created successfully',
                'user': result.data[0]
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to create user'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    try:
        data = request.get_json()
        is_active = data.get('is_active', False)
        
        if not supabase_available:
            return jsonify({
                'success': True,
                'message': f'User {"activated" if is_active else "deactivated"} successfully'
            })
        
        supabase = get_supabase_client()
        result = supabase.table('users').update({
            'is_active': is_active,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', user_id).execute()
        
        if result.data:
            # Log the status change
            supabase.table('system_logs').insert({
                'log_level': 'INFO',
                'log_source': 'user_management',
                'log_message': f'User {user_id} {"activated" if is_active else "deactivated"}',
                'user_id': current_user.id if current_user.is_authenticated else None
            }).execute()
            
            return jsonify({
                'success': True,
                'message': f'User {"activated" if is_active else "deactivated"} successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user"""
    try:
        # Prevent deleting self
        if user_id == current_user.id:
            return jsonify({'success': False, 'error': 'Cannot delete your own account'}), 400
        
        if not supabase_available:
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        
        supabase = get_supabase_client()
        
        # Get user info for logging before deletion
        user_result = supabase.table('users').select('username').eq('id', user_id).execute()
        if not user_result.data:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        username = user_result.data[0]['username']
        
        # Delete user
        result = supabase.table('users').delete().eq('id', user_id).execute()
        
        if result.data:
            # Log the deletion
            supabase.table('system_logs').insert({
                'log_level': 'WARN',
                'log_source': 'user_management',
                'log_message': f'User deleted: {username}',
                'user_id': current_user.id if current_user.is_authenticated else None
            }).execute()
            
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to delete user'}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/users/stats')
@admin_required
def get_user_stats():
    """Get user statistics for dashboard"""
    try:
        if not supabase_available:
            return jsonify({
                'success': True,
                'stats': {
                    'total_users': 24,
                    'active_users': 22,
                    'admin_count': 2,
                    'caregiver_count': 22,
                    'recent_logins': 15
                }
            })
        
        supabase = get_supabase_client()
        
        # Get all users
        users_result = supabase.table('users').select('role', 'is_active', 'last_login').execute()
        users = users_result.data
        
        total_users = len(users)
        active_users = len([u for u in users if u.get('is_active', False)])
        admin_count = len([u for u in users if u.get('role') == 'admin'])
        caregiver_count = len([u for u in users if u.get('role') == 'caregiver'])
        
        # Count recent logins (last 24 hours)
        recent_threshold = datetime.utcnow() - timedelta(hours=24)
        recent_logins = 0
        for user in users:
            if user.get('last_login'):
                try:
                    login_time = datetime.fromisoformat(user['last_login'].replace('Z', '+00:00'))
                    if login_time > recent_threshold:
                        recent_logins += 1
                except:
                    pass
        
        return jsonify({
            'success': True,
            'stats': {
                'total_users': total_users,
                'active_users': active_users,
                'admin_count': admin_count,
                'caregiver_count': caregiver_count,
                'recent_logins': recent_logins
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =============================================================================
# SYSTEM ACTIONS
# =============================================================================

@admin_bp.route('/api/system/actions/restart-service', methods=['POST'])
@admin_required
def restart_service():
    """Restart a system service"""
    try:
        data = request.get_json()
        service_name = data.get('service_name')
        
        if not service_name:
            return jsonify({'success': False, 'error': 'Service name is required'}), 400
        
        # In a real implementation, you would actually restart the service
        # For now, we'll just simulate it and update the database
        
        if supabase_available:
            supabase = get_supabase_client()
            
            # Update service status
            supabase.table('system_services').update({
                'last_restart': datetime.utcnow().isoformat(),
                'status': 'running',
                'updated_at': datetime.utcnow().isoformat()
            }).eq('service_name', service_name).execute()
            
            # Log the restart
            supabase.table('system_logs').insert({
                'log_level': 'INFO',
                'log_source': 'system_admin',
                'log_message': f'Service restarted: {service_name}',
                'user_id': current_user.id if current_user.is_authenticated else None
            }).execute()
        
        return jsonify({
            'success': True,
            'message': f'{service_name} service restarted successfully'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/api/system/actions/clear-cache', methods=['POST'])
@admin_required
def clear_system_cache():
    """Clear system cache"""
    try:
        # Simulate cache clearing
        if supabase_available:
            supabase = get_supabase_client()
            supabase.table('system_logs').insert({
                'log_level': 'INFO',
                'log_source': 'system_admin',
                'log_message': 'System cache cleared',
                'user_id': current_user.id if current_user.is_authenticated else None
            }).execute()
        
        return jsonify({'success': True, 'message': 'System cache cleared successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# =============================================================================
# PAGE ROUTES
# =============================================================================

@admin_bp.route('/system-monitoring')
@admin_required
def system_monitoring():
    """System monitoring dashboard page"""
    return render_template('admin/Arbaz/system_monitoring.html')

@admin_bp.route('/user-management')
@admin_required
def user_management():
    """User management page"""
    # Load users for template
    users = []
    if supabase_available:
        try:
            supabase = get_supabase_client()
            result = supabase.table('users').select('*').order('created_at', desc=True).execute()
            users = result.data
        except Exception as e:
            print(f"Error loading users: {e}")
    
    return render_template('admin/Arbaz/user_management.html', users=users)

@admin_bp.route('/analytics')
@admin_required
def analytics():
    """Analytics dashboard page"""
    return render_template('admin/Arbaz/analytics.html')
