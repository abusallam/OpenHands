from typing import Dict, List
import graphviz
from datetime import datetime

class TaskVisualizer:
    """
    Visualizes task relationships and progress.
    
    Features:
    - Dependency graph visualization
    - Progress tracking
    - Timeline visualization
    - Resource allocation view
    - Critical path highlighting
    """

    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def create_dependency_graph(self) -> str:
        """
        Creates a visual representation of task dependencies.
        """
        dot = graphviz.Digraph(comment='Task Dependencies')
        
        # Add nodes
        for task_id, task in self.task_manager.tasks.items():
            color = self._get_status_color(task.status)
            dot.node(task_id, task.title, color=color)
        
        # Add edges
        for task_id, task in self.task_manager.tasks.items():
            for dep in task.dependencies:
                dot.edge(dep, task_id)
        
        return dot.source

    def create_timeline(self) -> Dict[str, Any]:
        """
        Creates a timeline visualization of tasks.
        """
        timeline = []
        for task_id, task in self.task_manager.tasks.items():
            timeline.append({
                "id": task_id,
                "title": task.title,
                "start": task.created_at.isoformat(),
                "end": (task.completed_at or datetime.now()).isoformat(),
                "progress": task.progress,
                "status": task.status.value
            })
        return {"timeline": timeline} 