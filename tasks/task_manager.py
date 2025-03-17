from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import asyncio
from uuid import uuid4
import networkx as nx

class TaskStatus(Enum):
    PLANNED = "planned"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    CRITICAL = 3

@dataclass
class TaskContext:
    """Context information for a task"""
    files: List[str]
    dependencies: List[str]
    environment: str
    requirements: List[str]
    estimated_time: int  # minutes

@dataclass
class Task:
    """Represents a single task in the system"""
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    context: TaskContext
    dependencies: List[str]
    subtasks: List['Task']
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    assigned_to: Optional[str] = None
    progress: float = 0.0
    notes: List[str] = None

class TaskManager:
    """
    Advanced task management system for AI coaching.
    
    Features:
    - Task creation and organization
    - Dependency management
    - Progress tracking
    - Priority scheduling
    - Automated execution
    """

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.dependency_graph = nx.DiGraph()
        self.task_history: List[Dict] = []
        self.active_tasks: Dict[str, asyncio.Task] = {}

    async def create_task(self, 
                         title: str,
                         description: str,
                         context: TaskContext,
                         priority: TaskPriority = TaskPriority.MEDIUM,
                         dependencies: List[str] = None) -> Task:
        """
        Creates a new task with given specifications.
        """
        task_id = f"task_{uuid4().hex[:8]}"
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.PLANNED,
            priority=priority,
            context=context,
            dependencies=dependencies or [],
            subtasks=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            notes=[]
        )
        
        self.tasks[task_id] = task
        self._update_dependency_graph(task)
        return task

    async def create_task_sequence(self, 
                                 tasks: List[Dict],
                                 sequential: bool = True) -> List[Task]:
        """
        Creates a sequence of related tasks.
        """
        created_tasks = []
        previous_task_id = None

        for task_data in tasks:
            if sequential and previous_task_id:
                if 'dependencies' not in task_data:
                    task_data['dependencies'] = []
                task_data['dependencies'].append(previous_task_id)

            task = await self.create_task(**task_data)
            created_tasks.append(task)
            previous_task_id = task.id

        return created_tasks 