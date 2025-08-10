#!/usr/bin/env python3
"""
Complete migration script to add missing columns to safety_zone table
This fixes both zone_type and status column errors
"""

import os
import sys
from datetime import datetime
import psycopg2
from urllib.parse import urlparse

# Add the current directory to Python path
# sys.path.append(os.path.dirname(__file__))  # Commented out to avoid importing app.py

def load_config():
    """Load database configuration from config.env"""
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), 'config.env')
    
    if not os.path.exists(config_path):
        print("❌ config.env file not found!")
        return None
    
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key] = value
    
    return config

def get_db_connection():
    """Get database connection from config"""
    config = load_config()
    if not config or 'DATABASE_URL' not in config:
        print("❌ DATABASE_URL not found in config.env")
        return None
    
    try:
        # Parse the DATABASE_URL
        url = urlparse(config['DATABASE_URL'])
        
        conn = psycopg2.connect(
            host=url.hostname,
            port=url.port,
            database=url.path[1:],  # Remove leading '/'
            user=url.username,
            password=url.password
        )
        
        return conn
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return None

def check_columns_exist(conn):
    """Check which columns exist in safety_zone table"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'safety_zone' AND column_name IN ('zone_type', 'status');
        """)
        
        existing_columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return existing_columns
    except Exception as e:
        print(f"❌ Error checking columns: {e}")
        return []

def add_missing_columns(conn):
    """Add missing columns to safety_zone table"""
    try:
        existing_columns = check_columns_exist(conn)
        cursor = conn.cursor()
        
        columns_added = []
        
        # Add zone_type column if missing
        if 'zone_type' not in existing_columns:
            print("➕ Adding zone_type column...")
            cursor.execute("""
                ALTER TABLE safety_zone 
                ADD COLUMN zone_type VARCHAR(20) DEFAULT 'safe';
            """)
            
            # Update existing records
            cursor.execute("""
                UPDATE safety_zone 
                SET zone_type = 'safe' 
                WHERE zone_type IS NULL;
            """)
            columns_added.append('zone_type')
            print("✅ zone_type column added successfully")
        
        # Add status column if missing
        if 'status' not in existing_columns:
            print("➕ Adding status column...")
            cursor.execute("""
                ALTER TABLE safety_zone 
                ADD COLUMN status VARCHAR(20) DEFAULT 'approved';
            """)
            
            # Update existing records
            cursor.execute("""
                UPDATE safety_zone 
                SET status = 'approved' 
                WHERE status IS NULL;
            """)
            columns_added.append('status')
            print("✅ status column added successfully")
        
        if columns_added:
            conn.commit()
            print(f"🎉 Successfully added columns: {', '.join(columns_added)}")
        else:
            print("ℹ️ All required columns already exist")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding columns: {e}")
        conn.rollback()
        return False

def verify_migration(conn):
    """Verify that all required columns exist"""
    try:
        existing_columns = check_columns_exist(conn)
        required_columns = ['zone_type', 'status']
        
        missing_columns = [col for col in required_columns if col not in existing_columns]
        
        if not missing_columns:
            print("✅ Migration verification passed - all required columns exist")
            return True
        else:
            print(f"❌ Migration verification failed - missing columns: {', '.join(missing_columns)}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

def main():
    """Main migration function"""
    print("🔄 Starting SafeStep complete database migration...")
    print(f"📅 Migration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get database connection
    conn = get_db_connection()
    if not conn:
        print("❌ Migration failed: Could not connect to database")
        return False
    
    try:
        # Check current state
        existing_columns = check_columns_exist(conn)
        required_columns = ['zone_type', 'status']
        missing_columns = [col for col in required_columns if col not in existing_columns]
        
        if not missing_columns:
            print("✅ All required columns already exist in safety_zone table")
            print("🎉 No migration needed!")
            return True
        
        print(f"🔍 Missing columns found: {', '.join(missing_columns)}")
        
        # Add missing columns
        if add_missing_columns(conn):
            # Verify the migration
            if verify_migration(conn):
                print("🎉 Migration completed successfully!")
                print("👥 Your friends can now clone the repo and sign up without errors")
                return True
            else:
                print("❌ Migration verification failed")
                return False
        else:
            print("❌ Migration failed")
            return False
            
    finally:
        conn.close()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Complete migration finished successfully!")
        print("You can now run your Flask app without column errors.")
    else:
        print("\n❌ Migration failed!")
        print("Please check the error messages above and try again.")
    
    input("\nPress Enter to exit...")
