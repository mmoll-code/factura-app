import httpx
from typing import Optional
import base64

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

    async def send_file(self, phone: str, file_path: str, filename: str, caption: Optional[str] = None, is_group: Optional[bool] = False) -> bool:
        """
        Send file via WhatsApp using base64 encoding
        
        Args:
            phone: Recipient phone number
            file_path: Path to the file to send
            filename: Name for the file
            caption: Optional caption for the file
            is_group: Whether it's a group message
            
        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Read file and encode to base64 with MIME prefix
            with open(file_path, "rb") as file:
                file_content = file.read()
                base64_raw = base64.b64encode(file_content).decode('utf-8')
                # Add MIME prefix as required by wppconnect
                base64_content = f"data:application/pdf;base64,{base64_raw}"
            
            url = f"{self.base_url}/api/{self.session}/send-file-base64"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            data = {
                "phone": [phone],  # phone must be array according to messageController.ts
                "base64": base64_content,
                "filename": filename,
                "isGroup": is_group or False
            }
            
            if caption:
                data["caption"] = caption
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, headers=headers, json=data)
                if resp.status_code >= 400:
                    print(f"Error sending WhatsApp file: {resp.text}")
                    return False
            return True
            
        except Exception as e:
            print(f"Error sending file via WhatsApp: {e}")
            return False 