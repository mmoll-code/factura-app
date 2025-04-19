import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

OPENAPI_KEY = os.getenv("OPENAI_API_KEY")

# 1st step: enhance PDF or images
INPUT_IMG_INVOICE = os.path.join(BASE_DIR, os.getenv("INPUT_IMG_INVOICE", ''))
OUTPUT_IMG_INVOICE = os.path.join(BASE_DIR, os.getenv("OUTPUT_IMG_INVOICE", ''))

# 2nd step: extract the data images and convert
PROCESSED_INVOICE = os.path.join(BASE_DIR, os.getenv("PROCESSED_INVOICE", ''))

print("INPUT_IMG_INVOICE", INPUT_IMG_INVOICE)
print("OUTPUT_IMG_INVOICE", OUTPUT_IMG_INVOICE)
print("PROCESSED_INVOICE", PROCESSED_INVOICE)

