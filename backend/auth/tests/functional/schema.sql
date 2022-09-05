CREATE SCHEMA IF NOT EXISTS auth_etube;

CREATE TABLE IF NOT EXISTS auth_etube.users (
    id UUID PRIMARY KEY,
    login TEXT NOT NULL,
    password TEXT,
    email TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE UNIQUE INDEX IF NOT EXISTS user_email_idx ON auth_etube.users(email);

CREATE TABLE IF NOT EXISTS auth_etube.roles (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE UNIQUE INDEX IF NOT EXISTS role_title_idx ON auth_etube.roles(title);

CREATE TABLE IF NOT EXISTS auth_etube.permissions (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    http_method TEXT,
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
CREATE UNIQUE INDEX IF NOT EXISTS permission_title_idx ON auth_etube.permissions(title);

CREATE TABLE IF NOT EXISTS auth_etube.role_permissions (
    id UUID PRIMARY KEY,
    role_id UUID NOT NULL REFERENCES auth_etube.roles ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES auth_etube.permissions ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 

CREATE TABLE IF NOT EXISTS auth_etube.user_roles (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth_etube.users ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES auth_etube.roles ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 

CREATE TABLE IF NOT EXISTS auth_etube.sign_in_history (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth_etube.users ON DELETE CASCADE,
    os TEXT,
    device TEXT,
    browser TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 

CREATE TABLE IF NOT EXISTS auth_etube.user_socials (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    user_service_id TEXT,
    email TEXT,
    service_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
); 
