from typing import Dict, List, Optional
from enum import Enum
import subprocess
import asyncio

class ToolCategory(Enum):
    CODE_GENERATION = "code_generation"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"
    ANALYSIS = "analysis"

class Tool:
    def __init__(self, name: str, category: ToolCategory, command: str):
        self.name = name
        self.category = category
        self.command = command
        self.is_available = self._check_availability()

    def _check_availability(self) -> bool:
        try:
            subprocess.run(
                self.command.split()[0],
                capture_output=True,
                text=True
            )
            return True
        except:
            return False

class ToolManager:
    """
    Manages and executes various development tools.
    
    Features:
    - Tool discovery
    - Tool execution
    - Result parsing
    - Tool chaining
    - Error handling
    """

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._initialize_tools()

    def _initialize_tools(self):
        """Initialize all available tools"""
        # Code Generation Tools
        self.register_tool(
            Tool("copilot", ToolCategory.CODE_GENERATION, "copilot")
        )
        self.register_tool(
            Tool("gpt-code", ToolCategory.CODE_GENERATION, "gpt-code")
        )

        # Testing Tools
        self.register_tool(
            Tool("pytest", ToolCategory.TESTING, "pytest")
        )
        self.register_tool(
            Tool("jest", ToolCategory.TESTING, "jest")
        )

        # Documentation Tools
        self.register_tool(
            Tool("sphinx", ToolCategory.DOCUMENTATION, "sphinx-build")
        )
        self.register_tool(
            Tool("jsdoc", ToolCategory.DOCUMENTATION, "jsdoc")
        )

        # Analysis Tools
        self.register_tool(
            Tool("pylint", ToolCategory.ANALYSIS, "pylint")
        )
        self.register_tool(
            Tool("eslint", ToolCategory.ANALYSIS, "eslint")
        )

    async def execute_tool(self,
                          tool_name: str,
                          args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a specific tool with given arguments.
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")

        tool = self.tools[tool_name]
        if not tool.is_available:
            raise RuntimeError(f"Tool {tool_name} is not available")

        try:
            process = await asyncio.create_subprocess_exec(
                *self._build_command(tool, args),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            
            return {
                "success": process.returncode == 0,
                "output": stdout.decode(),
                "error": stderr.decode() if stderr else None,
                "tool": tool_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            } 