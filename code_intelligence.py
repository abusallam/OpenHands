from typing import Dict, List, Optional
import ast
import libcst
from pathlib import Path
import networkx as nx

class CodeIntelligence:
    def __init__(self):
        self.dependency_graph = nx.DiGraph()
        self.symbol_table: Dict[str, Dict] = {}
        self.code_metrics: Dict[str, Dict] = {}

    async def analyze_codebase(self, root_path: Path) -> Dict:
        """Analyzes entire codebase for dependencies and metrics"""
        for file_path in root_path.rglob('*.py'):
            await self.analyze_file(file_path)
        return {
            "dependencies": self._get_dependency_report(),
            "metrics": self._get_metrics_report(),
            "symbols": self._get_symbol_report()
        }

    async def analyze_file(self, file_path: Path):
        """Analyzes a single file for symbols and dependencies"""
        with open(file_path) as f:
            content = f.read()
            tree = ast.parse(content)
            
        # Analyze symbols and dependencies
        visitor = CodeVisitor(self.symbol_table, self.dependency_graph)
        visitor.visit(tree)
        
        # Calculate metrics
        self.code_metrics[str(file_path)] = {
            "complexity": self._calculate_complexity(tree),
            "maintainability": self._calculate_maintainability(tree),
            "test_coverage": await self._get_test_coverage(file_path)
        }

    def get_context_for_edit(self, file_path: str, edit_location: int) -> Dict:
        """Gets relevant context for an edit at a specific location"""
        return {
            "symbols_in_scope": self._get_symbols_at_location(file_path, edit_location),
            "related_files": self._get_related_files(file_path),
            "dependencies": self._get_local_dependencies(file_path)
        } 