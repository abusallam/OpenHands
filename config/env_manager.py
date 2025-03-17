from typing import Dict, Optional
from pathlib import Path
import yaml
from cryptography.fernet import Fernet
import json

class EnvironmentManager:
    """
    Manages environment configurations and sensitive data.
    
    Features:
    - Multiple environment support
    - Encrypted sensitive data
    - Template generation
    - Version control
    - Automatic validation
    """

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.encryption_key = self._load_or_create_key()
        self.fernet = Fernet(self.encryption_key)
        self.environments = self._load_environments()

    def create_environment(self, name: str, template: bool = False) -> Dict:
        """Creates a new environment configuration"""
        env_config = {
            "name": name,
            "type": "template" if template else "environment",
            "variables": self._get_default_variables(),
            "servers": self._get_default_servers(),
            "security": {
                "encryption_enabled": True,
                "require_2fa": False
            }
        }
        
        self._save_environment(name, env_config)
        return env_config

    def _get_default_variables(self) -> Dict:
        """Returns default environment variables"""
        return {
            "DATABASE_URL": "postgresql://user:pass@localhost:5432/db",
            "API_KEY": "dummy_api_key",
            "SECRET_KEY": "dummy_secret_key",
            "DEBUG": "false",
            "ENVIRONMENT": "development"
        }

    def _get_default_servers(self) -> Dict:
        """Returns default server configurations"""
        return {
            "development": {
                "host": "dev.example.com",
                "port": 22,
                "username": "dev_user",
                "key_path": "~/.ssh/id_rsa"
            },
            "staging": {
                "host": "staging.example.com",
                "port": 22,
                "username": "stage_user",
                "key_path": "~/.ssh/id_rsa"
            },
            "production": {
                "host": "prod.example.com",
                "port": 22,
                "username": "prod_user",
                "key_path": "~/.ssh/id_rsa"
            }
        } 