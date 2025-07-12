INVOICE_EXTRACTION_PROMPT = """
Extraé del siguiente texto los siguientes campos para emitir una factura:

- razon_social
- rut
- direccion

Devolveme solo un JSON válido con los campos mencionados, sin explicaciones adicionales.

Texto:
{message}
"""
