#!/bin/bash
set -e

echo "🚀 SafeStep Docker Entrypoint"
echo "=================================="

# Function to wait for database
wait_for_db() {
    if [ "$DATABASE_URL" ]; then
        echo "⏳ Waiting for database to be ready..."
        python -c "
import time
import os
import sys
try:
    import psycopg2
    import urllib.parse as urlparse
    
    url = os.environ.get('DATABASE_URL')
    if url:
        parsed = urlparse.urlparse(url)
        for i in range(30):
            try:
                conn = psycopg2.connect(
                    database=parsed.path[1:],
                    user=parsed.username,
                    password=parsed.password,
                    host=parsed.hostname,
                    port=parsed.port
                )
                conn.close()
                print('✅ Database connection successful!')
                break
            except psycopg2.OperationalError:
                if i == 29:
                    print('❌ Database not ready after 30 seconds')
                    sys.exit(1)
                time.sleep(1)
                print(f'⏳ Retrying database connection... ({i+1}/30)')
except ImportError:
    print('⚠️ psycopg2 not available, skipping database check')
"
    fi
}

# Function to initialize database
init_database() {
    echo "🔧 Initializing SafeStep database..."
    python -c "
import os
import sys
sys.path.insert(0, '/app')

try:
    from app import app, db
    from werkzeug.security import generate_password_hash
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print('✅ Database tables created/verified')
        
        # Import User model
        from app import User
        
        # Create admin user if doesn't exist
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
            print('✅ Admin user created')
        
        # Create demo caregiver if doesn't exist
        demo = User.query.filter_by(username='demo').first()
        if not demo:
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
            print('✅ Demo caregiver created')
        
        db.session.commit()
        print('✅ Database initialization complete')

except Exception as e:
    print(f'⚠️ Database initialization error: {e}')
    print('🔄 Application will continue, but some features may not work')
"
}

# Function to check environment
check_environment() {
    echo "🔍 Checking environment configuration..."
    
    if [ -z "$SECRET_KEY" ]; then
        echo "⚠️ SECRET_KEY not set, using default (not recommended for production)"
    fi
    
    if [ -z "$DATABASE_URL" ]; then
        echo "⚠️ DATABASE_URL not set, falling back to SQLite"
    else
        echo "✅ PostgreSQL/Supabase database configured"
    fi
    
    if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_KEY" ]; then
        echo "✅ Supabase integration enabled"
    else
        echo "ℹ️ Supabase integration disabled (optional)"
    fi
    
    if [ -n "$GEMINI_API_KEY" ]; then
        echo "✅ AI chatbot features enabled"
    else
        echo "ℹ️ AI chatbot features disabled (optional)"
    fi
}

# Function to create necessary directories
create_directories() {
    echo "📁 Creating necessary directories..."
    mkdir -p /app/instance /app/prediction /app/static/uploads
    echo "✅ Directories created"
}

# Main execution
main() {
    check_environment
    create_directories
    wait_for_db
    init_database
    
    echo "🌐 Starting SafeStep application..."
    echo "=================================="
    echo "Admin Login: admin / admin123"
    echo "Demo Login: demo / demo123"
    echo "=================================="
    
    # Execute the main command
    exec "$@"
}

# Run main function
main "$@"