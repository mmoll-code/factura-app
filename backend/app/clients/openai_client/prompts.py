INVOICE_EXTRACTION_PROMPT = """
Extraé del siguiente texto los siguientes campos para emitir una factura:

- tipo_documento: 2 para persona jurídica o si se especifica un RUT, si hay omisión entonces es 2.
- razon_social: nombre de la empresa.
- documento: número de identificación de la empresa, puede ser un RUT o cédula.
- direccion: dirección de la empresa, si hay omisión entonces "Calle 123".
- ciudad: ciudad de la empresa, si hay omisión entonces es "Montevideo".
- departamento: departamento de la empresa, si hay omisión entonces es "Montevideo".
- pais: país de la empresa, si hay omisión entonces es "UY".
- items: una lista de objetos con concepto, cantidad, precio e indicador_facturacion: 3, si hay omisión entonces es una lista vacía.

Devolveme solo un JSON válido con los campos mencionados, sin explicaciones adicionales.

Texto:
{message}
"""

INTENT_DETECTION_PROMPT = """
Analizá el siguiente mensaje y respondé solo con un JSON válido con el campo:
- intencion: puede ser "crear_comprobante", "consultar_estado", "ayuda", "otro".
No agregues explicaciones ni texto adicional.

Mensaje:
{message}
"""
