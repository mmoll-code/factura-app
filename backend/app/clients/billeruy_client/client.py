# biller/client.py
import httpx
from .exceptions import BillerAPIError
import os

class BillerAPIClient:
    def __init__(self):

        self.base_url = os.getenv("BILLER_API_BASE_URL")
        self.token = os.getenv("BILLER_API_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    async def post(self, endpoint: str, data: dict):
        url = f"{self.base_url}/{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=data)
            if response.status_code >= 400:
                print(f"BillerAPIError: {response.text}")
                raise BillerAPIError(response.status_code, response.text)
            return response.json()
