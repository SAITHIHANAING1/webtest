#!/usr/bin/env python3
"""
Database migration script to update schema and fix demo user passwords
Run this after cloning the repository or when database schema changes
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def migrate_database():
    """Apply database migrations"""
    db_path = os.path.join('..', 'instance', 'safestep.db')
    # Also try the local path if the relative path doesn't work
    if not os.path.exists(db_path):
        db_path = 'safestep.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print("❌ Database file not found. Please run the app first to create it.")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔄 Starting database migration...")
        
        # Check if patient_id column exists
        cursor.execute("PRAGMA table_info(seizure_session)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'patient_id' not in columns:
            print("➕ Adding patient_id column to seizure_session table...")
            cursor.execute("ALTER TABLE seizure_session ADD COLUMN patient_id INTEGER")
            print("✅ patient_id column added successfully")
        else:
            print("ℹ️  patient_id column already exists")
        
        # Fix demo user passwords
        demo_users = [
            ('demo', 'demo123'),
            ('admin', 'admin123'),
            ('caregiver', 'caregiver123')
        ]
        
        print("🔐 Updating demo user passwords...")
        for username, password in demo_users:
            # Check if user exists
            cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
            if cursor.fetchone():
                new_hash = generate_password_hash(password)
                cursor.execute("UPDATE user SET password_hash = ? WHERE username = ?", 
                             (new_hash, username))
                print(f"✅ Updated password for user: {username}")
        
        conn.commit()
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_demo_users_if_missing():
    """Create demo users if they don't exist"""
    db_path = os.path.join('..', 'instance', 'safestep.db')
    
    if not os.path.exists(db_path):
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    demo_users = [
        ('admin', 'admin@demo.com', 'admin123', 'Admin', 'User', 'admin'),
        ('demo', 'caregiver@demo.com', 'demo123', 'Demo', 'Caregiver', 'caregiver'),
        ('caregiver', 'caregiver2@demo.com', 'caregiver123', 'Test', 'Caregiver', 'caregiver')
    ]
    
    try:
        for username, email, password, first_name, last_name, role in demo_users:
            # Check if user exists
            cursor.execute("SELECT id FROM user WHERE username = ?", (username,))
            if not cursor.fetchone():
                password_hash = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO user (username, email, password_hash, first_name, last_name, role, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                """, (username, email, password_hash, first_name, last_name, role))
                print(f"✅ Created demo user: {username}")
        
        conn.commit()
    except Exception as e:
        print(f"❌ Error creating demo users: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 SafeStep Database Migration Tool")
    print("=" * 40)
    
    if migrate_database():
        create_demo_users_if_missing()
        print("\n🎉 Migration completed! You can now run the application.")
        print("\nDemo login credentials:")
        print("- Admin: username=admin, password=admin123")
        print("- Caregiver: username=demo, password=demo123")
        print("- Caregiver: username=caregiver, password=caregiver123")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
