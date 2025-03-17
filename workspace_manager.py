from pathlib import Path
from typing import Dict, List, Optional
import aiofiles
import git
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WorkspaceManager:
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.git_repo = git.Repo(workspace_path) if workspace_path.joinpath('.git').exists() else None
        self.file_watchers: Dict[str, FileSystemEventHandler] = {}
        self.workspace_state: Dict[str, Dict] = {}
        self.setup_workspace_monitoring()

    def setup_workspace_monitoring(self):
        """Sets up real-time monitoring of workspace changes"""
        self.observer = Observer()
        event_handler = WorkspaceEventHandler(self)
        self.observer.schedule(event_handler, str(self.workspace_path), recursive=True)
        self.observer.start()

    async def create_branch_for_edit(self, edit_description: str) -> str:
        """Creates a new git branch for an edit operation"""
        if not self.git_repo:
            return None
            
        branch_name = f"mcp-edit-{int(time.time())}"
        current = self.git_repo.active_branch
        new_branch = self.git_repo.create_head(branch_name)
        new_branch.checkout()
        return branch_name

    async def commit_changes(self, files: List[str], message: str):
        """Commits changes to version control"""
        if not self.git_repo:
            return
            
        self.git_repo.index.add(files)
        self.git_repo.index.commit(message)

    async def create_snapshot(self) -> str:
        """Creates a workspace snapshot for rollback"""
        snapshot_id = f"snapshot-{int(time.time())}"
        snapshot_path = self.workspace_path / ".mcp" / "snapshots" / snapshot_id
        await self._copy_workspace(snapshot_path)
        return snapshot_id

    async def restore_snapshot(self, snapshot_id: str):
        """Restores workspace from a snapshot"""
        snapshot_path = self.workspace_path / ".mcp" / "snapshots" / snapshot_id
        await self._copy_workspace(self.workspace_path, snapshot_path) 