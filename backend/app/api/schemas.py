from pydantic import BaseModel, Field
from typing import Any, Dict

class WebhookRequest(BaseModel):
    # Define your expected fields here, for example:
    event: str
    payload: Dict[str, Any]


class WhatsappWebhookMessage(BaseModel):
    event: str = Field(..., description="Tipo de evento recibido desde WaApi, típicamente 'message'")
    # event: str = Field(..., description="message")
    origin: str = Field(..., description="Número de WhatsApp del usuario que envió el mensaje")
    # origin: str = Field(..., description="099747179")
    message: str = Field(..., description="Mensaje de texto enviado por el usuario")
    # message: str = Field(..., description="MMOLLCODE SRL\nRUT 219125030014\nDoctor Manuel Albo 2656\nSaludos Martín Moll.\n")



# {
#   "event": "message",
#   "origin": "099747179",
#   "message": "MMOLLCODE SRL\nRUT 219125030014\nDoctor Manuel Albo 2656\nSaludos Martín Moll.\n"
# }