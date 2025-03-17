from enum import Enum
from typing import Optional, Any, List
import asyncio

class OperationStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class MCPProgress:
    def __init__(self, operation_id: str):
        self.operation_id = operation_id
        self.status = OperationStatus.PENDING
        self.progress = 0.0
        self.message = ""
        self.details: List[str] = []
        self._subscribers = set()

    async def update(self, progress: float, message: str, status: OperationStatus = None):
        self.progress = progress
        self.message = message
        if status:
            self.status = status
        self.details.append(message)
        await self._notify_subscribers()

    async def _notify_subscribers(self):
        for callback in self._subscribers:
            try:
                await callback(self)
            except Exception:
                pass 