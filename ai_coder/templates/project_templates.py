from typing import Dict, List, Optional
from pathlib import Path
import jinja2
import yaml

class ProjectTemplate:
    """Base class for project templates"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.files: Dict[str, str] = {}
        self.dependencies: List[str] = []
        self.configuration: Dict[str, Any] = {}

class WebAppTemplate(ProjectTemplate):
    """Template for web applications"""
    def __init__(self):
        super().__init__(
            name="webapp",
            description="Modern web application template"
        )
        self.frontend_framework = "react"
        self.backend_framework = "fastapi"
        self.database = "postgresql"

class MicroserviceTemplate(ProjectTemplate):
    """Template for microservices"""
    def __init__(self):
        super().__init__(
            name="microservice",
            description="Scalable microservice template"
        )
        self.service_mesh = "istio"
        self.monitoring = "prometheus"
        self.tracing = "jaeger"

class MLProjectTemplate(ProjectTemplate):
    """Template for machine learning projects"""
    def __init__(self):
        super().__init__(
            name="ml_project",
            description="Machine learning project template"
        )
        self.ml_framework = "pytorch"
        self.experiment_tracking = "mlflow"
        self.data_versioning = "dvc"

class TemplateManager:
    """
    Manages project templates and their instantiation.
    
    Features:
    - Multiple template types
    - Custom template creation
    - Template modification
    - Configuration management
    - Dependency resolution
    """

    def __init__(self):
        self.templates: Dict[str, ProjectTemplate] = {}
        self.template_engine = jinja2.Environment()
        self._load_built_in_templates()

    async def create_project_from_template(self,
                                         template_name: str,
                                         config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new project from a template.
        """
        if template_name not in self.templates:
            raise ValueError(f"Template not found: {template_name}")
            
        template = self.templates[template_name]
        
        # Customize template
        customized = await self._customize_template(template, config)
        
        # Generate project structure
        project = await self._generate_project(customized)
        
        # Setup dependencies
        await self._setup_dependencies(project)
        
        # Initialize git repository
        await self._initialize_git(project)
        
        return {
            "project_path": project.path,
            "structure": project.structure,
            "configuration": project.config,
            "next_steps": await self._generate_next_steps(project)
        }

    async def create_custom_template(self,
                                   specification: Dict[str, Any]) -> ProjectTemplate:
        """
        Creates a custom project template.
        """
        template = ProjectTemplate(
            name=specification["name"],
            description=specification["description"]
        )
        
        # Generate template structure
        await self._generate_template_structure(template, specification)
        
        # Add to template library
        self.templates[template.name] = template
        
        return template 