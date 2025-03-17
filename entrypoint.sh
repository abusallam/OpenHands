#!/bin/bash

# Wait for PostgreSQL to be ready
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" -c '\q'; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 1
done

echo "PostgreSQL is up - executing database initialization"

# Create database if it doesn't exist
PGPASSWORD=$POSTGRES_PASSWORD psql -h "$DATABASE_HOST" -U "$DATABASE_USER" <<-EOSQL
    SELECT 'CREATE DATABASE ai_coder'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ai_coder');
EOSQL

# Run migrations
alembic upgrade head

# Start the application
exec uvicorn main:app --host 0.0.0.0 --port 8529 --proxy-headers --forwarded-allow-ips "*" 