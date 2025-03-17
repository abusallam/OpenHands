import httpx
import asyncio
from typing import Dict, Any

class AiCoderClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json"
        }

    async def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            response = await client.request(
                method=method,
                url=url,
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    # Example methods to interact with your AI Coder API
    async def generate_code(self, prompt: str) -> Dict[str, Any]:
        return await self.make_request(
            method="POST",
            endpoint="/api/v1/generate",
            data={"prompt": prompt}
        )

    async def analyze_code(self, code: str) -> Dict[str, Any]:
        return await self.make_request(
            method="POST",
            endpoint="/api/v1/analyze",
            data={"code": code}
        )

# Example usage
async def main():
    # Initialize client
    client = AiCoderClient(
        base_url="https://your-coolify-deployment-url",
        api_key="your_api_key_here"
    )

    try:
        # Example: Generate code
        result = await client.generate_code(
            prompt="Create a Python function to calculate fibonacci sequence"
        )
        print("Generated Code:", result)

        # Example: Analyze code
        analysis = await client.analyze_code(
            code="def hello(): print('world')"
        )
        print("Code Analysis:", analysis)

    except httpx.HTTPError as e:
        print(f"HTTP Error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 