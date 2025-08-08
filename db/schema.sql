-- Supabase/PostgreSQL schema for the LinkedIn Automation Platform

-- User Management
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    subscription_tier TEXT
);

-- Job Management
CREATE TABLE IF NOT EXISTS search_jobs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    startup_url TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analysis_results (
    id UUID PRIMARY KEY,
    job_id UUID REFERENCES search_jobs(id),
    provider TEXT NOT NULL,
    response_data JSONB,
    score NUMERIC
);

-- Smart-Money Radar v4 Tables
CREATE TABLE IF NOT EXISTS prompt_runs (
    id UUID PRIMARY KEY,
    job_id UUID REFERENCES search_jobs(id),
    provider TEXT NOT NULL,
    prompt_template TEXT,
    response JSONB,
    cost NUMERIC
);

CREATE TABLE IF NOT EXISTS prompt_templates (
    id UUID PRIMARY KEY,
    provider TEXT NOT NULL,
    template_type TEXT,
    content TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS investor_watchlist (
    id UUID PRIMARY KEY,
    investor_name TEXT,
    firm TEXT,
    linkedin_url TEXT,
    added_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS liquidity_events (
    id UUID PRIMARY KEY,
    investor_id UUID REFERENCES investor_watchlist(id),
    event_type TEXT,
    description TEXT,
    detected_date DATE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_search_jobs_user ON search_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_prompt_runs_job ON prompt_runs(job_id);
CREATE INDEX IF NOT EXISTS idx_analysis_results_job ON analysis_results(job_id);

