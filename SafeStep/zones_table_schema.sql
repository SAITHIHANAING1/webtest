-- ✅ COMPLETED: Zones table has been created and configured
-- This file is kept for reference only

-- Zones table schema (already created in Supabase):
CREATE TABLE zones (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    radius DOUBLE PRECISION DEFAULT 100,
    zone_type VARCHAR(20) DEFAULT 'safe',
    status VARCHAR(20) DEFAULT 'approved',
    is_active BOOLEAN DEFAULT true,
    user_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ✅ COMPLETED: Permissions have been granted and RLS disabled
-- ✅ COMPLETED: Sample data has been inserted
