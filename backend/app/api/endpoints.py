from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.core import config
from app.services.convert import run_processing_pipeline
import shutil, os
from zipfile import ZipFile
from pydantic import BaseModel, Field
from typing import Any, Dict

from ..clients.openai_client.invoice_extractor import OpenAIIntentDetector, OpenAIInvoiceExtractor

from ..services.billeruy_service import BillerService
from ..services.invoice_service import InvoiceService
from ..services.chat_memory import ChatMemoryService
from ..clients.openai_client.base_client import OpenAIBaseClient
import httpx
from ..services.conversational_ai_service import ConversationalAIService
from ..services.whatsapp_messenger import WhatsappMessenger

from .schemas import WhatsappWebhookMessage

router = APIRouter()

@router.post("/process_zip/")
async def process_zip(file: UploadFile = File(...)):
    temp_zip = "temp.zip"
    DESTINATION_PATH = config.INPUT_IMG_INVOICE
    print(f"DESTINATION_PATH: {DESTINATION_PATH}")
    print("Recibiendo archivo...")
    with open(temp_zip, "wb") as f:
        shutil.copyfileobj(file.file, f)
    print(f"🗂️ Extrayendo contenido a {DESTINATION_PATH}...")
    with ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall(DESTINATION_PATH)
    run_processing_pipeline()
    return {"message": "Procesamiento exitoso", "download": "/download"}

@router.get("/download")
def download_excel():
    return FileResponse(
        "output/facturas.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="facturas.xlsx"
    )


class WebhookPayload(BaseModel):
    event: str = Field(..., example="invoice_created")
    payload: Dict[str, Any] = Field(..., example={"invoice_id": 123, "amount": 456.78})

@router.post(
    "/webhook-waapi/",
    summary="Receive webhook events",
    description="Receives a webhook event with a JSON payload."
)
async def webhook_waapi(payload: WhatsappWebhookMessage):
    """
    Receives a webhook event.
    - **event**: The event type.
    - **payload**: The event payload as a JSON object.
    """
    try:
        if payload.event == "onmessage":
            relevant_data = {
                "from": payload.from_,
                "to": payload.to,
                "body": payload.body,
                "timestamp": payload.timestamp,
                "chatId": payload.chatId,
                "type": payload.type,
                "isGroupMsg": payload.isGroupMsg,
            }
            print("Relevant message data:", relevant_data)

            # Save message to chat memory (Redis)
            chat_memory = ChatMemoryService(redis_url=config.REDIS_URL)
            await chat_memory.add_message(payload.chatId, relevant_data)

            # Get chat history
            history = await chat_memory.get_history(payload.chatId, limit=20)

            # Conversational AI Service
            ai_service = ConversationalAIService(openai_api_key=config.OPENAPI_KEY)
            openai_response = ai_service.get_ai_response(history, payload.from_)

            intent_detector = OpenAIIntentDetector(api_key=config.OPENAPI_KEY)
            intent = intent_detector.detect_intent(payload.body)
            print(f"intent: {intent}")

            if intent == "crear_comprobante":
                extractor = OpenAIInvoiceExtractor(api_key=config.OPENAPI_KEY)
                invoice_data = extractor.extract_invoice_data(payload.body)
                print(f"invoice_data: {invoice_data}")
                
                try:
                    biller_service = BillerService()
                    # Use build_min_comprobante_payload to create proper payload
                    comprobante_payload = biller_service.build_min_comprobante_payload(
                        tipo_comprobante=111,
                        forma_pago=1,
                        sucursal=int(os.getenv("BILLER_API_BRANCH_ID", "1")),
                        moneda="UYU",
                        cliente_razon_social=invoice_data.get("razon_social", "Cliente"),
                        cliente_tipo_documento=invoice_data.get("tipo_documento", 3),
                        cliente_documento=invoice_data.get("documento", "12345678"),
                        cliente_direccion=invoice_data.get("direccion", "Calle 123"),
                        cliente_pais=invoice_data.get("pais", "UY"),
                        items=invoice_data.get("items", [])
                    )
                    
                    biller_result = await biller_service.crear_comprobante(comprobante_payload)
                    response_message = f"Comprobante emitido con éxito. Nro: {biller_result.get('numero', 'N/A')}"
                except Exception as e:
                    response_message = f"Ocurrió un error al emitir el comprobante: {str(e)}"
            else:
                # Use conversational AI response
                response_message = openai_response

            # Save response to chat memory
            ai_message = {
                "from": payload.to,
                "to": payload.from_,
                "body": response_message,
                "timestamp": int(__import__('time').time()),
                "chatId": payload.chatId,
                "type": "chat",
                "isGroupMsg": False
            }
            await chat_memory.add_message(payload.chatId, ai_message)

            # Whatsapp Messenger
            wppconnect_url = os.getenv("WPPCONNECT_URL", "http://wppconnect:21465")
            wppconnect_token = os.getenv("WPPCONNECT_TOKEN", "changeme")
            session = payload.session or os.getenv("WPPCONNECT_SESSION", "default")
            
            print(f"WhatsApp config - URL: {wppconnect_url}, Token: {'*' * len(wppconnect_token) if wppconnect_token else 'None'}, Session: {session}")
            
            try:
                messenger = WhatsappMessenger(
                    base_url=wppconnect_url,
                    token=wppconnect_token,
                    session=session
                )
                print(f"Sending WhatsApp message to: {payload.from_}")
                sent = await messenger.send_message(
                    phone=payload.from_,
                    message=response_message,
                    is_group=payload.isGroupMsg or False
                )
                if not sent:
                    print("Warning: WhatsApp message failed to send")
                    return {"status": "ok", "warning": "Comprobante creado pero no se pudo enviar notificación"}
                print("WhatsApp message sent successfully")
            except Exception as whatsapp_error:
                print(f"WhatsApp error: {whatsapp_error}")
                # Don't fail the whole request if WhatsApp fails
                return {"status": "ok", "warning": f"Comprobante creado pero error en WhatsApp: {whatsapp_error}"}

        else:
            print(f"Ignored event: {payload.event}")

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
