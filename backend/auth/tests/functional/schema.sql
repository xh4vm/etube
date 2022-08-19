CREATE SCHEMA IF NOT EXISTS auth;

CREATE TABLE IF NOT EXISTS auth.users (
    id UUID PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT,
    email TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE UNIQUE INDEX IF NOT EXISTS user_email_idx ON auth.users(email);

CREATE TABLE IF NOT EXISTS auth.roles (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE UNIQUE INDEX IF NOT EXISTS role_title_idx ON auth.roles(title);

CREATE TABLE IF NOT EXISTS auth.permissions (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    http_method TEXT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE UNIQUE INDEX IF NOT EXISTS permission_title_idx ON auth.permissions(title);

CREATE TABLE IF NOT EXISTS auth.role_permissions (
    id UUID PRIMARY KEY,
    role_id UUID NOT NULL REFERENCES auth.roles ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES auth.permissions ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 

CREATE TABLE IF NOT EXISTS auth.user_roles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES auth.roles ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 

CREATE TABLE IF NOT EXISTS auth.sign_in_history (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users ON DELETE CASCADE,
    os TEXT,
    device TEXT,
    browser TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
