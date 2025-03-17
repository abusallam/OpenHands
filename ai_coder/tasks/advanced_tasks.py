from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime
import networkx as nx

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

@dataclass
class EnhancedTask:
    """Advanced task representation"""
    id: str
    title: str
    description: str
    complexity: TaskComplexity
    estimated_time: int
    required_skills: List[str]
    dependencies: List[str]
    priority: int
    deadline: datetime
    assignee: Optional[str]
    resources: List[str]
    acceptance_criteria: List[str]

class AdvancedTaskSystem:
    """
    Enhanced task management system.
    
    Features:
    - Intelligent task breakdown
    - Resource allocation
    - Timeline management
    - Progress tracking
    - Quality assurance
    """

    def __init__(self):
        self.task_graph = nx.DiGraph()
        self.resource_manager = ResourceManager()
        self.timeline_manager = TimelineManager()
        self.progress_tracker = ProgressTracker()

    async def create_project_plan(self,
                                project_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a comprehensive project plan with tasks.
        """
        # Analyze project requirements
        analysis = await self._analyze_project(project_spec)
        
        # Generate task breakdown
        tasks = await self._generate_tasks(analysis)
        
        # Create timeline
        timeline = await self.timeline_manager.create_timeline(tasks)
        
        # Allocate resources
        resource_allocation = await self.resource_manager.allocate_resources(tasks)
        
        return {
            "tasks": tasks,
            "timeline": timeline,
            "resource_allocation": resource_allocation,
            "estimated_completion": timeline.end_date,
            "critical_path": await self._identify_critical_path(tasks)
        }

    async def execute_task_sequence(self,
                                  sequence: List[str]) -> Dict[str, Any]:
        """
        Executes a sequence of tasks with dependencies.
        """
        execution_plan = await self._create_execution_plan(sequence)
        results = []
        
        for task_batch in execution_plan:
            batch_results = await asyncio.gather(
                *[self._execute_task(task_id) for task_id in task_batch]
            )
            results.extend(batch_results)
            
            # Validate batch results
            if not all(r["success"] for r in batch_results):
                break
                
        return {
            "sequence_completed": all(r["success"] for r in results),
            "results": results,
            "metrics": await self._calculate_metrics(results)
        } 