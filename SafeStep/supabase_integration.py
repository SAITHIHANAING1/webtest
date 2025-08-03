#!/usr/bin/env python3
"""
Supabase integration for Flask app
This combines Flask-SQLAlchemy with Supabase client features
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Global Supabase client
supabase: Client = None

def init_supabase():
    """Initialize Supabase client"""
    global supabase
    
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    if url and key:
        try:
            supabase = create_client(url, key)
            print("✅ Supabase client initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Supabase client: {e}")
            return False
    else:
        print("ℹ️ Supabase credentials not found, using SQLite fallback")
        return False

def get_supabase_client() -> Client:
    """Get the Supabase client instance"""
    return supabase

def test_supabase_features():
    """Test Supabase-specific features"""
    if not supabase:
        print("❌ Supabase client not initialized")
        return False
    
    try:
        # Test auth capabilities
        session = supabase.auth.get_session()
        print("✅ Supabase auth accessible")
        
        # Test storage capabilities (if you plan to use file uploads)
        buckets = supabase.storage.list_buckets()
        print(f"✅ Supabase storage accessible, buckets: {len(buckets) if buckets else 0}")
        
        return True
    except Exception as e:
        print(f"❌ Supabase features test failed: {e}")
        return False

# Authentication helpers (optional, for future use)
def create_supabase_user(email: str, password: str):
    """Create a user using Supabase auth"""
    if not supabase:
        return None
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        print(f"Error creating Supabase user: {e}")
        return None

def sign_in_supabase_user(email: str, password: str):
    """Sign in a user using Supabase auth"""
    if not supabase:
        return None
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        print(f"Error signing in Supabase user: {e}")
        return None

if __name__ == '__main__':
    print("🧪 Testing Supabase integration...")
    
    if init_supabase():
        test_supabase_features()
        print("🎉 Supabase integration ready!")
    else:
        print("❌ Supabase integration failed - using SQLite fallback")
