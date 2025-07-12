from pydantic import BaseModel
from typing import Any, Dict

class WebhookRequest(BaseModel):
    # Define your expected fields here, for example:
    event: str
    payload: Dict[str, Any]