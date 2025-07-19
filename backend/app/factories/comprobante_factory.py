import os
from app.core import config
from app.clients.billeruy_client.schemas import (
    ComprobanteCrearPayload, ClienteInfo, SucursalInfo, ItemInfo
)


class ComprobantePayloadFactory:
    """Factory para crear payloads de comprobantes desde datos extraídos por IA"""
    
    @staticmethod
    def build_from_invoice_data(
        invoice_data: dict,
        tipo_comprobante: int = 111,
        forma_pago: int = 1,
        sucursal: int = None,
        moneda: str = "UYU",
        **kwargs
    ) -> ComprobanteCrearPayload:
        """
        Construye un ComprobanteCrearPayload desde datos extraídos por IA
        
        Args:
            invoice_data: Datos extraídos por OpenAI (razon_social, documento, etc.)
            tipo_comprobante: Tipo de comprobante (default: 111 = e-Factura)
            forma_pago: Forma de pago (default: 1 = contado)
            sucursal: ID de sucursal (default: desde config.BILLER_API_BRANCH_ID)
            moneda: Moneda (default: UYU)
            **kwargs: Otros parámetros opcionales
            
        Returns:
            ComprobanteCrearPayload listo para enviar a la API
        """
        
        # Get default sucursal from config if not provided
        if sucursal is None:
            sucursal = config.BILLER_API_BRANCH_ID
        
        # Build cliente info
        cliente = ClienteInfo(
            tipo_documento=invoice_data.get("tipo_documento", 3),
            documento=invoice_data.get("documento", "12345678"),
            razon_social=invoice_data.get("razon_social", "Cliente"),
            sucursal=SucursalInfo(
                pais=invoice_data.get("pais", "UY"),
                direccion=invoice_data.get("direccion", "Calle 123"),
                ciudad=invoice_data.get("ciudad", "Montevideo"),
                departamento=invoice_data.get("departamento", "Montevideo")
            )
        )
        
        # Build items info
        items_data = invoice_data.get("items", [])
        if not items_data:
            # Default item if none provided
            items_data = [
                {
                    "cantidad": 1,
                    "concepto": "Servicios",
                    "precio": 1000.0,
                    "indicador_facturacion": 3
                }
            ]
        
        # Convert items to ItemInfo objects
        item_objs = []
        for item in items_data:
            item_obj = ItemInfo(
                cantidad=item.get("cantidad", 1),
                concepto=item.get("concepto", "Servicios"),
                precio=item.get("precio", 0.0),
                indicador_facturacion=item.get("indicador_facturacion", 3)
            )
            item_objs.append(item_obj)
        
        # Build complete payload
        return ComprobanteCrearPayload(
            tipo_comprobante=tipo_comprobante,
            forma_pago=forma_pago,
            sucursal=sucursal,
            moneda=moneda,
            cliente=cliente,
            items=item_objs,
            # Add any additional kwargs
            **{k: v for k, v in kwargs.items() if k in ComprobanteCrearPayload.model_fields}
        ) 