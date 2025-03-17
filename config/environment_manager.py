from typing import Dict, List, Optional
from pathlib import Path
import yaml
from cryptography.fernet import Fernet
import base64
import os

class EnvironmentConfig:
    """
    Comprehensive environment configuration manager.
    
    Features:
    - Multiple environment support
    - Secure credential storage
    - Template generation
    - Validation
    - Auto-discovery
    """

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.env_path = project_path / ".env"
        self.env_template_path = project_path / ".env.template"
        self.encryption_key = self._load_or_create_key()
        self.environments = {
            "development": self._get_dev_config(),
            "staging": self._get_staging_config(),
            "production": self._get_prod_config()
        }

    def generate_env_files(self) -> Dict[str, Path]:
        """Generates environment files for all configurations"""
        generated_files = {}
        
        for env_name, config in self.environments.items():
            env_file = self.project_path / f".env.{env_name}"
            self._write_env_file(env_file, config)
            generated_files[env_name] = env_file
            
        # Create template file
        self._create_template_file()
        
        return generated_files

    def _get_base_config(self) -> Dict[str, str]:
        """Base configuration for all environments"""
        return {
            # Server Configuration
            "SERVER_HOST": "0.0.0.0",
            "SERVER_PORT": "8000",
            "DEBUG": "false",
            "ENVIRONMENT": "",
            "SECRET_KEY": self._generate_secret_key(),
            
            # Database Configuration
            "DATABASE_URL": "",
            "DATABASE_POOL_SIZE": "20",
            "DATABASE_MAX_OVERFLOW": "10",
            
            # AI Model Configuration
            "OPENAI_API_KEY": "",
            "HUGGINGFACE_API_KEY": "",
            "MODEL_CACHE_DIR": "./model_cache",
            "DEFAULT_MODEL": "codegen-16B-mono",
            
            # Authentication
            "JWT_SECRET_KEY": self._generate_secret_key(),
            "JWT_ALGORITHM": "HS256",
            "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
            
            # Redis Configuration
            "REDIS_HOST": "localhost",
            "REDIS_PORT": "6379",
            "REDIS_PASSWORD": "",
            
            # Tool Integration
            "GITHUB_TOKEN": "",
            "DOCKER_REGISTRY": "",
            "KUBERNETES_CONFIG": "",
            
            # Monitoring
            "PROMETHEUS_ENDPOINT": "http://localhost:9090",
            "GRAFANA_API_KEY": "",
            "SENTRY_DSN": "",
            
            # Security
            "CORS_ORIGINS": "*",
            "SSL_CERT_PATH": "",
            "SSL_KEY_PATH": "",
            
            # Logging
            "LOG_LEVEL": "INFO",
            "LOG_FORMAT": "json",
            "LOG_FILE": "app.log",
            
            # Cache Configuration
            "CACHE_TYPE": "redis",
            "CACHE_EXPIRE_TIME": "3600",
            
            # Task System
            "TASK_QUEUE_URL": "",
            "MAX_CONCURRENT_TASKS": "5",
            
            # AI Code Generation
            "MAX_CODE_LENGTH": "10000",
            "CODE_GENERATION_TIMEOUT": "30",
            "MODEL_TEMPERATURE": "0.7"
        }

    def _get_dev_config(self) -> Dict[str, str]:
        """Development environment configuration"""
        config = self._get_base_config()
        config.update({
            "ENVIRONMENT": "development",
            "DEBUG": "true",
            "DATABASE_URL": "postgresql://dev_user:dev_pass@localhost:5432/dev_db",
            "REDIS_HOST": "localhost",
            "LOG_LEVEL": "DEBUG",
            "CORS_ORIGINS": "*",
            "MODEL_TEMPERATURE": "0.8"
        })
        return config

    def _get_staging_config(self) -> Dict[str, str]:
        """Staging environment configuration"""
        config = self._get_base_config()
        config.update({
            "ENVIRONMENT": "staging",
            "DATABASE_URL": "postgresql://staging_user:staging_pass@staging-db:5432/staging_db",
            "REDIS_HOST": "staging-redis",
            "LOG_LEVEL": "INFO",
            "CORS_ORIGINS": "https://staging.example.com",
            "MODEL_TEMPERATURE": "0.7"
        })
        return config

    def _get_prod_config(self) -> Dict[str, str]:
        """Production environment configuration"""
        config = self._get_base_config()
        config.update({
            "ENVIRONMENT": "production",
            "DATABASE_URL": "postgresql://prod_user:prod_pass@prod-db:5432/prod_db",
            "REDIS_HOST": "prod-redis",
            "LOG_LEVEL": "WARNING",
            "CORS_ORIGINS": "https://example.com",
            "MODEL_TEMPERATURE": "0.5",
            "SSL_CERT_PATH": "/etc/ssl/certs/app.crt",
            "SSL_KEY_PATH": "/etc/ssl/private/app.key"
        })
        return config 