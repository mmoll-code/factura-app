from ..clients.billeruy_client.client import BillerAPIClient
from ..clients.billeruy_client.config import BillerSettings

class BillerService:
    def __init__(self, settings: BillerSettings):
        self.client = BillerAPIClient(settings)

    async def create_invoice(self, data: dict):
        return await self.client.post("/invoices", data)