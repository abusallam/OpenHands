from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MCPToolConfig(BaseModel):
    name: str
    description: str
    enabled: bool = True
    rate_limit: Optional[int] = None
    requires_auth: bool = True
    timeout: int = 30

class MCPServerConfig(BaseModel):
    tools: Dict[str, MCPToolConfig] = {
        "edit_code": MCPToolConfig(
            name="edit_code",
            description="Edit code files with AI assistance",
            rate_limit=100
        ),
        "code_review": MCPToolConfig(
            name="code_review",
            description="Review code changes or entire files",
            rate_limit=50
        ),
        "generate_tests": MCPToolConfig(
            name="generate_tests",
            description="Generate unit tests for specified code",
            rate_limit=30
        )
    }
    
    workspace_path: str = Field(..., description="Path to the workspace directory")
    git_integration: bool = True
    max_file_size: int = 1024 * 1024  # 1MB
    supported_languages: List[str] = ["python", "javascript", "typescript", "java", "go"] 