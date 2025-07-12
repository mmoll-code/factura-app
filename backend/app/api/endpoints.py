from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import FileResponse
from app.core import config
from app.services.convert import run_processing_pipeline
import shutil, os
from zipfile import ZipFile
from pydantic import BaseModel, Field
from typing import Any, Dict
import json
from ..services.invoice_service import InvoiceService

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
    print("Webhook recibido:", payload.model_dump())
    # Store payload in Redis list
    # redis = await get_redis()
    # await redis.rpush("webhook_events", payload.model_dump_json())


    # data = await request.json()
    # mensaje = data.get("message", "")
    # numero = data.get("from", "")


    try:
        print(f"HELLO")
        message = payload.message
        print(f"message: {message}")
        number = payload.origin
        print(f"number: {number}")
        
        openai_api_key = os.getenv("MM_OPEN_API_KEY")
        # openai_api_key = config.OPENAI_API_KEY
        invoice_service = InvoiceService(openai_api_key=openai_api_key)
        extracted_data = invoice_service.interpret_message(message)
        
        print(f"datos_extraidos: {extracted_data}")

        # Acá seguiría validación y flujo
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}







    # return {"status": "ok"}
