FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-dotenv \
    sqlalchemy \
    asyncpg \
    alembic \
    psycopg2-binary

# Copy application files
COPY . .

# Expose port
EXPOSE 8529

# Create entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
