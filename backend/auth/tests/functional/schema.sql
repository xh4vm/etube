CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT,
    email TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE INDEX IF NOT EXISTS user_email_idx ON public.users(email);
