from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_ANON_KEY'))

tables = ['incidents', 'users', 'reports', 'zones', 'sessions', 'predictions', 'patients']

print("Checking existing tables in SafeStep database:")
print("=" * 50)

for table in tables:
    try:
        result = client.table(table).select('*').limit(1).execute()
        print(f"✓ {table}: {len(result.data)} rows (table exists)")
    except Exception as e:
        print(f"✗ {table}: {str(e)[:80]}...")

print("\nTable check completed.")