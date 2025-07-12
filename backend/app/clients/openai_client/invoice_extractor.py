import json
from typing import Dict
from .base_client import OpenAIBaseClient
from .prompts import INVOICE_EXTRACTION_PROMPT
from .exceptions import OpenAIExtractionError

class OpenAIInvoiceExtractor(OpenAIBaseClient):
    def extract_invoice_data(self, message: str) -> Dict:
        prompt = INVOICE_EXTRACTION_PROMPT.format(message=message)
        messages = [{"role": "user", "content": prompt}]

        try:
            raw_response = self.chat_completion(messages)
            return json.loads(raw_response)

        except json.JSONDecodeError as e:
            raise OpenAIExtractionError(f"Respuesta inválida de OpenAI: {raw_response}") from e

        except Exception as e:
            print(f"Error general al comunicar con OpenAI: {e}")
            raise OpenAIExtractionError("Error general al comunicar con OpenAI") from e
