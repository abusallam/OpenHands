from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime

class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    CODE_MODIFICATION = "code_modification"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    REVIEW = "review"
    DEPLOYMENT = "deployment"

@dataclass
class AITask:
    """Represents an AI coding task"""
    id: str
    type: TaskType
    description: str
    context: CodeContext
    subtasks: List['AITask']
    tools_required: List[str]
    estimated_time: int
    priority: int
    status: str
    created_at: datetime
    dependencies: List[str] = None

class AITaskSystem:
    """
    Manages AI coding tasks and their execution.
    
    Features:
    - Task creation
    - Task breakdown
    - Tool selection
    - Progress tracking
    - Result validation
    """

    def __init__(self, ai_coder: AICoder, tool_manager: ToolManager):
        self.ai_coder = ai_coder
        self.tool_manager = tool_manager
        self.tasks: Dict[str, AITask] = {}

    async def create_coding_task(self,
                               description: str,
                               context: CodeContext) -> AITask:
        """
        Creates a new coding task with automatic breakdown.
        """
        # Analyze task
        task_analysis = await self._analyze_task(description)
        
        # Create main task
        main_task = AITask(
            id=f"task_{uuid4().hex[:8]}",
            type=task_analysis.task_type,
            description=description,
            context=context,
            subtasks=[],
            tools_required=task_analysis.required_tools,
            estimated_time=task_analysis.estimated_time,
            priority=task_analysis.priority,
            status="created",
            created_at=datetime.now()
        )
        
        # Break down into subtasks
        subtasks = await self._break_down_task(main_task)
        main_task.subtasks = subtasks
        
        self.tasks[main_task.id] = main_task
        return main_task

    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """
        Executes a coding task using AI and tools.
        """
        task = self.tasks[task_id]
        
        try:
            # Execute subtasks first
            subtask_results = []
            for subtask in task.subtasks:
                result = await self.execute_task(subtask.id)
                subtask_results.append(result)
                if not result["success"]:
                    raise Exception(f"Subtask {subtask.id} failed")

            # Execute main task
            if task.type == TaskType.CODE_GENERATION:
                result = await self.ai_coder.generate_code(
                    task.description,
                    task.context
                )
            elif task.type == TaskType.CODE_MODIFICATION:
                result = await self.ai_coder.modify_code(
                    task.context.active_file,
                    task.description,
                    task.context
                )

            # Execute required tools
            tool_results = []
            for tool in task.tools_required:
                tool_result = await self.tool_manager.execute_tool(
                    tool,
                    {"task": task, "previous_result": result}
                )
                tool_results.append(tool_result)

            return {
                "success": True,
                "task_id": task_id,
                "result": result,
                "tool_results": tool_results,
                "subtask_results": subtask_results
            }

        except Exception as e:
            return {
                "success": False,
                "task_id": task_id,
                "error": str(e)
            } 