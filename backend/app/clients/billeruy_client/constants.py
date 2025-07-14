from pydantic import BaseModel, Field
from typing import Optional
from enum import IntEnum

class IndicadorFacturacion(IntEnum):
    PRODUCTO = 1
    SERVICIO = 2
    PRODUCTO_Y_SERVICIO = 3
    NO_GRAVADO = 4
    EXENTO = 5
    EXPORTACION = 6
    NO_FACTURABLE = 7
    BONIFICACION = 8
    RECARGO = 9
    OTROS = 10


class ComprobanteCrearPayload(BaseModel):
    tipo_comprobante: int = Field(..., description="Tipo de comprobante. Ej: 101=e-Ticket, 111=e-Factura, etc.")
    numero_interno: Optional[str] = Field(None, description="Número interno único del comprobante.")
    forma_pago: int = Field(..., description="1=contado, 2=crédito")
    fecha_emision: Optional[str] = Field(None, description="Formato dd/mm/aaaa. Mínimo 01/10/2011.")
    fecha_vencimiento: Optional[str] = Field(None, description="Formato dd/mm/aaaa.")
    sucursal: int = Field(..., description="ID de sucursal de la empresa en Biller.")
    moneda: str = Field(..., description="Moneda. Ej: UYU, USD, ARS, BRL, EUR.")
    tasa_cambio: Optional[float] = Field(None, description="Tasa de cambio. Opcional.")
    montos_brutos: Optional[bool] = Field(None, description="True/1: precios incluyen IVA. False/0: se suma IVA.")
    numero_orden: Optional[str] = Field(None, description="Número de orden del CFE.")
    lugar_entrega: Optional[str] = Field(None, description="Lugar de entrega.")
    # ... continue for all fields
