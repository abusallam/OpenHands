FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir \
    fastapi>=0.109.0 \
    uvicorn>=0.27.0 \
    python-dotenv>=1.0.0 \
    pydantic>=2.5.0 \
    pydantic-settings>=2.1.0 \
    google-generativeai>=0.3.0 \
    sqlalchemy>=2.0.25 \
    asyncpg>=0.29.0 \
    redis>=5.0.1 \
    python-jose>=3.3.0 \
    passlib>=1.7.4 \
    bcrypt>=4.1.0 \
    python-multipart==0.0.6 \
    httpx>=0.26.0 \
    pytest==7.4.3 \
    pytest-asyncio==0.21.1 \
    black==23.11.0 \
    isort==5.12.0 \
    openai>=1.3.0 \
    anthropic>=0.5.0 \
    transformers>=4.35.0 \
    torch>=2.1.0 \
    python-jose>=3.3.0 \
    passlib>=1.7.4 \
    bcrypt>=4.1.0 \
    python-multipart>=0.0.6 \
    aiohttp>=3.9.0 \
    pytest-cov>=4.1.0 \
    mypy>=1.7.0 \
    pylint>=3.0.2 \
    prometheus-client>=0.17.1 \
    python-json-logger>=2.0.7 \
    jupyter>=1.0.0 \
    ipython>=8.17.2 \
    gitpython>=3.1.40 \
    mkdocs>=1.5.3 \
    mkdocs-material>=9.4.14 \
    python-slugify>=8.0.1 \
    pyyaml>=6.0.1 \
    jinja2>=3.1.2

# Copy the rest of the application
COPY . .

# Expose the new port
EXPOSE 8529

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8529"]
