-- Initialize database schema and initial data
CREATE TABLE IF NOT EXISTS ai_tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    configuration JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Add any other necessary tables 