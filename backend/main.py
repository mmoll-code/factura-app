from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import json
import re
from zipfile import ZipFile
import shutil, os
from PIL import Image
import pytesseract
from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os
from app.core import config
from app.api.endpoints import router as api_router


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
# Verificar que la API key se haya obtenido correctamente
# print(f"API Key: {api_key}")  # Para depuración, eliminar en producción



if api_key is None:
    raise ValueError("La API key de OpenAI no se encontró. Asegúrate de que el archivo .env contiene la clave correcta.")

client = OpenAI(api_key=api_key)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:4200", "https://localhost:4200"],  # origen del frontend
    allow_origins=["*"],  # origen del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
