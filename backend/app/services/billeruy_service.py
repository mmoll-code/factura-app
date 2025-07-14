from ..clients.billeruy_client.client import BillerAPIClient
from app.clients.billeruy_client.schemas import (
    ComprobanteCrearPayload, ClienteInfo, SucursalInfo, ItemInfo
)

class BillerService():
    def __init__(self):
        self.biller_client = BillerAPIClient()

    async def crear_comprobante(self, data: ComprobanteCrearPayload):
        payload = data.model_dump(exclude_none=True, mode="json")
        print(f"PAYLOAD data: {payload}")
        return await self.biller_client.post("/v2/comprobantes/crear", payload)
    
    
    def build_biller_payload(
        nombre_fantasia: str,
        tipo_documento: int,
        documento: str,
        direccion: str,
        ciudad: str,
        departamento: str,
        pais: str = "UY"
    ) -> dict:
        
        print(f"build_biller_payload: {nombre_fantasia}, {tipo_documento}, {documento}, {direccion}, {ciudad}, {departamento}, {pais}")
        return {
            "nombre_fantasia": nombre_fantasia,
            "tipo_documento": tipo_documento,
            "documento": documento,
            "direccion": direccion,
            "ciudad": ciudad,
            "departamento": departamento,
            "pais": pais
        }
    
    
    def build_min_comprobante_payload(
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
