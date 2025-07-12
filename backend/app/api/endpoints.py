from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import FileResponse
from app.core import config
from app.services.convert import run_processing_pipeline
import shutil, os
from zipfile import ZipFile
from pydantic import BaseModel, Field
from typing import Any, Dict

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


@router.post(
    "/webhook/",
    summary="Receive webhook events",
    description="Receives a webhook event with a JSON payload."
)
async def webhook(request: Request):
    """
    Receives a webhook event.
    - **event**: The event type.
    - **payload**: The event payload as a JSON object.
    """
    # Your processing logic here
    payload = await request.json()
    print("Webhook recibido:", payload)
    return {"status": "ok"}
