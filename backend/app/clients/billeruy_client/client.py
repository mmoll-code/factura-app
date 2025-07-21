# biller/client.py
import httpx
from .exceptions import BillerAPIError
import os
import json

class BillerAPIClient:
    def __init__(self):
        self.base_url = os.getenv("BILLER_API_BASE_URL")
        self.token = os.getenv("BILLER_API_TOKEN")
        
        # Validate required environment variables
        if not self.base_url:
            raise ValueError("BILLER_API_BASE_URL environment variable is required")
        if not self.token:
            raise ValueError("BILLER_API_TOKEN environment variable is required")
            
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        
        # Initialize persistent client as None
        self._client = None

    async def _get_client(self):
        """Get or create persistent HTTP client with cookie support"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                cookies=httpx.Cookies()
            )
        return self._client

    async def close(self):
        """Close the HTTP client"""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def post(self, endpoint: str, data: dict):
        url = f"{self.base_url}/{endpoint}"
        print(f"Making request to: {url}")
        
        try:
            # Ensure proper JSON serialization with double quotes
            json_data = json.dumps(data, ensure_ascii=False)
            print(f"JSON payload: {json_data}")
            
            client = await self._get_client()
            response = await client.post(
                url, 
                headers=self.headers, 
                content=json_data
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            
            if response.status_code >= 400:
                error_message = self._parse_error_response(response.text)
                print(f"BillerAPIError: {error_message}")
                raise BillerAPIError(response.status_code, error_message)
            return response.json()
        except Exception as e:
            print(f"Error in POST request: {e}")
            raise

    async def test_connection(self):
        """Test basic connectivity to Biller API"""
        url = f"{self.base_url}/v2/comprobantes/crear"
        print(f"Testing connection to: {url}")
        try:
            client = await self._get_client()
            # Just test connectivity with a HEAD request
            response = await client.head(url)
            print(f"Connection test result: {response.status_code}")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    async def test_postman_payload(self):
        """Test with the exact payload that works in Postman"""
        test_payload = {
            "tipo_comprobante": 111,
            "forma_pago": 1,
            "sucursal": 636,
            "moneda": "UYU",
            "cliente": {
                "tipo_documento": 2,
                "documento": "219125030014",
                "razon_social": "mmollcode srl",
                "sucursal": {
                    "direccion": "Calle 123",
                    "ciudad": "Montevideo",
                    "departamento": "Montevideo",
                    "pais": "UY"
                }
            },
            "items": [
                {
                    "cantidad": 1,
                    "concepto": "servicios de consultoría",
                    "precio": 1500.0,
                    "indicador_facturacion": 3
                }
            ]
        }
        
        print("Testing with Postman payload...")
        return await self.post("/v2/comprobantes/crear", test_payload)

    async def get_comprobante_pdf(self, comprobante_id: int) -> bytes:
        """Download PDF content for a comprobante"""
        # url = f"{self.base_url}/v2/comprobantes/{comprobante_id}/pdf"
        url = f"{self.base_url}/v2/comprobantes/pdf?id={comprobante_id}"
        print(f"Downloading PDF from: {url}")
        
        try:
            client = await self._get_client()
            response = await client.get(url, headers=self.headers)
            
            print(f"PDF Response status: {response.status_code}")
            print(f"PDF Response headers: {dict(response.headers)}")
            
            if response.status_code >= 400:
                error_message = self._parse_error_response(response.text)
                print(f"BillerAPIError: {error_message}")
                raise BillerAPIError(response.status_code, error_message)
            
            # Get content and analyze it
            content = response.content
            print(f"🔍 PDF Content Analysis:")
            print(f"  - Content type: {type(content)}")
            print(f"  - Content size: {len(content)} bytes")
            
            # Try to detect content format
            # import base64
            # pdf_bytes = base64.b64decode(content)
           
            return content
        except Exception as e:
            print(f"Error downloading PDF: {e}")
            raise

    def _parse_error_response(self, error_text: str) -> str:
        """Parse API error response and return a user-friendly message"""
        try:
            # Try to parse as JSON array of errors
            errors = json.loads(error_text)
            if isinstance(errors, list):
                parsed_errors = []
                for error in errors:
                    field = error.get("field", "Unknown field")
                    messages = error.get("message", [])
                    if isinstance(messages, list):
                        for msg in messages:
                            parsed_errors.append(f"• {field}: {msg}")
                    else:
                        parsed_errors.append(f"• {field}: {messages}")
                return "Errores de validación:\n" + "\n".join(parsed_errors)
            else:
                return f"Error de API: {error_text}"
        except (json.JSONDecodeError, KeyError, TypeError):
            # If parsing fails, return original error
            return f"Error de API: {error_text}"
