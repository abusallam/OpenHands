FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages with compatible versions
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn==0.27.0 \
    python-dotenv==1.0.0 \
    sqlalchemy==1.4.42 \
    asyncpg==0.29.0 \
    databases==0.8.0 \
    psycopg2-binary==2.9.9 \
    passlib[bcrypt]==1.7.4 \
    PyJWT==2.8.0 \
    python-jose[cryptography]==3.3.0 \
    jinja2==3.1.2 \
    aiofiles==23.2.1 \
    python-multipart==0.0.6

# Create directories
RUN mkdir -p static/css static/js templates

# Copy application files
COPY static/ static/
COPY templates/ templates/
COPY main.py .
COPY init.sql .

# Verify JWT installation
RUN python -c "import jwt; print('JWT package installed successfully')"

# Set environment variables
ENV ADMIN_USERNAME=${ADMIN_USERNAME:-admin}
ENV ADMIN_EMAIL=${ADMIN_EMAIL:-admin@aicoder.com}
ENV ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin}
ENV ADMIN_TOKEN_SECRET=${ADMIN_TOKEN_SECRET:-your_secret_key_here}

# Create entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8529

ENTRYPOINT ["./entrypoint.sh"]
