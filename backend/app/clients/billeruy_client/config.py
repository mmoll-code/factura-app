# biller/config.py
from pydantic import BaseSettings

class BillerSettings(BaseSettings):
    api_base_url: str
    api_token: str

    class Config:
        env_prefix = "BILLER_"
        env_file = ".env"
