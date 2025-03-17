from typing import List, Dict
from dataclasses import dataclass
import asyncio

@dataclass
class EditPlan:
    steps: List[Dict]
    estimated_impact: float
    required_changes: List[str]
    validation_steps: List[str]

class EditPlanner:
    def __init__(self, code_intelligence: CodeIntelligence, workspace_manager: WorkspaceManager):
        self.code_intelligence = code_intelligence
        self.workspace_manager = workspace_manager

    async def create_edit_plan(self, edit_request: Dict) -> EditPlan:
        """Creates a structured plan for implementing the requested changes"""
        # Analyze the edit request
        affected_files = await self._identify_affected_files(edit_request)
        dependencies = await self._analyze_dependencies(affected_files)
        
        # Create step-by-step plan
        steps = await self._generate_edit_steps(edit_request, affected_files)
        
        # Estimate impact and create validation steps
        impact = await self._estimate_impact(steps, dependencies)
        validation = await self._create_validation_steps(steps)
        
        return EditPlan(
            steps=steps,
            estimated_impact=impact,
            required_changes=affected_files,
            validation_steps=validation
        )

    async def execute_plan(self, plan: EditPlan) -> Dict:
        """Executes an edit plan with validation and rollback capability"""
        snapshot_id = await self.workspace_manager.create_snapshot()
        
        try:
            results = []
            for step in plan.steps:
                result = await self._execute_step(step)
                results.append(result)
                
                # Validate after each step
                if not await self._validate_step(step, result):
                    raise Exception(f"Validation failed for step: {step['description']}")
                    
            return {
                "success": True,
                "results": results,
                "validation": await self._run_validation(plan.validation_steps)
            }
        except Exception as e:
            await self.workspace_manager.restore_snapshot(snapshot_id)
            return {
                "success": False,
                "error": str(e),
                "rollback": "completed"
            } 