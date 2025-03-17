from pydantic import BaseSettings, Field
from typing import Dict, Any, Optional
import logging

class MCPConfig(BaseSettings):
    host: str = Field(default="0.0.0.0", env="OPENHANDS_MCP_HOST")
    port: int = Field(default=8000, env="OPENHANDS_MCP_PORT")
    debug: bool = Field(default=False, env="OPENHANDS_MCP_DEBUG")
    log_level: str = Field(default="INFO", env="OPENHANDS_MCP_LOG_LEVEL")
    rate_limit_requests: int = Field(default=100, env="OPENHANDS_MCP_RATE_LIMIT_REQUESTS")
    rate_limit_period: int = Field(default=60, env="OPENHANDS_MCP_RATE_LIMIT_PERIOD")  # seconds
    auth_enabled: bool = Field(default=True, env="OPENHANDS_MCP_AUTH_ENABLED")
    auth_secret: str = Field(default="your-secret-key", env="OPENHANDS_MCP_AUTH_SECRET")
    aider_config: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        env_file = ".env" 