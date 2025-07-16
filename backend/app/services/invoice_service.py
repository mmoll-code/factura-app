

from ..clients.openai_client.exceptions import OpenAIExtractionError
from ..clients.openai_client.invoice_extractor import OpenAIInvoiceExtractor



class InvoiceService:
    def __init__(self, openai_api_key: str):
        self.extractor = OpenAIInvoiceExtractor(api_key=openai_api_key)

    def interpret_message(self, text_message: str) -> dict:
        try:
            return self.extractor.extract_invoice_data(text_message)
        except OpenAIExtractionError as e:
            # You can log or raise a higher-level error here
            raise e
