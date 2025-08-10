# SafeStep Database Migration Guide

## Problem Solved
This migration fixes the PostgreSQL database column errors that occurred when signing up as a caregiver:
- `column safety_zone.zone_type does not exist`
- `column safety_zone.status does not exist`

## Quick Setup for New Users

If you're cloning this repository for the first time, follow these steps:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd webtest/SafeStep
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
- Copy `config.env.example` to `config.env` (if exists)
- Or create `config.env` with your Supabase credentials:
```
DATABASE_URL=postgresql://username:password@host:port/database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 4. Run Database Migration
```bash
python migrate_safety_zone_complete.py
```

### 5. Start the Application
```bash
python app.py
```

The app will be available at: http://127.0.0.1:5000

## Migration Details

The migration script (`migrate_safety_zone_complete.py`) adds the following columns to the `safety_zone` table:
- `zone_type` VARCHAR(20) DEFAULT 'safe'
- `status` VARCHAR(20) DEFAULT 'approved'

## Troubleshooting

### Error: "config.env file not found"
Create a `config.env` file with your database credentials.

### Error: "DATABASE_URL not found"
Make sure your `config.env` file contains the correct DATABASE_URL.

### Error: "Failed to connect to database"
Verify your Supabase credentials and network connection.

## Files Added/Modified
- `migrate_safety_zone_complete.py` - Complete migration script
- `DATABASE_SETUP.md` - This guide

## Success Indicators
✅ Migration completed successfully!
✅ Flask app starts without column errors
✅ Caregiver dashboard loads without issues
✅ All database operations work properly

## Support
If you encounter any issues:
1. Check that all required columns exist in your database
2. Verify your `config.env` file has correct credentials
3. Run the migration script again if needed

The migration script is safe to run multiple times - it will only add missing columns.
