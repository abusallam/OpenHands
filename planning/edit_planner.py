from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio

class EditImpact(Enum):
    """Classification of edit impact levels"""
    MINIMAL = "minimal"      # Local changes only
    MODERATE = "moderate"    # Affects few files
    SIGNIFICANT = "significant"  # Widespread changes
    CRITICAL = "critical"    # System-wide impact

@dataclass
class EditStep:
    """Represents a single step in an edit plan"""
    description: str
    file_path: str
    line_range: tuple
    change_type: str
    estimated_impact: EditImpact
    validation_requirements: List[str]

@dataclass
class EditPlan:
    """Complete plan for implementing code changes"""
    steps: List[EditStep]
    estimated_duration: float
    required_changes: List[str]
    validation_steps: List[str]
    rollback_plan: Dict[str, Any]
    dependencies: List[str]

class AdvancedEditPlanner:
    """
    Intelligent system for planning and executing code edits.
    
    Features:
    - Multi-step edit planning
    - Impact analysis
    - Dependency tracking
    - Automatic validation
    - Rollback planning
    """

    def __init__(self, 
                 code_intelligence: EnhancedCodeIntelligence,
                 workspace_manager: WorkspaceManager):
        self.code_intelligence = code_intelligence
        self.workspace_manager = workspace_manager
        self.edit_history: List[EditPlan] = []

    async def create_comprehensive_plan(self, 
                                      edit_request: Dict,
                                      safety_level: str = "strict") -> EditPlan:
        """
        Creates a detailed plan for implementing requested changes.

        Args:
            edit_request: Dictionary containing edit details
            safety_level: Desired safety level ("strict", "moderate", "flexible")

        Returns:
            EditPlan object with complete implementation details
        """
        # Analyze request and context
        affected_files = await self._identify_affected_files(edit_request)
        dependencies = await self._analyze_dependencies(affected_files)
        
        # Generate steps with safety checks
        steps = []
        for file_path in affected_files:
            file_steps = await self._plan_file_changes(
                file_path,
                edit_request,
                safety_level
            )
            steps.extend(file_steps)

        # Create comprehensive plan
        plan = EditPlan(
            steps=steps,
            estimated_duration=await self._estimate_duration(steps),
            required_changes=affected_files,
            validation_steps=await self._create_validation_steps(steps, safety_level),
            rollback_plan=await self._create_rollback_plan(steps),
            dependencies=dependencies
        )

        self.edit_history.append(plan)
        return plan

    async def execute_plan_with_monitoring(self, 
                                         plan: EditPlan,
                                         progress_callback: Optional[callable] = None) -> Dict:
        """
        Executes an edit plan with real-time monitoring and safety checks.

        Args:
            plan: EditPlan to execute
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary containing execution results and metrics
        """
        start_time = time.time()
        snapshot_id = await self.workspace_manager.create_snapshot()
        
        try:
            results = []
            for i, step in enumerate(plan.steps):
                # Execute step with safety checks
                result = await self._execute_step_safely(step)
                results.append(result)
                
                # Update progress
                if progress_callback:
                    await progress_callback(i / len(plan.steps), step.description)
                
                # Validate step
                validation = await self._validate_step(step, result)
                if not validation["success"]:
                    raise ValidationError(f"Step validation failed: {validation['error']}")

            return {
                "success": True,
                "results": results,
                "duration": time.time() - start_time,
                "metrics": await self._collect_execution_metrics(results)
            }

        except Exception as e:
            await self.workspace_manager.restore_snapshot(snapshot_id)
            return {
                "success": False,
                "error": str(e),
                "rollback": "completed",
                "duration": time.time() - start_time
            } 