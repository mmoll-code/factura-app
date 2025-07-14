from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from app.core import config
from app.services.convert import run_processing_pipeline
import shutil, os
from zipfile import ZipFile
from pydantic import BaseModel, Field
from typing import Any, Dict

from ..services.billeruy_service import BillerService
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

    try:
        message = payload.message
        number = payload.origin
        print(f"number: {number}")
        
        openai_api_key = os.getenv("MM_OPEN_API_KEY")
        invoice_service = InvoiceService(openai_api_key=openai_api_key)
        extracted_data = invoice_service.interpret_message(message)

        print(f"datos_extraidos: {extracted_data}")

        # Load Biller settings from env
        biller_service = BillerService()

        branch_id = int(os.getenv("BILLER_API_BRANCH_ID", "1"))
        print(f"branch_id: {branch_id}")

        items = extracted_data["items"]
        if len(items) == 0:
            items = [
                {
                    "cantidad": 1,
                    "concepto": "Servicios de desarrollo de software",
                    "precio": 1000,
                    "indicador_facturacion": 3
                }
            ]
        print(f"items: {items}")

        biller_payload = biller_service.build_min_comprobante_payload(
            tipo_comprobante=111,
            forma_pago=1,
            sucursal=branch_id,
            moneda="UYU",
            cliente_razon_social=extracted_data["razon_social"],
            cliente_tipo_documento=extracted_data["tipo_documento"],
            cliente_documento=extracted_data["documento"],
            cliente_direccion=extracted_data["direccion"],
            cliente_pais=extracted_data.get("pais", "UY"),
            items=items
        )

        biller_result = await biller_service.crear_comprobante(biller_payload)
        print(f"Biller API result: {biller_result}")

        return {"status": "ok", "biller_result": biller_result}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
