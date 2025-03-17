#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h internal_db -p 5432 -U ai_coder; do
    sleep 1
done

# Wait for Redis to be ready
echo "Waiting for Redis..."
while ! redis-cli -h internal_redis -a internal_redis_password ping; do
    sleep 1
done

# Run database migrations if needed
echo "Running database migrations..."
python scripts/db_migrate.py

# Start the application
echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 8000 