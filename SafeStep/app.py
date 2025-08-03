from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to initialize Supabase client
try:
    from supabase_integration import init_supabase, get_supabase_client
    supabase_available = init_supabase()
    if supabase_available:
        print("✅ Supabase integration enabled")
    else:
        print("ℹ️ Supabase integration disabled, using SQLite")
except ImportError:
    print("ℹ️ Supabase integration not available")
    supabase_available = False

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))

# Database configuration - Supabase PostgreSQL or fallback to SQLite
database_url = os.environ.get('DATABASE_URL')
if database_url and supabase_available:
    # Using Supabase/PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print("🔗 Using Supabase PostgreSQL database")
else:
    # Fallback to SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safestep.db'
    print("🔗 Using SQLite database (local)")
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Session configuration for Flask-Login
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), default='caregiver')  # 'caregiver' or 'admin'
    supabase_user_id = db.Column(db.String(36), nullable=True)  # UUID from Supabase Auth
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    seizure_sessions = db.relationship('SeizureSession', backref='user', lazy=True)
    safety_zones = db.relationship('SafetyZone', backref='user', lazy=True)
    training_progress = db.relationship('TrainingProgress', backref='user', lazy=True)
    support_tickets = db.relationship('SupportTicket', backref='user', lazy=True)

class SeizureSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    severity = db.Column(db.String(20))  # 'mild', 'moderate', 'severe'
    notes = db.Column(db.Text)
    location = db.Column(db.String(100))
    triggers = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SafetyZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius = db.Column(db.Float)  # in meters
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrainingModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    video_url = db.Column(db.String(200))
    quiz_questions = db.Column(db.Text)  # JSON string
    duration_minutes = db.Column(db.Integer, default=30)
    difficulty_level = db.Column(db.String(20), default='beginner')  # 'beginner', 'intermediate', 'advanced'
    module_type = db.Column(db.String(50), default='video')  # 'video', 'interactive', 'reading'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class TrainingProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_percentage = db.Column(db.Integer, default=0)
    quiz_score = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    module = db.relationship('TrainingModule', backref='progress', lazy=True)

class SupportTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # 'open', 'in_progress', 'closed'
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class PredictionJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prediction_type = db.Column(db.String(50))
    confidence_score = db.Column(db.Float)
    predicted_time = db.Column(db.DateTime)
    actual_outcome = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(f"🔍 Admin check - Authenticated: {current_user.is_authenticated}")
        if current_user.is_authenticated:
            print(f"🔍 Admin check - User role: {current_user.role}")
        
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        elif current_user.role != 'admin':
            flash('You need admin privileges to access this page.', 'error')
            return redirect(url_for('landing'))
        
        print("🔍 Admin check passed - proceeding to admin page")
        return f(*args, **kwargs)
    return decorated_function

# Routes

