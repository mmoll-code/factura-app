from pydantic import BaseModel, Field
from typing import List, Optional, Union
from .constants import IndicadorFacturacion



class SucursalInfo(BaseModel):
    direccion: str = "Calle 123"
    ciudad: Optional[str] = "Montevideo"
    departamento: Optional[str] = "Montevideo"
    pais: str = "UY"

class ClienteInfo(BaseModel):
    tipo_documento: int
    documento: str
    razon_social: str
    nombre_fantasia: Optional[str] = None
    informacion_adicional: Optional[str] = None
    sucursal: SucursalInfo

class ItemInfo(BaseModel):
    codigo: Optional[Union[str, int]] = None
    cantidad: int
    concepto: str
    precio: float
    indicador_facturacion: IndicadorFacturacion = Field(
        ...,
        description=(
            "Tipo de ítem facturado. "
            "1=Producto, 2=Servicio, 3=Producto y servicio, 4=No gravado, "
            "5=Exento, 6=Exportación, 7=No facturable, 8=Bonificación, "
            "9=Recargo, 10=Otros"
        )
    )
    descuento_tipo: Optional[str] = None
    descuento_cantidad: Optional[float] = None
    recargo_tipo: Optional[str] = None
    recargo_cantidad: Optional[float] = None

class DescuentoRecargoInfo(BaseModel):
    tipo: str
    cantidad: float

class ComprobanteCrearPayload(BaseModel):
    tipo_comprobante: int
    numero_interno: Optional[str] = None
    forma_pago: int
    fecha_emision: Optional[str] = None  # dd/mm/aaaa
    fecha_vencimiento: Optional[str] = None  # dd/mm/aaaa
    sucursal: int
    moneda: str
    tasa_cambio: Optional[float] = None
    montos_brutos: Optional[bool] = None
    numero_orden: Optional[str] = None
    lugar_entrega: Optional[str] = None
    cliente: ClienteInfo
    items: List[ItemInfo]
    descuentosRecargos: Optional[List[DescuentoRecargoInfo]] = None
    referencia_global: Optional[bool] = None
    razon_referencia: Optional[str] = None
    referencias: Optional[str] = None
    tipo_traslado: Optional[int] = None
    adenda: Optional[str] = None
    informacion_adicional: Optional[str] = None
    modalidad_venta: Optional[int] = None
    clausula_venta: Optional[str] = None
    via_transporte: Optional[int] = None
    indicador_pagos_terceros: Optional[bool] = None
