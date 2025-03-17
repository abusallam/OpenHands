from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time
from typing import Dict, List
import jwt
from config import MCPConfig

security = HTTPBearer()
config = MCPConfig()

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}

    async def check_rate_limit(self, client_id: str) -> bool:
        current_time = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = []

        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if current_time - req_time < config.rate_limit_period
        ]

        if len(self.requests[client_id]) >= config.rate_limit_requests:
            return False

        self.requests[client_id].append(current_time)
        return True

rate_limiter = RateLimiter()

async def verify_token(credentials: HTTPAuthorizationCredentials) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            config.auth_secret,
            algorithms=["HS256"]
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

async def rate_limit_middleware(request: Request, call_next):
    if config.auth_enabled:
        credentials = await security(request)
        payload = await verify_token(credentials)
        client_id = payload.get("client_id", "anonymous")
    else:
        client_id = request.client.host

    if not await rate_limiter.check_rate_limit(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )

    response = await call_next(request)
    return response 