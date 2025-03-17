from typing import List, Dict, Any
from dataclasses import dataclass
from pathlib import Path
import asyncio
import git

@dataclass
class FileContext:
    path: Path
    content: str
    last_modified: float
    git_status: str = None

class MCPContextManager:
    def __init__(self, workspace_path: str):
        self.workspace = Path(workspace_path)
        self.file_contexts: Dict[str, FileContext] = {}
        self.repo = git.Repo(workspace_path) if Path(workspace_path).joinpath('.git').exists() else None
        
    async def track_file(self, file_path: str) -> FileContext:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
            
        content = await self._read_file(path)
        context = FileContext(
            path=path,
            content=content,
            last_modified=path.stat().st_mtime,
            git_status=self._get_git_status(path) if self.repo else None
        )
        self.file_contexts[str(path)] = context
        return context

    async def _read_file(self, path: Path) -> str:
        async with aiofiles.open(path, 'r') as f:
            return await f.read()

    def _get_git_status(self, path: Path) -> str:
        if not self.repo:
            return None
        return self.repo.git.status('--porcelain', str(path)) 