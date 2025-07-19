import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# OpenAI Configuration
OPENAPI_KEY = os.getenv("OPENAI_API_KEY")

# 1st step: enhance PDF or images
INPUT_IMG_INVOICE = os.path.join(BASE_DIR, os.getenv("INPUT_IMG_INVOICE", ''))
OUTPUT_IMG_INVOICE = os.path.join(BASE_DIR, os.getenv("OUTPUT_IMG_INVOICE", ''))

# 2nd step: extract the data images and convert
PROCESSED_INVOICE = os.path.join(BASE_DIR, os.getenv("PROCESSED_INVOICE", ''))

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Biller API Configuration
BILLER_API_BASE_URL = os.getenv("BILLER_API_BASE_URL", "https://api.biller.uy")
BILLER_API_TOKEN = os.getenv("BILLER_API_TOKEN", "1234567890")
BILLER_API_BRANCH_ID = int(os.getenv("BILLER_API_BRANCH_ID", "1"))

# WppConnect Configuration
WPPCONNECT_URL = os.getenv("WPPCONNECT_URL", "http://localhost:21465")
WPPCONNECT_TOKEN = os.getenv("WPPCONNECT_TOKEN", "changeme")
WPPCONNECT_SESSION = os.getenv("WPPCONNECT_SESSION", "default")

