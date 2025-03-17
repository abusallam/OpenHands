from typing import Dict, List, Optional
from dataclasses import dataclass
import pytest
import coverage
import asyncio
from pathlib import Path

@dataclass
class ValidationResult:
    """Results of validation checks"""
    success: bool
    test_results: Dict[str, Any]
    coverage_data: Dict[str, float]
    static_analysis: Dict[str, Any]
    security_checks: Dict[str, Any]
    performance_metrics: Dict[str, float]

class ComprehensiveValidator:
    """
    Advanced validation system for code changes.
    
    Features:
    - Multi-level testing
    - Code coverage analysis
    - Static code analysis
    - Security scanning
    - Performance testing
    """

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.coverage = coverage.Coverage()
        self.test_history: List[ValidationResult] = []

    async def validate_changes(self, 
                             changed_files: List[str],
                             validation_level: str = "complete") -> ValidationResult:
        """
        Performs comprehensive validation of code changes.

        Args:
            changed_files: List of modified files
            validation_level: Desired validation depth

        Returns:
            ValidationResult object with all check results
        """
        # Run all validation checks concurrently
        test_results, coverage_data, static_analysis, security_checks = await asyncio.gather(
            self._run_tests(changed_files),
            self._analyze_coverage(changed_files),
            self._run_static_analysis(changed_files),
            self._run_security_checks(changed_files)
        )

        # Analyze performance impact
        performance_metrics = await self._measure_performance_impact(changed_files)

        result = ValidationResult(
            success=all([
                test_results["success"],
                coverage_data["coverage_threshold_met"],
                static_analysis["passes_threshold"],
                security_checks["no_critical_issues"]
            ]),
            test_results=test_results,
            coverage_data=coverage_data,
            static_analysis=static_analysis,
            security_checks=security_checks,
            performance_metrics=performance_metrics
        )

        self.test_history.append(result)
        return result 