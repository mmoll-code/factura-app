# biller/client.py
import httpx
from .config import BillerSettings
from .exceptions import BillerAPIError

class BillerAPIClient:
    def __init__(self, settings: BillerSettings):
        self.base_url = settings.api_base_url
        self.token = settings.api_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def post(self, endpoint: str, data: dict):
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=data)
            if response.status_code >= 400:
                raise BillerAPIError(response.status_code, response.text)
            return response.json()
