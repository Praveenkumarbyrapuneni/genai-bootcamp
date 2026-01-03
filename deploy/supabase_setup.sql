-- Supabase SQL Setup for CareerPath AI Activity Tracking
-- Run this in your Supabase Dashboard > SQL Editor

-- Table 1: User Searches - Tracks what users search for
CREATE TABLE IF NOT EXISTS user_searches (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_email TEXT,
    target_role TEXT NOT NULL,
    current_skills JSONB DEFAULT '[]',
    timeframe TEXT,
    resume_uploaded BOOLEAN DEFAULT FALSE,
    searched_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 2: User Activity - Tracks logins, page views, etc.
CREATE TABLE IF NOT EXISTS user_activity (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_email TEXT,
    activity_type TEXT NOT NULL,
    details JSONB DEFAULT '{}',
    activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_user_searches_user_id ON user_searches(user_id);
CREATE INDEX IF NOT EXISTS idx_user_searches_searched_at ON user_searches(searched_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_activity_user_id ON user_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activity_activity_at ON user_activity(activity_at DESC);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE user_searches ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;

-- Policy to allow insert for authenticated users
CREATE POLICY "Allow insert for all" ON user_searches FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow insert for all" ON user_activity FOR INSERT WITH CHECK (true);

-- Policy to allow read for all (or restrict to admins if needed)
CREATE POLICY "Allow read for all" ON user_searches FOR SELECT USING (true);
CREATE POLICY "Allow read for all" ON user_activity FOR SELECT USING (true);
