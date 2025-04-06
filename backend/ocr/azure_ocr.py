from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

# Config desde variables de entorno (o podés hardcodear para tests)
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

client = DocumentAnalysisClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)

def analyze_invoice(image_path: str) -> dict:
    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", document=f)
        result = poller.result()

    datos = {
        "proveedor": result.fields.get("VendorName", {}).value if result.fields.get("VendorName") else None,
        "fecha": str(result.fields.get("InvoiceDate", {}).value) if result.fields.get("InvoiceDate") else None,
        "total": float(result.fields.get("InvoiceTotal", {}).value) if result.fields.get("InvoiceTotal") else None,
        "productos": []
    }

    items = result.fields.get("Items", {}).value if result.fields.get("Items") else []

    for item in items:
        datos["productos"].append({
            "nombre": item.value.get("Description", {}).value,
            "cantidad": item.value.get("Quantity", {}).value,
            "precio_unitario": item.value.get("UnitPrice", {}).value,
            "precio_total": item.value.get("Amount", {}).value,
        })

    return datos
