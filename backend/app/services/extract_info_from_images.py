import base64
import json
import os
from openai import AzureOpenAI
import openai

for var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(var, None)

# Eliminar uso heredado de proxies si existen
if hasattr(openai, 'proxies'):
    del openai.proxies

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def extract_info_from_images(image_files):

    gpt_4o_model = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT")

    # no_proxy_http_client = httpx.Client(proxies=None)
    gpt_client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-05-01-preview"
    )
    
    extracted_data = []

    system_message = (
        "Usted es un experto analizador de tickets y recibos de compras"
    )

    parameters_schema = {
        "type": "object",
        "properties": {       
            # "producto": {
            #     "type": "string",
            #     "enum": ["alimentacion", "transporte","alojamiento","no_especifica"],
            #      "description": 'Rubro del gasto realizado',
            # },
            "descripcion": {
                "type": "string",
                "description": 'Breve descripcion de la factura o documento',
            },
            "fecha": {
                "type": "string",
                "description": 'La fecha de creacion del documento o factura. Debe tener formato dd/mm/YYYY',
            },
            "contrato": {
                "type": "string",
                "description": 'numero de contrato',
            },
            "numeroFactura": {
                "type": "string",
                "description": 'numero de la documento',
            },
            "rut proveedor": {
                "type": "string",
                "description": 'codigo numerico de entre 9 a 12 digitos',
            },
            "rut comprador": {
                "type": "string",
                "description": 'codigo numerico de entre 9 a 12 digitos',
            },
            "moneda": {
                "type": "string",
                "enum": ["USD", "UYU", "EU", "Gs", "no_especificado"],
                "description": 'moneda del documento o factura. Puede ser dolares - USD, pesos - UYU, euros - EU, guaranies - Gs',
            },
            "iva 10": {
                "type": "number",
                "description": 'total iva 10% de la factura o documento',
            },
            "iva 22": {
                "type": "number",
                "description": 'total iva 22% de la factura o documento',
            },
            "iva 0": {
                "type": "number",
                "description": 'total iva 0% de la factura o documento excento',
            },
            "iva total": {
                "type": "number",
                "description": 'total iva de la factura o documento',
            },
            "subtotal": {
                "type": "number",
                "description": 'el subtotal del importe de la factura',
            },
            "total": {
                "type": "number",
                "description": 'el total del importe de la factura',
            },
            "redondeo": {
                "type": "number",
                "description": 'el redondeo de la factura',
            },
            "total a pagar": {
                "type": "number",
                "description": 'el total a pagar de la factura',
            },
            "observaciones": {
                "type": "string",
                "description": 'el total del importe de la factura',
            },
            "tipo": {
                "type": "string",
                "enum": ["factura", "nota de credito", "ticket", "nota de debito", "recibo","no_especificado"],
                "description": 'tipos de documentos de compra',
            },
            "items": {
                "type": "array",
                "description": "Lista de ítems, productos, conceptos, articulos incluidos en la factura.",
                "items": {
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "El nombre del ítem, producto, concepto, articulo."
                        },
                        "cantidad": {
                            "type": "number",
                            "description": "La cantidad del ítem."
                        },
                        "precio unitario": {
                            "type": "number",
                            "description": "El precio unitario indicado en cada linea de la factura."
                        },
                        "precio total": {
                            "type": "number",
                            "description": "El precio total indicado en cada linea de la factura."
                        }
                    },
                    "required": ["nombre", "cantidad", "precio unitario", "precio total"]
                }
            }
        },
        "required": ["producto", "descripcion", "fecha", "tipo", "moneda", "iva 10", "iva 22", "iva 0", "iva total", "subtotal", "total", "redondeo", "total a pagar","observaciones", "contrato", "numeroFactura", "rut proveedor", "rut comprador", "items"],
        }

    function_schema = {
        "name": "invoice_analyzer",
        "description": "Analiza datos extraidos de tickets y facturas de compra.",
        "parameters": parameters_schema,
    }

    for i in image_files:
        image_file = os.path.join(path_to_tickets, i)
        encoded_image = base64.b64encode(open(image_file, 'rb').read()).decode('ascii')

        user_message_template = (
            f"""dado el siguiente ticket o recibo de compra adjunto.
            ### Extraiga los datos relevantes
            No debes incluir ninguna opinión o interpretación personal o inferir informacion, sino que debes centrarte en utilizar la informacion proporcionada.
            ### El formato de la respuesta debe ser un objeto json parseable.
            """
        )

        gpt_response = gpt_client.chat.completions.create(
            model=gpt_4o_model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": [{
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": user_message_template
                        }
                    ]},
            ],
            functions=[function_schema],
            function_call={"name": function_schema["name"]},
        )

        function_call = gpt_response.choices[0].message.function_call
        used_tokens = gpt_response.usage
        print(function_call.arguments)
        print(used_tokens)
        
        json_result = json.loads(function_call.arguments)
        folder_path = "processed-docs-json-gpt4o"

        with open(os.path.join(folder_path, i.split('.')[0] + "_gpt.json"), "w") as file_gpt:
            json.dump(json_result, file_gpt)

    return extracted_data


FOLDER_PATH = os.getenv("FOLDER_PATH")

if not FOLDER_PATH:
    raise ValueError("FOLDER_PATH no está definido en el entorno")

path_to_tickets = os.getenv("FOLDER_PATH")
all_processed_files = os.listdir(path_to_tickets)
extracted_info = extract_info_from_images(all_processed_files)
