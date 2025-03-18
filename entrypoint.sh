#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -c '\q'; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done

echo "PostgreSQL is up - checking database"

# Check if database exists
if ! PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -lqt | cut -d \| -f 1 | grep -qw ai_coder; then
    echo "Creating database ai_coder"
    PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -c "CREATE DATABASE ai_coder;"
fi

# Connect to ai_coder database and create tables
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -d ai_coder -c "
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8529 --proxy-headers --forwarded-allow-ips "*" 