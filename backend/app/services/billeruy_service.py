from ..clients.billeruy_client.client import BillerAPIClient
from ..clients.billeruy_client.schemas import (
    ComprobanteCrearPayload, ClienteInfo, SucursalInfo, ItemInfo
)
import os

class BillerService():
    def __init__(self):
        self.biller_client = BillerAPIClient()

    async def crear_comprobante(self, data: ComprobanteCrearPayload):
        payload = data.model_dump(exclude_none=True, mode="json")
        print(f"PAYLOAD data: {payload}")
        return await self.biller_client.post("v2/comprobantes/crear", payload)
    
    def build_crear_comprobante_payload(
        self,
        tipo_comprobante: int,
        forma_pago: int,
        sucursal: int,
        moneda: str,
        cliente_razon_social: str,
        cliente_tipo_documento: int,
        cliente_documento: str,
        cliente_direccion: str,
        cliente_pais: str,
        items: list
    ) -> ComprobanteCrearPayload:
        """
        Build the minimum required payload for comprobantes/crear.
        `items` should be a list of dicts with keys: cantidad, concepto, precio, indicador_facturacion
        """
        cliente = ClienteInfo(
            tipo_documento=cliente_tipo_documento,
            documento=cliente_documento,
            razon_social=cliente_razon_social,
            sucursal=SucursalInfo(pais=cliente_pais, direccion=cliente_direccion)
        )
        item_objs = [ItemInfo(**item) for item in items]
        return ComprobanteCrearPayload(
            tipo_comprobante=tipo_comprobante,
            forma_pago=forma_pago,
            sucursal=sucursal,
            moneda=moneda,
            cliente=cliente,
            items=item_objs
        )

    async def descargar_y_guardar_pdf(self, comprobante_id, comprobante_serie, comprobante_numero):
        """
        Downloads and saves PDF locally for a comprobante
        
        Args:
            comprobante_id: ID of the comprobante
            comprobante_serie: Serie of the comprobante  
            comprobante_numero: Numero of the comprobante
            
        Returns:
            dict with PDF info or None if failed
        """
        pdf_filename = None
        try:
            print(f"Attempting to download PDF for comprobante ID: {comprobante_id}")
            pdf_content = await self.obtener_comprobante_pdf(comprobante_id)
            
            # Create comprobantes directory if it doesn't exist
            comprobantes_dir = os.path.join(os.getcwd(), "comprobantes")
            os.makedirs(comprobantes_dir, exist_ok=True)
            
            # Save PDF with descriptive filename
            pdf_filename = f"comprobante_{comprobante_serie}_{comprobante_numero}_{comprobante_id}.pdf"
            pdf_path = os.path.join(comprobantes_dir, pdf_filename)
            
            print(f"Saving PDF to: {pdf_path}")
            print(f"PDF content size: {len(pdf_content)} bytes")
            
            with open(pdf_path, "wb") as f:
                f.write(pdf_content)
            
            # Verify the file was written correctly
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"PDF saved successfully: {pdf_path} (size: {file_size} bytes)")
                
                # Quick validation - check if file starts with PDF header
                with open(pdf_path, "rb") as f:
                    header = f.read(4)
                    if header == b'%PDF':
                        print("✅ Saved PDF file has valid header")
                    else:
                        print(f"⚠️ Warning: Saved file doesn't have PDF header: {header}")
                        
                return {
                    'pdf_filename': pdf_filename,
                    'pdf_path': pdf_path,
                    'pdf_size': file_size
                }
            else:
                print("❌ Error: PDF file was not created")
                return None
                
        except Exception as pdf_error:
            print(f"Error downloading/saving PDF: {pdf_error}")
            return None

    async def obtener_comprobante_pdf(self, comprobante_id: int) -> bytes:
        """Obtiene el PDF de un comprobante por su ID"""
        return await self.biller_client.get_comprobante_pdf(comprobante_id)


## Cear Comprobante example payload:
# {
#     "tipo_comprobante": 101,
#     "forma_pago": 1,
#     "sucursal": 636,
#     "moneda": "UYU",
#     "montos_brutos": 0,
#     "cliente": "-",
#     "items": [
#         {
#         	"codigo": "esteCodigo",
#             "cantidad": 1,
#             "concepto": "Pelota de fútbol",
#             "precio": 200,
#             "indicador_facturacion": 3
#         }
#     ]
# }

# {   
#     'tipo_comprobante': 111, 
#     'forma_pago': 1, 
#     'sucursal': 636, 
#     'moneda': 'UYU', 
#     'cliente': {
#         'tipo_documento': 2, 
#         'documento': '219125030014', 
#         'razon_social': 'mmollcode srl', 
#         'sucursal': {
#             'direccion': 'Calle 123', 
#             'ciudad': 'Montevideo', 
#             'departamento': 'Montevideo', 
#             'pais': 'UY'}
#         }, 
#     'items': [{'cantidad': 1, 'concepto': 'servicios de consultoría', 'precio': 1500.0, 'indicador_facturacion': 3}]
# }

