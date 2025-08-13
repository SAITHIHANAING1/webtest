-- SafeStep Supabase Database Migration Script
-- This script creates all new tables, functions, and views for the enhanced SafeStep application

-- ============================================================================
-- 1. MEDICATIONS MANAGEMENT TABLES
-- ============================================================================

-- Medications table
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
);

-- Medication logs table
CREATE TABLE IF NOT EXISTS medication_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    medication_id UUID REFERENCES medications(id) ON DELETE CASCADE,
    taken_at TIMESTAMP WITH TIME ZONE NOT NULL,
    dosage_taken VARCHAR(100),
    notes TEXT,
    missed BOOLEAN DEFAULT FALSE,
    side_effects_experienced TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- 2. HEALTHCARE PROVIDERS MANAGEMENT TABLES
-- ============================================================================

-- Healthcare providers table
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
);

-- Patient-provider assignments table
CREATE TABLE IF NOT EXISTS patient_provider_assignments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
    provider_id UUID REFERENCES healthcare_providers(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL, -- 'primary', 'specialist', 'emergency', 'consultant'
    assigned_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(patient_id, provider_id, relationship_type)
);

-- ============================================================================
-- 3. CARE PLANS MANAGEMENT TABLES
-- ============================================================================

-- Care plans table
CREATE TABLE IF NOT EXISTS care_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
    provider_id UUID REFERENCES healthcare_providers(id),
    plan_name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed', 'paused', 'cancelled'
    goals JSONB,
    interventions JSONB,
    progress_notes TEXT,
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'urgent'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Care plan tasks table
CREATE TABLE IF NOT EXISTS care_plan_tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    care_plan_id UUID REFERENCES care_plans(id) ON DELETE CASCADE,
    task_name VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'urgent'
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'cancelled'
    assigned_to VARCHAR(100),
    completion_notes TEXT,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- 4. EMERGENCY CONTACTS & RESPONSE TABLES
-- ============================================================================

-- Emergency contacts table
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
);

-- Emergency response plans table
CREATE TABLE IF NOT EXISTS emergency_response_plans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
    plan_name VARCHAR(255) NOT NULL,
    trigger_conditions JSONB NOT NULL,
    response_steps JSONB NOT NULL,
    escalation_timeline JSONB,
    medical_information TEXT,
    special_instructions TEXT,
    emergency_medications JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Emergency alerts table
CREATE TABLE IF NOT EXISTS emergency_alerts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
    incident_id UUID REFERENCES incidents(id),
    alert_type VARCHAR(50) NOT NULL, -- 'seizure', 'fall', 'medication', 'zone_breach', 'medical_emergency'
    severity VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    message TEXT NOT NULL,
    contacts_notified JSONB,
    response_actions JSONB,
    location_data JSONB,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(255),
    resolution_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- 5. ENHANCED ANALYTICS TABLES
-- ============================================================================

-- Analytics reports table
CREATE TABLE IF NOT EXISTS analytics_reports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL,
    report_type VARCHAR(50) NOT NULL, -- 'patient_summary', 'medication_adherence', 'incident_analysis', 'care_plan_progress'
    report_name VARCHAR(255) NOT NULL,
    parameters JSONB NOT NULL,
    generated_data JSONB,
    file_path VARCHAR(500),
    file_size_bytes BIGINT,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'generating', 'completed', 'failed'
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Prediction results table
CREATE TABLE IF NOT EXISTS prediction_results (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id UUID REFERENCES pwids(id) ON DELETE CASCADE,
    model_version VARCHAR(50) NOT NULL,
    risk_score DECIMAL(5,2) NOT NULL,
    confidence_level DECIMAL(5,2) NOT NULL,
    risk_factors JSONB,
    recommendations JSONB,
    input_features JSONB,
    prediction_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    valid_until TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(255)
);

-- Feature usage logs table
CREATE TABLE IF NOT EXISTS feature_usage_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL,
    feature_name VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'view', 'create', 'update', 'delete', 'export'
    metadata JSONB,
    session_id VARCHAR(255),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- 6. INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Medications indexes
