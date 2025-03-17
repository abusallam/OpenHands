from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from mcp import MCPServer, MCPResponse
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from pathlib import Path
import time

from config import MCPConfig, MCPServerConfig
from middleware import rate_limit_middleware, verify_token, security
from mcp_context import MCPContextManager
from session import MCPSessionManager
from progress import MCPProgress
from operation import OperationStatus
from code_intelligence import CodeIntelligence, EnhancedCodeIntelligence
from workspace_manager import WorkspaceManager
from edit_planner import EditPlanner, AdvancedEditPlanner
from validation import ValidationManager, ComprehensiveValidator
from monitoring import MetricsManager
from docs import DocumentationGenerator
from ssh import SecureSSHManager
from config import EnvironmentManager
from deployment import DeploymentManager
from tasks import TaskManager, TaskExecutor, TaskPlanner, TaskVisualizer
from ai_coder.core import AICoder, CodeContext
from ai_coder.tools import ToolManager
from ai_coder.tasks import AITaskSystem
from ai_coder.project import ProjectManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OpenHandsMCP:
    def __init__(self):
        self.config = MCPConfig()
        self.session_manager = MCPSessionManager()
        self.context_manager = MCPContextManager(self.config.workspace_path)
        self.app = FastAPI(title="OpenHands MCP Server")
        self.mcp = MCPServer(self.app)
        self.aider = None
        self.code_intelligence = EnhancedCodeIntelligence(Path(self.config.workspace_path))
        self.workspace_manager = WorkspaceManager(Path(self.config.workspace_path))
        self.edit_planner = AdvancedEditPlanner(self.code_intelligence)
        self.validator = ComprehensiveValidator(Path(self.config.workspace_path))
        self.doc_generator = DocumentationGenerator(Path(self.config.workspace_path))
        self.metrics_manager = MetricsManager()
        self.ssh_manager = SecureSSHManager(self.config.config_path)
        self.env_manager = EnvironmentManager(self.config.config_path)
        self.deploy_manager = DeploymentManager(self.ssh_manager, self.env_manager)
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor(self.task_manager)
        self.task_planner = TaskPlanner(self.task_manager)
        self.task_visualizer = TaskVisualizer(self.task_manager)
        self.setup_middleware()
        self.setup_mcp_endpoints()
        self.setup_mcp_tools()
        self.setup_mcp_resources()

    def setup_middleware(self):
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Add rate limiting middleware
        self.app.middleware("http")(rate_limit_middleware)

    async def initialize_aider(self):
        try:
            # Initialize Aider with configuration
            logger.info("Initializing Aider...")
            # Add your Aider initialization code here
            pass
        except Exception as e:
            logger.error(f"Failed to initialize Aider: {e}")
            raise

    def setup_mcp_endpoints(self):
        @self.mcp.tool(
            name="edit_file",
            description="Edits a file using AI assistance",
            schema={
                "file_path": {"type": "string", "description": "Path to the file to edit"},
                "edit_instructions": {"type": "string", "description": "Instructions for the edit"}
            }
        )
        async def edit_file(
            file_path: str,
            edit_instructions: str,
            credentials: HTTPAuthorizationCredentials = Depends(security)
        ) -> MCPResponse:
            try:
                if self.config.auth_enabled:
                    await verify_token(credentials)

                if not self.aider:
                    raise HTTPException(status_code=500, detail="Aider not initialized")
                
                logger.info(f"Editing file: {file_path}")
                result = await self.aider.edit(file_path, edit_instructions)
                
                return MCPResponse(
                    status="success",
                    data={
                        "result": result,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
            except Exception as e:
                logger.error(f"Error editing file: {e}")
                return MCPResponse(
                    status="error",
                    error=str(e)
                )

        @self.mcp.resource(
            name="status",
            description="Get OpenHands system status"
        )
        async def get_status(
            credentials: HTTPAuthorizationCredentials = Depends(security)
        ) -> MCPResponse:
            if self.config.auth_enabled:
                await verify_token(credentials)

            return MCPResponse(
                status="success",
                data={
                    "status": "running",
                    "aider_initialized": bool(self.aider),
                    "version": "1.0.0",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

        @self.mcp.tool(
            name="smart_edit",
            description="Intelligent code editing with validation and rollback"
        )
        async def smart_edit(request: Dict) -> MCPResponse:
            start_time = time.time()
            try:
                # Create and execute edit plan
                plan = await self.edit_planner.create_comprehensive_plan(request)
                result = await self.edit_planner.execute_plan_with_monitoring(plan)
                
                # Validate changes
                validation = await self.validator.validate_changes(plan.required_changes)
                
                duration = time.time() - start_time
                await self.metrics_manager.record_operation("smart_edit", duration, result["success"])
                
                return MCPResponse(
                    status="success",
                    data={
                        "result": result,
                        "validation": validation,
                        "metrics": await self.metrics_manager.get_performance_metrics()
                    }
                )
            except Exception as e:
                duration = time.time() - start_time
                await self.metrics_manager.record_operation("smart_edit", duration, False)
                return MCPResponse(status="error", error=str(e))

        @self.mcp.resource(
            name="codebase_analysis",
            description="Get comprehensive codebase analysis"
        )
        async def analyze_codebase() -> MCPResponse:
            analysis = await self.code_intelligence.analyze_codebase(
                Path(self.config.workspace_path)
            )
            return MCPResponse(status="success", data=analysis)

    def setup_mcp_tools(self):
        @self.mcp.tool(
            name="edit_code",
            description="Edit code files with AI assistance",
            schema={
                "file_path": {"type": "string", "description": "Path to the file to edit"},
                "edit_instructions": {"type": "string", "description": "Natural language instructions for the edit"},
                "mode": {"type": "string", "enum": ["safe", "aggressive"], "default": "safe", "description": "Edit mode"}
            }
        )
        async def edit_code(file_path: str, edit_instructions: str, mode: str = "safe") -> MCPResponse:
            try:
                result = await self.aider.edit(file_path, edit_instructions, mode=mode)
                return MCPResponse(
                    status="success",
                    data={"changes": result.changes, "explanation": result.explanation}
                )
            except Exception as e:
                return MCPResponse(status="error", error=str(e))

        @self.mcp.tool(
            name="code_review",
            description="Review code changes or entire files",
            schema={
                "files": {"type": "array", "items": {"type": "string"}, "description": "Files to review"},
                "review_type": {"type": "string", "enum": ["security", "performance", "style", "full"], "default": "full"}
            }
        )
        async def code_review(files: List[str], review_type: str = "full") -> MCPResponse:
            try:
                reviews = await self.aider.review(files, review_type)
                return MCPResponse(
                    status="success",
                    data={"reviews": reviews}
                )
            except Exception as e:
                return MCPResponse(status="error", error=str(e))

        @self.mcp.tool(
            name="generate_tests",
            description="Generate unit tests for specified code",
            schema={
                "file_path": {"type": "string", "description": "Path to the source file"},
                "framework": {"type": "string", "enum": ["pytest", "unittest"], "default": "pytest"},
                "coverage_target": {"type": "integer", "minimum": 0, "maximum": 100, "default": 80}
            }
        )
        async def generate_tests(file_path: str, framework: str = "pytest", coverage_target: int = 80) -> MCPResponse:
            try:
                tests = await self.aider.generate_tests(file_path, framework, coverage_target)
                return MCPResponse(
                    status="success",
                    data={"test_file": tests.file_path, "coverage": tests.coverage}
                )
            except Exception as e:
                return MCPResponse(status="error", error=str(e))

    def setup_mcp_resources(self):
        @self.mcp.resource(
            name="project_context",
            description="Get current project context and statistics"
        )
        async def get_project_context() -> MCPResponse:
            try:
                context = await self.aider.get_project_context()
                return MCPResponse(
                    status="success",
                    data={
                        "files_tracked": context.tracked_files,
                        "git_status": context.git_status,
                        "recent_changes": context.recent_changes,
                        "active_branches": context.branches
                    }
                )
            except Exception as e:
                return MCPResponse(status="error", error=str(e))

        @self.mcp.resource(
            name="model_config",
            description="Get or update AI model configuration"
        )
        async def model_config() -> MCPResponse:
            return MCPResponse(
                status="success",
                data={
                    "current_model": self.aider.model_config,
                    "available_models": self.aider.available_models
                }
            )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        try:
            await self.initialize_aider()
            yield
        finally:
            if self.aider:
                logger.info("Cleaning up Aider...")
                await self.aider.cleanup()

    def get_app(self) -> FastAPI:
        self.app.lifespan = self.lifespan
        return self.app

    async def handle_mcp_request(self, request: dict, session: MCPSession) -> MCPResponse:
        operation_id = request.get('operation_id')
        progress = MCPProgress(operation_id)
        
        async def operation():
            try:
                # Your operation logic here
                await progress.update(0.5, "Processing request...")
                result = await self.aider.process(request)
                await progress.update(1.0, "Complete", OperationStatus.COMPLETED)
                return result
            except Exception as e:
                await progress.update(1.0, str(e), OperationStatus.FAILED)
                raise

        return await session.start_operation(operation_id, operation())

# Create application instance
app = OpenHandsMCP().get_app() 

class EnhancedMCPServer:
    """
    Enhanced MCP server with comprehensive features.
    
    Features:
    - Intelligent code editing
    - Advanced validation
    - Documentation generation
    - Performance monitoring
    - Security checks
    """

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.code_intelligence = EnhancedCodeIntelligence(Path(config.workspace_path))
        self.edit_planner = AdvancedEditPlanner(self.code_intelligence)
        self.validator = ComprehensiveValidator(Path(config.workspace_path))
        self.doc_generator = DocumentationGenerator(Path(config.workspace_path))
        self.ssh_manager = SecureSSHManager(config.config_path)
        self.env_manager = EnvironmentManager(config.config_path)
        self.deploy_manager = DeploymentManager(self.ssh_manager, self.env_manager)
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor(self.task_manager)
        self.task_planner = TaskPlanner(self.task_manager)
        self.task_visualizer = TaskVisualizer(self.task_manager)
        
        self.setup_enhanced_endpoints()

    def setup_enhanced_endpoints(self):
        """Sets up all MCP endpoints with enhanced capabilities"""
        @self.mcp.tool(
            name="deploy_code",
            description="Deploy code to remote server"
        )
        async def deploy_code(
            server_id: str,
            code_path: str,
            environment: str = "development"
        ) -> MCPResponse:
            try:
                result = await self.deploy_manager.deploy_code(
                    server_id,
                    Path(code_path),
                    environment
                )
                return MCPResponse(
                    status="success",
                    data=result
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                )

        @self.mcp.tool(
            name="manage_environment",
            description="Manage environment configurations"
        )
        async def manage_environment(
            action: str,
            env_name: str,
            data: Optional[Dict] = None
        ) -> MCPResponse:
            try:
                if action == "create":
                    result = self.env_manager.create_environment(env_name)
                elif action == "update":
                    result = self.env_manager.update_environment(env_name, data)
                elif action == "delete":
                    result = self.env_manager.delete_environment(env_name)
                else:
                    raise ValueError(f"Unknown action: {action}")

                return MCPResponse(
                    status="success",
                    data=result
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                )

        @self.mcp.tool(
            name="create_development_plan",
            description="Create a development plan with tasks"
        )
        async def create_development_plan(
            objective: str,
            context: Dict[str, Any]
        ) -> MCPResponse:
            try:
                plan = await self.task_planner.create_development_plan(
                    objective,
                    context
                )
                return MCPResponse(
                    status="success",
                    data=plan
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                )

        @self.mcp.tool(
            name="execute_task",
            description="Execute a specific task"
        )
        async def execute_task(task_id: str) -> MCPResponse:
            try:
                result = await self.task_executor.execute_task(task_id)
                return MCPResponse(
                    status="success",
                    data=result
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                )

        @self.mcp.tool(
            name="visualize_tasks",
            description="Get task visualizations"
        )
        async def visualize_tasks(
            visualization_type: str = "dependency_graph"
        ) -> MCPResponse:
            try:
                if visualization_type == "dependency_graph":
                    data = self.task_visualizer.create_dependency_graph()
                elif visualization_type == "timeline":
                    data = self.task_visualizer.create_timeline()
                else:
                    raise ValueError(f"Unknown visualization type: {visualization_type}")

                return MCPResponse(
                    status="success",
                    data=data
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                ) 

class AICoderServer:
    """
    Complete AI coding server with integrated tools.
    
    Features:
    - AI code generation
    - Tool management
    - Task execution
    - Project management
    - Progress tracking
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ai_coder = AICoder()
        self.tool_manager = ToolManager()
        self.task_system = AITaskSystem(self.ai_coder, self.tool_manager)
        self.project_manager = ProjectManager(Path(config["project_path"]))

    def setup_endpoints(self):
        @self.mcp.tool(
            name="create_coding_task",
            description="Create and execute an AI coding task"
        )
        async def create_coding_task(
            description: str,
            context: Dict[str, Any]
        ) -> MCPResponse:
            try:
                # Create task
                task = await self.task_system.create_coding_task(
                    description,
                    CodeContext(**context)
                )
                
                # Execute task
                result = await self.task_system.execute_task(task.id)
                
                return MCPResponse(
                    status="success",
                    data={
                        "task": task,
                        "result": result
                    }
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                )

        @self.mcp.tool(
            name="initialize_project",
            description="Initialize a new AI-managed project"
        )
        async def initialize_project(
            project_path: str,
            template: str = "default"
        ) -> MCPResponse:
            try:
                result = await self.project_manager.initialize_project(template)
                return MCPResponse(
                    status="success",
                    data=result
                )
            except Exception as e:
                return MCPResponse(
                    status="error",
                    error=str(e)
                ) 