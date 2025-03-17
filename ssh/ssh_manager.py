from typing import Dict, Optional, List
import asyncssh
import asyncio
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import os

class SecureSSHManager:
    """
    Manages secure SSH connections to remote servers.
    
    Features:
    - Encrypted credential storage
    - Multiple connection management
    - Key-based authentication
    - Connection pooling
    - Automatic reconnection
    """

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.connections: Dict[str, asyncssh.SSHClientConnection] = {}
        self.encryption_key = self._load_or_create_key()
        self.fernet = Fernet(self.encryption_key)

    async def connect(self, server_id: str) -> asyncssh.SSHClientConnection:
        """
        Establishes an SSH connection to a remote server.

        Args:
            server_id: Identifier for the server configuration

        Returns:
            SSHClientConnection object
        """
        config = await self._get_server_config(server_id)
        try:
            conn = await asyncssh.connect(
                host=config['host'],
                port=config['port'],
                username=config['username'],
                password=self._decrypt(config['password']) if 'password' in config else None,
                client_keys=[config['key_path']] if 'key_path' in config else None,
                known_hosts=None  # In production, use proper known_hosts handling
            )
            self.connections[server_id] = conn
            return conn
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {server_id}: {str(e)}")

    async def execute_command(self, 
                            server_id: str, 
                            command: str,
                            timeout: int = 30) -> Dict[str, Any]:
        """
        Executes a command on the remote server.
        """
        conn = await self._get_or_create_connection(server_id)
        try:
            result = await conn.run(command, timeout=timeout)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.exit_code
            }
        except asyncssh.ProcessError as e:
            return {
                "error": str(e),
                "exit_code": e.exit_status
            }

    def _encrypt(self, data: str) -> str:
        """Encrypts sensitive data"""
        return self.fernet.encrypt(data.encode()).decode()

    def _decrypt(self, encrypted_data: str) -> str:
        """Decrypts sensitive data"""
        return self.fernet.decrypt(encrypted_data.encode()).decode() 