CREATE INDEX IF NOT EXISTS idx_medications_patient_id ON medications(patient_id);
CREATE INDEX IF NOT EXISTS idx_medications_active ON medications(patient_id, is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_medications_dates ON medications(start_date, end_date);

-- Medication logs indexes
CREATE INDEX IF NOT EXISTS idx_medication_logs_medication_id ON medication_logs(medication_id);
CREATE INDEX IF NOT EXISTS idx_medication_logs_taken_at ON medication_logs(taken_at DESC);
CREATE INDEX IF NOT EXISTS idx_medication_logs_patient_date ON medication_logs(medication_id, taken_at DESC);

-- Healthcare providers indexes
CREATE INDEX IF NOT EXISTS idx_providers_specialty ON healthcare_providers(specialty);
CREATE INDEX IF NOT EXISTS idx_providers_active ON healthcare_providers(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_providers_name ON healthcare_providers USING gin(to_tsvector('english', name));

-- Patient-provider assignments indexes
CREATE INDEX IF NOT EXISTS idx_patient_provider_patient_id ON patient_provider_assignments(patient_id);
CREATE INDEX IF NOT EXISTS idx_patient_provider_provider_id ON patient_provider_assignments(provider_id);
CREATE INDEX IF NOT EXISTS idx_patient_provider_active ON patient_provider_assignments(patient_id, is_active) WHERE is_active = true;

-- Care plans indexes
CREATE INDEX IF NOT EXISTS idx_care_plans_patient_id ON care_plans(patient_id);
CREATE INDEX IF NOT EXISTS idx_care_plans_status ON care_plans(status);
CREATE INDEX IF NOT EXISTS idx_care_plans_dates ON care_plans(start_date, end_date);

-- Care plan tasks indexes
CREATE INDEX IF NOT EXISTS idx_care_plan_tasks_plan_id ON care_plan_tasks(care_plan_id);
CREATE INDEX IF NOT EXISTS idx_care_plan_tasks_status ON care_plan_tasks(status);
CREATE INDEX IF NOT EXISTS idx_care_plan_tasks_due_date ON care_plan_tasks(due_date);

-- Emergency contacts indexes
CREATE INDEX IF NOT EXISTS idx_emergency_contacts_patient_id ON emergency_contacts(patient_id);
CREATE INDEX IF NOT EXISTS idx_emergency_contacts_priority ON emergency_contacts(patient_id, priority_order);

-- Emergency alerts indexes
CREATE INDEX IF NOT EXISTS idx_emergency_alerts_patient_id ON emergency_alerts(patient_id);
CREATE INDEX IF NOT EXISTS idx_emergency_alerts_unresolved ON emergency_alerts(created_at DESC) WHERE resolved_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_emergency_alerts_type_severity ON emergency_alerts(alert_type, severity);

-- Analytics indexes
CREATE INDEX IF NOT EXISTS idx_prediction_results_patient_date ON prediction_results(patient_id, prediction_date DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_reports_user_type ON analytics_reports(user_id, report_type);
CREATE INDEX IF NOT EXISTS idx_feature_usage_logs_user_feature ON feature_usage_logs(user_id, feature_name, created_at DESC);

-- Existing tables indexes (if not already present)
CREATE INDEX IF NOT EXISTS idx_incidents_patient_date ON incidents(patient_id, incident_date DESC);
CREATE INDEX IF NOT EXISTS idx_pwids_name ON pwids USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_safety_zone_patient ON safety_zone(patient_id);

-- ============================================================================
-- 7. DATABASE FUNCTIONS
-- ============================================================================

-- Function to calculate medication adherence
CREATE OR REPLACE FUNCTION calculate_medication_adherence(
    patient_uuid UUID,
    start_date DATE,
    end_date DATE
)
RETURNS DECIMAL(5,2) AS $$
DECLARE
    total_expected INTEGER := 0;
    total_taken INTEGER := 0;
    adherence_rate DECIMAL(5,2);
    med_record RECORD;
BEGIN
    -- Calculate for each active medication
    FOR med_record IN 
        SELECT id, frequency, start_date as med_start, COALESCE(end_date, end_date) as med_end
        FROM medications 
        WHERE patient_id = patient_uuid 
          AND start_date <= end_date
          AND (end_date IS NULL OR end_date >= start_date)
          AND is_active = true
    LOOP
        -- Calculate expected doses based on frequency
        -- Simplified: assume frequency contains number (e.g., "2 times daily" = 2)
        DECLARE
            frequency_per_day INTEGER := 1;
            days_in_period INTEGER;
            med_start_calc DATE;
            med_end_calc DATE;
        BEGIN
            -- Extract frequency number (simplified)
            IF med_record.frequency ILIKE '%twice%' OR med_record.frequency ILIKE '%2%' THEN
                frequency_per_day := 2;
            ELSIF med_record.frequency ILIKE '%three%' OR med_record.frequency ILIKE '%3%' THEN
                frequency_per_day := 3;
            ELSIF med_record.frequency ILIKE '%four%' OR med_record.frequency ILIKE '%4%' THEN
                frequency_per_day := 4;
            END IF;
            
            -- Calculate actual period for this medication
            med_start_calc := GREATEST(med_record.med_start, start_date);
            med_end_calc := LEAST(COALESCE(med_record.med_end, end_date), end_date);
            
            IF med_end_calc >= med_start_calc THEN
                days_in_period := med_end_calc - med_start_calc + 1;
                total_expected := total_expected + (days_in_period * frequency_per_day);
                
                -- Count actual doses taken
                SELECT COUNT(*) INTO total_taken
                FROM medication_logs ml
                WHERE ml.medication_id = med_record.id
                  AND ml.taken_at::date BETWEEN med_start_calc AND med_end_calc
                  AND ml.missed = false;
            END IF;
        END;
    END LOOP;
    
    -- Calculate adherence rate
    IF total_expected > 0 THEN
        adherence_rate := (total_taken::DECIMAL / total_expected::DECIMAL) * 100;
    ELSE
        adherence_rate := 0;
    END IF;
    
    RETURN ROUND(LEAST(adherence_rate, 100.00), 2);
END;
$$ LANGUAGE plpgsql;

-- Function to get patient risk summary
CREATE OR REPLACE FUNCTION get_patient_risk_summary(patient_uuid UUID)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT jsonb_build_object(
        'patient_id', patient_uuid,
        'latest_risk_score', (
            SELECT risk_score FROM prediction_results 
            WHERE patient_id = patient_uuid 
            ORDER BY prediction_date DESC LIMIT 1
        ),
        'latest_confidence', (
            SELECT confidence_level FROM prediction_results 
            WHERE patient_id = patient_uuid 
            ORDER BY prediction_date DESC LIMIT 1
        ),
        'incident_count_7d', (
            SELECT COUNT(*) FROM incidents 
            WHERE patient_id = patient_uuid 
              AND incident_date >= CURRENT_DATE - INTERVAL '7 days'
        ),
        'incident_count_30d', (
            SELECT COUNT(*) FROM incidents 
            WHERE patient_id = patient_uuid 
              AND incident_date >= CURRENT_DATE - INTERVAL '30 days'
        ),
        'medication_adherence_30d', calculate_medication_adherence(
            patient_uuid, 
            CURRENT_DATE - INTERVAL '30 days', 
            CURRENT_DATE
        ),
        'last_incident_date', (
            SELECT MAX(incident_date) FROM incidents 
            WHERE patient_id = patient_uuid
        ),
        'active_medications_count', (
            SELECT COUNT(*) FROM medications 
            WHERE patient_id = patient_uuid 
              AND is_active = true
              AND (end_date IS NULL OR end_date >= CURRENT_DATE)
        ),
        'active_care_plans_count', (
            SELECT COUNT(*) FROM care_plans 
            WHERE patient_id = patient_uuid 
              AND status = 'active'
        ),
        'unresolved_alerts_count', (
            SELECT COUNT(*) FROM emergency_alerts 
            WHERE patient_id = patient_uuid 
              AND resolved_at IS NULL
        )
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to update medication adherence scores
CREATE OR REPLACE FUNCTION update_medication_adherence_scores()
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER := 0;
    med_record RECORD;
BEGIN
    FOR med_record IN 
        SELECT id, patient_id FROM medications WHERE is_active = true
    LOOP
        UPDATE medications 
        SET adherence_score = calculate_medication_adherence(
            med_record.patient_id,
            CURRENT_DATE - INTERVAL '30 days',
            CURRENT_DATE
        ),
        updated_at = NOW()
        WHERE id = med_record.id;
        
        updated_count := updated_count + 1;
    END LOOP;
    
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 8. VIEWS FOR ANALYTICS
-- ============================================================================

-- Patient dashboard view
CREATE OR REPLACE VIEW patient_dashboard_view AS
SELECT 
    p.id,
    p.name,
    p.age,
    p.gender,
    p.email,
    p.phone,
    get_patient_risk_summary(p.id) as risk_summary,
    (
        SELECT COUNT(*) FROM incidents i 
        WHERE i.patient_id = p.id 
          AND i.incident_date >= CURRENT_DATE - INTERVAL '7 days'
    ) as incidents_7d,
    (
        SELECT COUNT(*) FROM incidents i 
        WHERE i.patient_id = p.id 
          AND i.incident_date >= CURRENT_DATE - INTERVAL '30 days'
    ) as incidents_30d,
    (
        SELECT COUNT(*) FROM medications m 
        WHERE m.patient_id = p.id 
          AND m.is_active = true
          AND (m.end_date IS NULL OR m.end_date >= CURRENT_DATE)
    ) as active_medications,
    (
        SELECT COUNT(*) FROM care_plans cp 
        WHERE cp.patient_id = p.id 
          AND cp.status = 'active'
    ) as active_care_plans,
    (
        SELECT hp.name FROM healthcare_providers hp
        JOIN patient_provider_assignments ppa ON hp.id = ppa.provider_id
        WHERE ppa.patient_id = p.id 
          AND ppa.relationship_type = 'primary' 
          AND ppa.is_active = true
        LIMIT 1
    ) as primary_provider,
    (
        SELECT COUNT(*) FROM emergency_alerts ea
        WHERE ea.patient_id = p.id 
          AND ea.resolved_at IS NULL
    ) as unresolved_alerts
FROM pwids p;

-- Medication adherence trends view
CREATE OR REPLACE VIEW medication_adherence_trends AS
SELECT 
    m.patient_id,
    m.medication_name,
    m.dosage,
    DATE_TRUNC('week', ml.taken_at) as week,
    COUNT(CASE WHEN ml.missed = false THEN 1 END) as doses_taken,
    COUNT(*) as total_logged,
    ROUND(
        (COUNT(CASE WHEN ml.missed = false THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0)::DECIMAL) * 100, 
        2
    ) as adherence_percentage
FROM medications m
LEFT JOIN medication_logs ml ON m.id = ml.medication_id
WHERE ml.taken_at >= CURRENT_DATE - INTERVAL '12 weeks'
  AND m.is_active = true
GROUP BY m.patient_id, m.medication_name, m.dosage, DATE_TRUNC('week', ml.taken_at)
ORDER BY m.patient_id, week DESC;

-- Care plan progress view
CREATE OR REPLACE VIEW care_plan_progress_view AS
SELECT 
    cp.id as care_plan_id,
    cp.patient_id,
    cp.plan_name,
    cp.status,
    cp.start_date,
    cp.end_date,
    COUNT(cpt.id) as total_tasks,
    COUNT(CASE WHEN cpt.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN cpt.status = 'pending' THEN 1 END) as pending_tasks,
    COUNT(CASE WHEN cpt.status = 'in_progress' THEN 1 END) as in_progress_tasks,
    ROUND(
        (COUNT(CASE WHEN cpt.status = 'completed' THEN 1 END)::DECIMAL / NULLIF(COUNT(cpt.id), 0)::DECIMAL) * 100,
        2
    ) as completion_percentage
FROM care_plans cp
LEFT JOIN care_plan_tasks cpt ON cp.id = cpt.care_plan_id
GROUP BY cp.id, cp.patient_id, cp.plan_name, cp.status, cp.start_date, cp.end_date;

-- ============================================================================
-- 9. ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on all new tables
ALTER TABLE medications ENABLE ROW LEVEL SECURITY;
ALTER TABLE medication_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE healthcare_providers ENABLE ROW LEVEL SECURITY;
ALTER TABLE patient_provider_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE care_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE care_plan_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE emergency_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE emergency_response_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE emergency_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE prediction_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE feature_usage_logs ENABLE ROW LEVEL SECURITY;

-- Policies for medications (caregivers can only see assigned patients)
CREATE POLICY "medications_caregiver_access" ON medications
    FOR ALL USING (
        patient_id IN (
            SELECT patient_id FROM patient_provider_assignments ppa
            JOIN healthcare_providers hp ON ppa.provider_id = hp.id
            WHERE hp.email = auth.jwt() ->> 'email'
              AND ppa.is_active = true
        )
    );

-- Policies for admin access (can see all)
CREATE POLICY "medications_admin_access" ON medications
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM auth.users 
            WHERE auth.uid() = id 
              AND (raw_user_meta_data->>'role' = 'admin' OR email LIKE '%admin%')
        )
    );

-- Similar policies for other tables (simplified for brevity)
-- In production, create specific policies for each table and user role

-- ============================================================================
-- 10. TRIGGERS FOR AUTOMATIC UPDATES
-- ============================================================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at columns
CREATE TRIGGER update_medications_updated_at
    BEFORE UPDATE ON medications
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_healthcare_providers_updated_at
    BEFORE UPDATE ON healthcare_providers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_care_plans_updated_at
    BEFORE UPDATE ON care_plans
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_care_plan_tasks_updated_at
    BEFORE UPDATE ON care_plan_tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_emergency_contacts_updated_at
    BEFORE UPDATE ON emergency_contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_emergency_response_plans_updated_at
    BEFORE UPDATE ON emergency_response_plans
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 11. SAMPLE DATA INSERTION (OPTIONAL)
-- ============================================================================

-- Insert sample healthcare providers
INSERT INTO healthcare_providers (name, specialty, license_number, phone, email, hospital_affiliation, years_experience)
VALUES 
    ('Dr. Sarah Johnson', 'Neurology', 'NEU001234', '+1-555-0101', 'sarah.johnson@hospital.com', 'Central Medical Center', 15),
    ('Dr. Michael Chen', 'Epileptology', 'EPI005678', '+1-555-0102', 'michael.chen@hospital.com', 'Neurological Institute', 12),
    ('Dr. Emily Rodriguez', 'Emergency Medicine', 'EM009876', '+1-555-0103', 'emily.rodriguez@hospital.com', 'Emergency Care Center', 8)
ON CONFLICT (license_number) DO NOTHING;

-- ============================================================================
-- 12. PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Analyze tables for query optimization
ANALYZE medications;
ANALYZE medication_logs;
ANALYZE healthcare_providers;
ANALYZE patient_provider_assignments;
ANALYZE care_plans;
ANALYZE care_plan_tasks;
ANALYZE emergency_contacts;
ANALYZE emergency_response_plans;
ANALYZE emergency_alerts;
ANALYZE analytics_reports;
ANALYZE prediction_results;
ANALYZE feature_usage_logs;

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Log migration completion
DO $$
BEGIN
    RAISE NOTICE 'SafeStep Supabase migration completed successfully!';
    RAISE NOTICE 'Created tables: medications, medication_logs, healthcare_providers, patient_provider_assignments,';
    RAISE NOTICE '                care_plans, care_plan_tasks, emergency_contacts, emergency_response_plans,';
    RAISE NOTICE '                emergency_alerts, analytics_reports, prediction_results, feature_usage_logs';
    RAISE NOTICE 'Created functions: calculate_medication_adherence, get_patient_risk_summary, update_medication_adherence_scores';
    RAISE NOTICE 'Created views: patient_dashboard_view, medication_adherence_trends, care_plan_progress_view';
    RAISE NOTICE 'Enabled RLS and created performance indexes';
END $$;