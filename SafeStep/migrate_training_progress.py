#!/usr/bin/env python3
"""
Database migration script to add missing columns to training_progress table
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment variables"""
    # Try to get DATABASE_URL first (full connection string)
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        print(f"Using DATABASE_URL: {database_url.split('@')[0]}@***")
        return database_url
    else:
        # Fallback to SQLite for local development
        print("No DATABASE_URL found, using SQLite fallback")
        return 'sqlite:///instance/safestep.db'

def migrate_database():
    """Add missing columns to training_progress table"""
    database_url = get_database_url()
    print(f"Connecting to database...")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Check if columns already exist
            if 'postgresql' in database_url:
                # PostgreSQL syntax
                check_status = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'training_progress' 
                    AND column_name = 'status'
                """)).fetchone()
                
                check_video_watched = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'training_progress' 
                    AND column_name = 'video_watched'
                """)).fetchone()
                
                # Add status column if it doesn't exist
                if not check_status:
                    print("Adding 'status' column...")
                    conn.execute(text("""
                        ALTER TABLE training_progress 
                        ADD COLUMN status VARCHAR(20) DEFAULT 'not_started'
                    """))
                    conn.commit()
                    print("✅ Added 'status' column")
                else:
                    print("ℹ️ 'status' column already exists")
                
                # Add video_watched column if it doesn't exist
                if not check_video_watched:
                    print("Adding 'video_watched' column...")
                    conn.execute(text("""
                        ALTER TABLE training_progress 
                        ADD COLUMN video_watched BOOLEAN DEFAULT FALSE
                    """))
                    conn.commit()
                    print("✅ Added 'video_watched' column")
                else:
                    print("ℹ️ 'video_watched' column already exists")
                    
            else:
                # SQLite syntax
                try:
                    conn.execute(text("""
                        ALTER TABLE training_progress 
                        ADD COLUMN status VARCHAR(20) DEFAULT 'not_started'
                    """))
                    print("✅ Added 'status' column")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print("ℹ️ 'status' column already exists")
                    else:
                        raise e
                
                try:
                    conn.execute(text("""
                        ALTER TABLE training_progress 
                        ADD COLUMN video_watched BOOLEAN DEFAULT 0
                    """))
                    print("✅ Added 'video_watched' column")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print("ℹ️ 'video_watched' column already exists")
                    else:
                        raise e
                
                conn.commit()
            
            print("\n🎉 Database migration completed successfully!")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    migrate_database()