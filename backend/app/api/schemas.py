from pydantic import BaseModel, Field
from typing import Any, Dict

class WebhookRequest(BaseModel):
    # Define your expected fields here, for example:
    event: str
    payload: Dict[str, Any]


class WhatsappWebhookMessage(BaseModel):
    event: str = Field(None, description="Tipo de evento recibido desde WaApi, típicamente 'message'")
    session: str = Field(None, description="Nombre de la sesión de WhatsApp")
    id: str = Field(None, description="ID del mensaje")
    body: str = Field(None, description="Cuerpo del mensaje")
    from_: str = Field(None, alias="from", description="Número de WhatsApp del remitente")
    to: str = Field(None, description="Número de WhatsApp del destinatario")
    type: str = Field(None, description="Tipo de mensaje (chat, image, etc)")
    timestamp: int = Field(None, description="Timestamp del mensaje")
    isGroupMsg: bool = Field(None, description="Indica si es mensaje de grupo")
    chatId: str = Field(None, description="ID del chat")
    # Puedes agregar más campos según lo que recibas normalmente

    class Config:
        extra = "allow"  # Permite campos adicionales no definidos explícitamente
        allow_population_by_field_name = True


# {
#   "event": "message",
#   "origin": "099747179",
#   "message": "MMOLLCODE SRL\nRUT 219125030014\nDoctor Manuel Albo 2656\nSaludos Martín Moll.\n"
# }