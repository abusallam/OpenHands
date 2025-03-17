from typing import Dict, List, Optional
from pathlib import Path
import asyncio
from datetime import datetime

class DeploymentManager:
    """
    Manages code deployment to remote servers.
    
    Features:
    - Automated deployments
    - Rollback capability
    - Deployment verification
    - Health checks
    - Deployment logging
    """

    def __init__(self, 
                 ssh_manager: SecureSSHManager,
                 env_manager: EnvironmentManager):
        self.ssh_manager = ssh_manager
        self.env_manager = env_manager
        self.deployment_history = []

    async def deploy_code(self,
                         server_id: str,
                         code_path: Path,
                         env: str = "development") -> Dict[str, Any]:
        """
        Deploys code to a remote server.

        Args:
            server_id: Server identifier
            code_path: Path to code to deploy
            env: Environment name

        Returns:
            Dictionary containing deployment results
        """
        # Get environment configuration
        env_config = self.env_manager.get_environment(env)
        
        # Create deployment record
        deployment_id = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Connect to server
            conn = await self.ssh_manager.connect(server_id)
            
            # Create backup
            backup_result = await self._create_backup(conn)
            
            # Deploy code
            deploy_result = await self._upload_code(conn, code_path)
            
            # Update environment
            await self._update_environment(conn, env_config)
            
            # Verify deployment
            verification = await self._verify_deployment(conn)
            
            self.deployment_history.append({
                "id": deployment_id,
                "timestamp": datetime.now().isoformat(),
                "server": server_id,
                "environment": env,
                "status": "success",
                "backup_id": backup_result["backup_id"]
            })
            
            return {
                "status": "success",
                "deployment_id": deployment_id,
                "verification": verification
            }
            
        except Exception as e:
            # Roll back if needed
            await self._rollback(conn, backup_result["backup_id"])
            
            self.deployment_history.append({
                "id": deployment_id,
                "timestamp": datetime.now().isoformat(),
                "server": server_id,
                "environment": env,
                "status": "failed",
                "error": str(e)
            })
            
            raise DeploymentError(f"Deployment failed: {str(e)}") 