# Landing and Authentication
@app.route('/')
def landing():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('caregiver_dashboard'))
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user_type = request.form.get('userType', '').strip()
        
        print(f"🔍 Login attempt - Username: {username}, UserType: {user_type}")
        
        if not username or not password or not user_type:
            flash('Please fill in all fields', 'error')
            return render_template('auth/login.html')
        
        # First try to find user in local database
        user = User.query.filter_by(username=username).first()
        
        # If user not found, try by email (in case they entered email instead of username)
        if not user:
            user = User.query.filter_by(email=username).first()
        
        if user:
            print(f"🔍 User found - Role: {user.role}, Active: {user.is_active}")
            
            # Check if user type matches user role
            if user.role != user_type:
                print(f"🔍 Role mismatch - User role: {user.role}, Selected type: {user_type}")
                flash('Invalid user type for this account', 'error')
                return render_template('auth/login.html')
            
            # Verify password - try both local and Supabase authentication
            password_valid = False
            
            # First try local password verification
            if check_password_hash(user.password_hash, password):
                password_valid = True
                print("🔍 Local password check passed")
            
            # If local password fails and Supabase is available, try Supabase auth
            elif supabase_available:
                try:
                    from supabase_integration import get_supabase_client
                    supabase = get_supabase_client()
                    
                    if supabase:
                        auth_response = supabase.auth.sign_in_with_password({
                            "email": user.email,
                            "password": password
                        })
                        
                        if auth_response.user:
                            password_valid = True
                            print("🔍 Supabase password check passed")
                            
                            # Update local password hash for future logins
                            user.password_hash = generate_password_hash(password)
                            db.session.commit()
                            
                except Exception as e:
                    print(f"🔍 Supabase authentication failed: {e}")
            
            if password_valid:
                if user.is_active:
                    login_user(user, remember=True)
                    print(f"🔍 User logged in successfully as {user.role}")
                    
                    # Store session info
                    session['user_id'] = user.id
                    session['user_role'] = user.role
                    session['user_name'] = f"{user.first_name} {user.last_name}"
                    
                    # Redirect based on user role
                    if user.role == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('caregiver_dashboard'))
                else:
                    print("🔍 User account is not active")
                    flash('Account is deactivated', 'error')
            else:
                print("🔍 Password check failed")
                flash('Invalid password', 'error')
        else:
            print("🔍 User not found")
            flash('Invalid username or email', 'error')
    
    return render_template('auth/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirmPassword', '')
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_type = request.form.get('userType', 'caregiver')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/sign_up.html')
            
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('auth/sign_up.html')
        
        # Check if user already exists in SQLAlchemy database
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('auth/sign_up.html')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/sign_up.html')
        
        try:
            # If Supabase is available, create user in Supabase Auth
            supabase_user_id = None
            if supabase_available:
                from supabase_integration import get_supabase_client
                supabase = get_supabase_client()
                
                if supabase:
                    try:
                        # Create user in Supabase Auth
                        auth_response = supabase.auth.sign_up({
                            "email": email,
                            "password": password,
                            "options": {
                                "data": {
                                    "first_name": first_name,
                                    "last_name": last_name,
                                    "username": username,
                                    "role": user_type
                                }
                            }
                        })
                        
                        if auth_response.user:
                            supabase_user_id = auth_response.user.id
                            print(f"✅ Supabase user created with ID: {supabase_user_id}")
                        else:
                            print("⚠️ Supabase user creation returned no user")
                            
                    except Exception as e:
                        print(f"❌ Supabase user creation failed: {e}")
                        flash(f'Error creating account: {str(e)}', 'error')
                        return render_template('auth/sign_up.html')
            
            # Create user in local SQLAlchemy database
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                role=user_type
            )
            
            # If we have a Supabase user ID, store it
            if supabase_user_id:
                user.supabase_user_id = supabase_user_id
            
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! You can now sign in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Database error during signup: {e}")
            flash('Error creating account. Please try again.', 'error')
            return render_template('auth/sign_up.html')
    
    return render_template('auth/sign_up.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            # In a real app, send password reset email
            flash('Password reset instructions sent to your email', 'info')
        else:
            flash('Email not found', 'error')
    
    return render_template('auth/forgot_pass.html')

@app.route('/logout')
@login_required
def logout():
    # Sign out from Supabase if available
    if supabase_available:
        try:
            from supabase_integration import get_supabase_client
            supabase = get_supabase_client()
            if supabase:
                supabase.auth.sign_out()
                print("🔍 Signed out from Supabase")
        except Exception as e:
            print(f"⚠️ Supabase logout error: {e}")
    
    # Clear session data
    session.clear()
    
    # Logout from Flask-Login
    logout_user()
    
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('landing'))

# Caregiver Routes
@app.route('/caregiver/dashboard')
@login_required
def caregiver_dashboard():
    recent_sessions = SeizureSession.query.filter_by(user_id=current_user.id).order_by(SeizureSession.created_at.desc()).limit(3).all()
    active_zones = SafetyZone.query.filter_by(user_id=current_user.id, is_active=True).count()
    completed_modules = TrainingProgress.query.filter_by(user_id=current_user.id, completed=True).count()
    
    return render_template('caregiver/Sai/dashboard.html', 
                         recent_sessions=recent_sessions,
                         active_zones=active_zones,
                         completed_modules=completed_modules)

@app.route('/caregiver/monitoring')
@login_required
def seizure_monitoring():
    return render_template('caregiver/Issac/monitoring.html')

@app.route('/caregiver/history')
@login_required
def seizure_history():
    sessions = SeizureSession.query.filter_by(user_id=current_user.id).order_by(SeizureSession.created_at.desc()).all()
    return render_template('caregiver/Issac/history.html', sessions=sessions)

@app.route('/caregiver/session/<int:session_id>')
@login_required
def session_detail(session_id):
    session = SeizureSession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    return render_template('caregiver/Issac/session_detail.html', session=session)

@app.route('/caregiver/zones')
@login_required
def safety_zones():
    zones = SafetyZone.query.filter_by(user_id=current_user.id).all()
    return render_template('caregiver/Sai/zones.html', zones=zones)

@app.route('/caregiver/zones/new', methods=['GET', 'POST'])
@login_required
def new_zone():
    if request.method == 'POST':
        zone = SafetyZone(
            user_id=current_user.id,
            name=request.form['name'],
            description=request.form['description'],
            latitude=float(request.form['latitude']) if request.form['latitude'] else None,
            longitude=float(request.form['longitude']) if request.form['longitude'] else None,
            radius=float(request.form['radius']) if request.form['radius'] else None
        )
        db.session.add(zone)
        db.session.commit()
        flash('Safety zone created successfully!', 'success')
        return redirect(url_for('safety_zones'))
    
    return render_template('caregiver/Sai/new_zone.html')

@app.route('/caregiver/training')
@login_required
def training_modules():
    modules = TrainingModule.query.filter_by(is_active=True).all()
    user_progress = {p.module_id: p for p in TrainingProgress.query.filter_by(user_id=current_user.id).all()}
    return render_template('caregiver/Ethan/training.html', modules=modules, user_progress=user_progress)

