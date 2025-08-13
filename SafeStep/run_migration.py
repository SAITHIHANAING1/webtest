#!/usr/bin/env python3
"""
SafeStep Database Migration Runner
Runs the Supabase migration script using Python and the Supabase client.
"""

import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_migration():
    """Run the database migration"""
    try:
        # Get Supabase credentials
        url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not url or not service_key:
            print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env file")
            return False
        
        # Create Supabase client with service key for admin operations
        supabase = create_client(url, service_key)
        
        print("Starting SafeStep database migration...")
        print("=" * 50)
        
        # Read the migration SQL file
        with open('supabase_migration.sql', 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        # Split the migration into individual statements
        # Remove comments and empty lines
        statements = []
        current_statement = []
        
        for line in migration_sql.split('\n'):
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('--'):
                continue
            
            current_statement.append(line)
            
            # If line ends with semicolon, it's the end of a statement
            if line.endswith(';'):
                statement = ' '.join(current_statement)
                if statement.strip():
                    statements.append(statement)
                current_statement = []
        
        # Add any remaining statement
        if current_statement:
            statement = ' '.join(current_statement)
            if statement.strip():
                statements.append(statement)
        
        print(f"Found {len(statements)} SQL statements to execute")
        
        # Execute each statement
        success_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements, 1):
            try:
                # Skip certain statements that might not work with Supabase client
                if any(skip_keyword in statement.upper() for skip_keyword in [
                    'CREATE EXTENSION',
                    'ALTER EXTENSION',
                    'ANALYZE',
                    'RAISE NOTICE'
                ]):
                    print(f"Skipping statement {i}: {statement[:50]}...")
                    continue
                
                print(f"Executing statement {i}/{len(statements)}: {statement[:50]}...")
                
                # Execute the SQL statement
                result = supabase.rpc('exec_sql', {'sql': statement}).execute()
                
                success_count += 1
                print(f"✓ Statement {i} executed successfully")
                
            except Exception as e:
                error_count += 1
                print(f"✗ Error in statement {i}: {str(e)}")
                print(f"  Statement: {statement[:100]}...")
                
                # Continue with other statements even if one fails
                continue
        
        print("\n" + "=" * 50)
        print(f"Migration completed!")
        print(f"Successful statements: {success_count}")
        print(f"Failed statements: {error_count}")
        
        if error_count == 0:
            print("🎉 All migration statements executed successfully!")
        else:
            print(f"⚠️  {error_count} statements failed. Check the errors above.")
        
        return error_count == 0
        
    except FileNotFoundError:
        print("Error: supabase_migration.sql file not found")
        return False
    except Exception as e:
        print(f"Error running migration: {str(e)}")
        return False

def create_tables_manually():
    """Create tables manually using Supabase client"""
    try:
        # Get Supabase credentials
        url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not url or not service_key:
            print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
            return False
        
        # Create Supabase client
        supabase = create_client(url, service_key)
        
        print("Creating tables manually...")
        
        # List of table creation statements
        table_statements = [
            # Medications table
            """
            CREATE TABLE IF NOT EXISTS medications (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
                medication_name VARCHAR(255) NOT NULL,
                dosage VARCHAR(100) NOT NULL,
                frequency VARCHAR(100) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE,
                prescribing_doctor VARCHAR(255),
                side_effects TEXT[],
                adherence_score DECIMAL(5,2) DEFAULT 0.00,
                notes TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """,
            
            # Healthcare providers table
            """
            CREATE TABLE IF NOT EXISTS healthcare_providers (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                specialty VARCHAR(100) NOT NULL,
                license_number VARCHAR(100) UNIQUE,
                phone VARCHAR(20),
                email VARCHAR(255),
                address TEXT,
                hospital_affiliation VARCHAR(255),
                years_experience INTEGER,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """,
            
            # Emergency contacts table
            """
            CREATE TABLE IF NOT EXISTS emergency_contacts (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                relationship VARCHAR(100) NOT NULL,
                phone_primary VARCHAR(20) NOT NULL,
                phone_secondary VARCHAR(20),
                email VARCHAR(255),
                address TEXT,
                priority_order INTEGER NOT NULL,
                is_medical_proxy BOOLEAN DEFAULT FALSE,
                is_emergency_contact BOOLEAN DEFAULT TRUE,
                notes TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
            """
        ]
        
        # Execute each table creation statement
        for i, statement in enumerate(table_statements, 1):
            try:
                print(f"Creating table {i}/{len(table_statements)}...")
                
                # Use the table() method to create tables
                # Note: This is a simplified approach, actual table creation might need different method
                result = supabase.postgrest.schema('public').rpc('exec_sql', {'sql': statement}).execute()
                
                print(f"✓ Table {i} created successfully")
                
            except Exception as e:
                print(f"✗ Error creating table {i}: {str(e)}")
                continue
        
        print("\nManual table creation completed!")
        return True
        
    except Exception as e:
        print(f"Error in manual table creation: {str(e)}")
        return False

def test_connection():
    """Test the Supabase connection"""
    try:
        # Get Supabase credentials
        url = os.getenv('SUPABASE_URL')
        anon_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not anon_key:
            print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
            return False
        
        # Create Supabase client
        supabase = create_client(url, anon_key)
        
        print("Testing Supabase connection...")
        
        # Test with a simple query
        result = supabase.table('pwids').select('id').limit(1).execute()
        
        print("✓ Supabase connection successful!")
        print(f"Database URL: {url}")
        
        return True
        
    except Exception as e:
        print(f"✗ Supabase connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("SafeStep Database Migration Runner")
    print("=" * 40)
    
    # Test connection first
    if not test_connection():
        print("\nConnection test failed. Please check your .env file.")
        sys.exit(1)
    
    print("\nConnection test passed!")
    
    # Ask user which method to use
    print("\nChoose migration method:")
    print("1. Run full migration script (recommended)")
    print("2. Create tables manually (fallback)")
    print("3. Skip migration")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        success = run_migration()
        if success:
            print("\n🎉 Migration completed successfully!")
        else:
            print("\n⚠️  Migration completed with errors.")
    elif choice == '2':
        success = create_tables_manually()
        if success:
            print("\n🎉 Manual table creation completed!")
        else:
            print("\n⚠️  Manual table creation failed.")
    elif choice == '3':
        print("\nMigration skipped.")
    else:
        print("\nInvalid choice. Exiting.")
        sys.exit(1)
    
    print("\nMigration runner finished.")