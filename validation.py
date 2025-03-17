from typing import List, Dict, Optional
import pytest
import coverage
import asyncio
from pathlib import Path

class ValidationManager:
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.coverage = coverage.Coverage()

    async def validate_changes(self, changed_files: List[str]) -> Dict:
        """Validates changes through multiple methods"""
        results = await asyncio.gather(
            self._run_tests(changed_files),
            self._run_static_analysis(changed_files),
            self._check_style(changed_files),
            self._verify_compilation(changed_files)
        )
        
        return {
            "test_results": results[0],
            "static_analysis": results[1],
            "style_checks": results[2],
            "compilation": results[3]
        }

    async def _run_tests(self, files: List[str]) -> Dict:
        """Runs relevant tests for changed files"""
        self.coverage.start()
        test_results = []
        
        for file_path in files:
            test_file = self._find_corresponding_test(file_path)
            if test_file:
                result = await self._run_pytest(test_file)
                test_results.append(result)
                
        self.coverage.stop()
        self.coverage.save()
        
        return {
            "results": test_results,
            "coverage": self.coverage.report()
        }

    async def _run_static_analysis(self, files: List[str]) -> Dict:
        """Runs static analysis tools"""
        results = {}
        for file_path in files:
            results[file_path] = {
                "mypy": await self._run_mypy(file_path),
                "pylint": await self._run_pylint(file_path),
                "bandit": await self._run_bandit(file_path)
            }
        return results 