@app.route('/caregiver/training/<int:module_id>')
@login_required
def module_detail(module_id):
    module = TrainingModule.query.get_or_404(module_id)
    progress = TrainingProgress.query.filter_by(user_id=current_user.id, module_id=module_id).first()
    return render_template('caregiver/Ethan/module_detail.html', module=module, progress=progress)

@app.route('/caregiver/predictions')
@login_required
def prediction_dashboard():
    predictions = PredictionJob.query.filter_by(user_id=current_user.id).order_by(PredictionJob.created_at.desc()).limit(10).all()
    return render_template('caregiver/Issac/predictions.html', predictions=predictions)

@app.route('/caregiver/support', methods=['GET', 'POST'])
@login_required
def support_ticket():
    if request.method == 'POST':
        ticket = SupportTicket(
            user_id=current_user.id,
            subject=request.form['subject'],
            description=request.form['description'],
            priority=request.form['priority']
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Support ticket submitted successfully!', 'success')
        return redirect(url_for('caregiver_dashboard'))
    
    return render_template('caregiver/Issac/support.html')

# Admin Routes
@app.route('/admin')
@login_required
@admin_required
def admin_redirect():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    try:
        total_users = User.query.filter_by(role='caregiver', is_active=True).count()
        total_sessions = SeizureSession.query.count()
        open_tickets = SupportTicket.query.filter_by(status='open').count()
        
        return render_template('admin/Sai/admin_dashboard.html',
                             total_users=total_users,
                             total_sessions=total_sessions,
                             open_tickets=open_tickets)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('admin/Sai/admin_dashboard.html',
                             total_users=0,
                             total_sessions=0,
                             open_tickets=0)

@app.route('/admin/users')
@login_required
@admin_required
def user_management():
    users = User.query.filter_by(role='caregiver').all()
    return render_template('admin/Arbaz/user_management.html', users=users)

@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # Prevent admin from deleting themselves
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        # Prevent deleting other admin users
        if user.role == 'admin':
            return jsonify({'success': False, 'message': 'Cannot delete admin users'}), 400
        
        # If user has supabase_user_id, try to delete from Supabase too
        if user.supabase_user_id:
            try:
                from supabase_integration import get_supabase_client
                supabase = get_supabase_client()
                # Note: Supabase doesn't allow deleting users via client-side API for security
                # This would need to be done via admin API or manually
                print(f"Note: Supabase user {user.supabase_user_id} should be deleted manually from Supabase dashboard")
            except Exception as e:
                print(f"Warning: Could not delete Supabase user: {e}")
        
        # Delete from local database
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'User {user.username} deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({'success': False, 'message': 'Failed to delete user'}), 500

@app.route('/admin/users/toggle-status/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # Prevent self-status change
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot change your own status'}), 400
        
        # Prevent deactivating other admin users
        if user.role == 'admin':
            return jsonify({'success': False, 'message': 'Cannot change admin user status'}), 400
        
        # Get the new status from request
        data = request.get_json()
        new_status = data.get('is_active', not user.is_active)
        
        # Update user status
        user.is_active = new_status
        db.session.commit()
        
        action = 'activated' if new_status else 'deactivated'
        return jsonify({
            'success': True, 
            'message': f'User {user.username} has been {action} successfully',
            'new_status': new_status
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error updating user status: {str(e)}'}), 500

@app.route('/admin/tickets')
@login_required
@admin_required
def ticket_management():
    tickets = SupportTicket.query.order_by(SupportTicket.created_at.desc()).all()
    return render_template('admin/Sai/ticket_management.html', tickets=tickets)

@app.route('/admin/training')
@login_required
@admin_required
def training_management():
    modules = TrainingModule.query.all()
    return render_template('admin/Ethan/admin_training.html', modules=modules)

@app.route('/admin/analytics')
@login_required
@admin_required
def analytics():
    return render_template('admin/Arbaz/analytics.html')

@app.route('/admin/monitoring')
@login_required
@admin_required
def system_monitoring():
    return render_template('admin/Issac/system_monitoring.html')

# API Routes for AJAX calls
@app.route('/api/sessions', methods=['POST'])
@login_required
def create_session():
    session = SeizureSession(
        user_id=current_user.id,
        start_time=datetime.utcnow(),
        severity=request.json.get('severity'),
        location=request.json.get('location'),
        triggers=request.json.get('triggers'),
        notes=request.json.get('notes')
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({'success': True, 'session_id': session.id})

@app.route('/api/sessions/<int:session_id>/end', methods=['POST'])
@login_required
def end_session(session_id):
    session = SeizureSession.query.filter_by(id=session_id, user_id=current_user.id).first_or_404()
    session.end_time = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if doesn't exist
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
        else:
            # Ensure existing admin is active
            if not admin.is_active:
                admin.is_active = True
                db.session.commit()
                print("✅ Admin user activated!")
            print(f"✅ Admin user exists: {admin.username} - Active: {admin.is_active}")
    
    app.run(debug=True)
