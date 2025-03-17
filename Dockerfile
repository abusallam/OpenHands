FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
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
    databases \
    psycopg2-binary \
    jinja2 \
    aiofiles

# Create directories
RUN mkdir -p static/css static/js templates

# Copy application files
COPY static/ static/
COPY templates/ templates/
COPY main.py .
COPY init.sql .

# Create entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8529

ENTRYPOINT ["./entrypoint.sh"]
