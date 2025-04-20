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


from app.services.convert import run_processing_pipeline

@app.post("/process_zip/")
async def process_zip(file: UploadFile = File(...)):
    temp_zip = "temp.zip"
    DESTINATION_PATH = config.INPUT_IMG_INVOICE
    print(f"DESTINATION_PATH: {DESTINATION_PATH}")
    # OUTPUTFILE = f"{config.PROCESSED_INVOICE}/facturas.xlsx"

    print("Recibiendo archivo...")

    # os.makedirs("output", exist_ok=True)
    # Save ZIP in disk: "wb" = write binary
    with open(temp_zip, "wb") as f:
        shutil.copyfileobj(file.file, f)

    print(f"🗂️ Extrayendo contenido a {DESTINATION_PATH}...")

    # Descomprimir el ZIP (queda en la carpeta del zip)
    with ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall(DESTINATION_PATH)


    # Buscar la primera carpeta válida dentro de "extracted"
    # subdirs = [
    #     d for d in os.listdir(DESTINATION_PATH)
    #     if os.path.isdir(os.path.join(DESTINATION_PATH, d)) and not d.startswith('__') and not d.startswith('.')
    # ]

    # if not subdirs:
    #     shutil.rmtree(DESTINATION_PATH, ignore_errors=True)
    #     os.remove(temp_zip)
    #     return {"message": "No se encontró ninguna carpeta válida dentro del ZIP."}

    # contenido_dir = os.path.join(DESTINATION_PATH, subdirs[0])  # Carpeta descomprimida real

    # print(f"📁 Carpeta seleccionada: {contenido_dir}")
    # print(f"🗂 Contenido: {os.listdir(contenido_dir)}")

    run_processing_pipeline()

    # rows = []

    # for fname in os.listdir(contenido_dir):
    #     if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
    #         img_path = os.path.join(contenido_dir, fname)
    #         print(f"📸 Procesando imagen: {img_path}")

    #         # Verificar si la imagen es válida
    #         try:
    #             img = Image.open(img_path)
    #             img.verify()  # Verifica si la imagen es válida
    #         except Exception as e:
    #             print(f"❌ Error al abrir la imagen {fname}: {e}")
    #             continue

    #         text = pytesseract.image_to_string(Image.open(img_path))
    #         print("📝 Texto extraído: ", text)

    #         try:
    #             response = client.chat.completions.create(
    #                 # model="gpt-4-turbo",
    #                 model="gpt-3.5-turbo",
    #                 messages=[
    #                     {
    #                         "role": "system",
    #                         "content": "Extraé los campos proveedor, fecha, monto_total, iva y numero_factura del siguiente texto de una factura. Devolvelo en formato JSON."
    #                     },
    #                     {
    #                         "role": "user",
    #                         "content": text
    #                     }
    #                 ]
    #                 # messages=[
    #                 #     {"role": "system", "content": "You are a helpful assistant."},
    #                 #     {"role": "user", "content": "Hola, ¿me puedes ayudar con un test?"}
    #                 # ],
    #             )

    #             content = response.choices[0].message.content
    #             print("🧠 GPT response:", content)
    #             # Limpieza del texto: elimina backticks y etiquetas tipo ```json
    #             cleaned = re.sub(r"^```json|```$", "", content.strip(), flags=re.IGNORECASE).strip("` \n")

    #             try:
    #                 parsed = json.loads(cleaned)
    #             except json.JSONDecodeError:
    #                 print("⚠️ No se pudo parsear como JSON. Usando eval como fallback.")
    #                 parsed = eval(cleaned)

    #             print("✅ Datos parseados:", parsed)
    #             # parsed = eval(content)  # 👈 O usar json.loads si el formato es válido
    #             rows.append(parsed)

    #         except Exception as e:
    #             print(f"❌ Error procesando {fname}: {e}")

    # if not rows:
    #     shutil.rmtree(DESTINATION_PATH, ignore_errors=True)
    #     os.remove(temp_zip)
    #     return {"message": "No se pudo procesar ninguna factura."}
    

    # df = pd.DataFrame(rows)
    # df.to_excel(DESTINATION_PATH, index=False)

    # shutil.rmtree(DESTINATION_PATH, ignore_errors=True)
    # os.remove(temp_zip)

    return {"message": "Procesamiento exitoso", "download": "/download"}



@app.get("/download")
def download_excel():
    return FileResponse("output/facturas.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="facturas.xlsx")
