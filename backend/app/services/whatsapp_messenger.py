import httpx
from typing import Optional

class WhatsappMessenger:
    def __init__(self, base_url: str, token: str, session: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.session = session

    async def send_message(self, phone: str, message: str, is_group: Optional[bool] = False) -> bool:
        url = f"{self.base_url}/api/{self.session}/send-message"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        data = {
            "phone": phone,
            "message": message,
            "isGroup": is_group or False
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=data)
            if resp.status_code >= 400:
                print(f"Error sending WhatsApp message: {resp.text}")
                return False
        return True 