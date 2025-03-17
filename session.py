from datetime import datetime
from typing import Dict, Any, Optional
import asyncio

class MCPSession:
    def __init__(self, session_id: str, client_id: str):
        self.session_id = session_id
        self.client_id = client_id
        self.created_at = datetime.utcnow()
        self.last_active = self.created_at
        self.context: Dict[str, Any] = {}
        self.active_operations: Dict[str, asyncio.Task] = {}

    async def start_operation(self, operation_id: str, coroutine) -> Any:
        task = asyncio.create_task(coroutine)
        self.active_operations[operation_id] = task
        try:
            result = await task
            return result
        finally:
            del self.active_operations[operation_id]

    async def cancel_operation(self, operation_id: str) -> bool:
        if operation_id in self.active_operations:
            self.active_operations[operation_id].cancel()
            return True
        return False

class MCPSessionManager:
    def __init__(self):
        self.sessions: Dict[str, MCPSession] = {}

    async def create_session(self, client_id: str) -> MCPSession:
        session_id = f"{client_id}-{datetime.utcnow().timestamp()}"
        session = MCPSession(session_id, client_id)
        self.sessions[session_id] = session
        return session

    async def get_session(self, session_id: str) -> Optional[MCPSession]:
        return self.sessions.get(session_id) 