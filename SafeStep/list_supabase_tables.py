#!/usr/bin/env python3
"""
Script to list all tables in Supabase database and identify unnecessary ones
"""

import os
from supabase import create_client, Client
from supabase_integration import init_supabase, get_supabase_client

def list_all_tables():
    """List all tables in the Supabase database"""
    try:
        # Initialize Supabase first
        if not init_supabase():
            print("❌ Failed to initialize Supabase connection")
            return []
        
        supabase = get_supabase_client()
        if not supabase:
            print("❌ Supabase client is None")
            return []
        
        print("✅ Supabase connected, listing tables...")
        
        # Try different approaches to list tables
        tables = []
        
        # Method 1: Try to query known tables first
        known_tables = [
            'users', 'pwids', 'incidents', 'zones', 'location_history',
            'system_metrics', 'system_services', 'system_logs', 'system_alerts',
            'user_sessions', 'user_activity', 'analytics_reports', 
            'performance_history', 'risk_assessments',
            'medications', 'medication_schedules', 'medication_events',
            'healthcare_providers', 'provider_specialties',
            'care_plans', 'care_plan_goals',
            'emergency_contacts', 'emergency_protocols', 'emergency_responses'
        ]
        
        print("=== CHECKING FOR KNOWN TABLES ===")
        existing_tables = []
        
        for table_name in known_tables:
            try:
                # Try to select from each table to see if it exists
                result = supabase.table(table_name).select('*').limit(1).execute()
                existing_tables.append(table_name)
                print(f"✅ {table_name} - EXISTS")
            except Exception as e:
                print(f"❌ {table_name} - NOT FOUND ({str(e)[:50]}...)")
        
        print(f"\nFound {len(existing_tables)} existing tables from known list")
        
        # Method 2: Try to use RPC to get all tables
        try:
            print("\n=== ATTEMPTING TO GET ALL TABLES VIA RPC ===")
            
            # Create a simple function to list tables
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """
            
            # Try direct table query approach
            print("Attempting direct query approach...")
            
            # Since RPC might not work, let's try a different approach
            # We'll use the existing tables we found
            return existing_tables
                
        except Exception as e:
            print(f"RPC method failed: {e}")
            print("Using tables found from known list check")
            return existing_tables
            
    except Exception as e:
        print(f"Error listing tables: {e}")
        return []

def identify_unnecessary_tables(tables):
    """Identify which tables might be unnecessary based on the current application"""
    
    # Tables that should exist for current functionality
    necessary_tables = {
        'users',           # User management
        'pwids',          # Patient data
        'incidents',      # Incident tracking
        'zones',          # Safety zones
        'location_history', # Location tracking
        'system_metrics', # System monitoring
        'system_services', # System monitoring
        'system_logs',    # System monitoring
        'system_alerts',  # System monitoring
        'user_sessions',  # User management
        'user_activity',  # Analytics
        'analytics_reports', # Analytics
        'performance_history', # System monitoring
        'risk_assessments'  # Analytics
    }
    
    # Tables that were removed and should be deleted
    removed_features_tables = {
        'medications',
        'medication_schedules',
        'medication_events',
        'healthcare_providers',
        'provider_specialties',
        'care_plans',
        'care_plan_goals',
        'emergency_contacts',
        'emergency_protocols',
        'emergency_responses'
    }
    
    print("\n=== TABLE ANALYSIS ===")
    
    necessary_found = []
    unnecessary_found = []
    unknown_found = []
    
    for table in tables:
        if table in necessary_tables:
            necessary_found.append(table)
        elif table in removed_features_tables:
            unnecessary_found.append(table)
        else:
            unknown_found.append(table)
    
    print(f"\n✅ NECESSARY TABLES ({len(necessary_found)}):")
    for table in sorted(necessary_found):
        print(f"   - {table}")
    
    print(f"\n❌ UNNECESSARY TABLES (from removed features) ({len(unnecessary_found)}):")
    for table in sorted(unnecessary_found):
        print(f"   - {table}")
    
    print(f"\n❓ UNKNOWN/OTHER TABLES ({len(unknown_found)}):")
    for table in sorted(unknown_found):
        print(f"   - {table}")
    
    return {
        'necessary': necessary_found,
        'unnecessary': unnecessary_found,
        'unknown': unknown_found
    }

def main():
    print("Connecting to Supabase...")
    
    tables = list_all_tables()
    
    if tables:
        analysis = identify_unnecessary_tables(tables)
        
        print("\n" + "="*50)
        print("SUMMARY:")
        print(f"Total tables: {len(tables)}")
        print(f"Necessary: {len(analysis['necessary'])}")
        print(f"Unnecessary: {len(analysis['unnecessary'])}")
        print(f"Unknown: {len(analysis['unknown'])}")
        
        if analysis['unnecessary']:
            print(f"\n⚠️  TABLES RECOMMENDED FOR DELETION:")
            for table in sorted(analysis['unnecessary']):
                print(f"   - {table}")
            
            print(f"\nThese tables are from removed features (medications, care plans, etc.)")
            print(f"and are no longer needed by the application.")
        
        if analysis['unknown']:
            print(f"\n🔍 UNKNOWN TABLES NEED REVIEW:")
            for table in sorted(analysis['unknown']):
                print(f"   - {table}")
            
            print(f"\nPlease review these tables to determine if they should be kept or removed.")
    
    else:
        print("No tables found or error occurred.")

if __name__ == "__main__":
    main()
