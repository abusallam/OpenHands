from typing import Dict, List, Optional, Callable
import asyncio
from datetime import datetime

class TaskExecutor:
    """
    Handles task execution and monitoring.
    
    Features:
    - Parallel task execution
    - Progress monitoring
    - Error handling
    - Resource management
    - Execution logging
    """

    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.execution_hooks: Dict[str, List[Callable]] = {}
        self.max_concurrent_tasks = 5
        self.semaphore = asyncio.Semaphore(self.max_concurrent_tasks)

    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """
        Executes a single task with all its requirements.
        """
        task = self.task_manager.tasks[task_id]
        
        # Check dependencies
        if not await self._check_dependencies(task):
            task.status = TaskStatus.BLOCKED
            return {"status": "blocked", "reason": "dependencies_not_met"}

        async with self.semaphore:
            try:
                # Mark task as in progress
                task.status = TaskStatus.IN_PROGRESS
                task.updated_at = datetime.now()

                # Execute pre-execution hooks
                await self._run_hooks("pre_execute", task)

                # Execute the task
                result = await self._execute_task_logic(task)

                # Update task status
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                task.progress = 1.0

                # Execute post-execution hooks
                await self._run_hooks("post_execute", task)

                return {
                    "status": "success",
                    "task_id": task_id,
                    "result": result
                }

            except Exception as e:
                task.status = TaskStatus.FAILED
                task.notes.append(f"Execution failed: {str(e)}")
                return {
                    "status": "failed",
                    "task_id": task_id,
                    "error": str(e)
                }

    async def execute_sequence(self, task_ids: List[str]) -> Dict[str, Any]:
        """
        Executes a sequence of tasks in order.
        """
        results = []
        for task_id in task_ids:
            result = await self.execute_task(task_id)
            results.append(result)
            if result["status"] == "failed":
                break
        return {"sequence_results": results} 