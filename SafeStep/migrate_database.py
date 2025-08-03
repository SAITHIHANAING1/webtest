#!/usr/bin/env python3
"""
Database migration script to add Supabase integration fields
"""
from app import app, db, User
from sqlalchemy import text

def migrate_database():
    """Add new fields for Supabase integration"""
    with app.app_context():
        try:
            # Check if the column already exists
            with db.engine.connect() as connection:
                result = connection.execute(text("PRAGMA table_info(user)")).fetchall()
                columns = [row[1] for row in result]
                
                if 'supabase_user_id' not in columns:
                    print("Adding supabase_user_id column to user table...")
                    connection.execute(text("ALTER TABLE user ADD COLUMN supabase_user_id VARCHAR(36)"))
                    connection.commit()
                    print("✅ Successfully added supabase_user_id column")
                else:
                    print("ℹ️ supabase_user_id column already exists")
            
            print("✅ Database migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
        
        return True

if __name__ == '__main__':
    print("🔄 Starting database migration...")
    migrate_database()
