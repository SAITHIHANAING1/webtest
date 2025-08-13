#!/usr/bin/env python3
"""
Docker-specific configuration for SafeStep
Handles graceful database setup for containerized environments
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import sys

def load_docker_environment():
    """Load environment variables for Docker deployment"""
    # Load from .env file if it exists
    if os.path.exists('.env'):
        load_dotenv('.env')
    # Fallback to config.env
    elif os.path.exists('config.env'):
        load_dotenv('config.env')
    
    print("🔧 Docker Configuration Loaded")

def setup_database_config():
    """Setup database configuration for Docker environment"""
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Test PostgreSQL/Supabase connection
        try:
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            print("✅ PostgreSQL/Supabase database connection verified")
            return database_url
        except Exception as e:
            print(f"⚠️ PostgreSQL connection failed: {e}")
            print("🔄 Falling back to SQLite for local development")
    
    # Fallback to SQLite
    sqlite_path = os.path.join('/app/instance', 'safestep.db')
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    sqlite_url = f'sqlite:///{sqlite_path}'
    print(f"✅ Using SQLite database: {sqlite_url}")
    return sqlite_url

def setup_supabase_config():
    """Setup Supabase configuration if available"""
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        print("✅ Supabase configuration detected")
        return True
    else:
        print("ℹ️ Supabase configuration not found - using local database only")
        return False

def check_required_environment():
    """Check and setup required environment variables"""
    # Set default SECRET_KEY if not provided
    if not os.environ.get('SECRET_KEY'):
        import secrets
        os.environ['SECRET_KEY'] = secrets.token_hex(32)
        print("⚠️ Generated temporary SECRET_KEY (set SECRET_KEY env var for production)")
    
    # Optional configurations
    optional_vars = [
        'GEMINI_API_KEY',
        'SUPABASE_SERVICE_KEY',
        'SESSION_COOKIE_SECURE'
    ]
    
    for var in optional_vars:
        if os.environ.get(var):
            print(f"✅ {var} configured")
        else:
            print(f"ℹ️ {var} not set (optional)")

def get_app_config():
    """Get complete application configuration for Docker"""
    load_docker_environment()
    check_required_environment()
    
    config = {
        'SECRET_KEY': os.environ.get('SECRET_KEY'),
        'SQLALCHEMY_DATABASE_URI': setup_database_config(),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SESSION_COOKIE_SECURE': os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() == 'true',
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Lax',
        'SUPABASE_AVAILABLE': setup_supabase_config()
    }
    
    print("🚀 Docker configuration complete")
    return config

if __name__ == "__main__":
    # Test configuration
    config = get_app_config()
    print("\n📋 Configuration Summary:")
    for key, value in config.items():
        if 'SECRET' in key or 'PASSWORD' in key:
            print(f"  {key}: {'*' * 8}")
        else:
            print(f"  {key}: {value}")