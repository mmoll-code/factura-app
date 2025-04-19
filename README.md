# 🧾 Procesador de Facturas - OCR + OpenAI + Excel

Proyecto fullstack para procesar facturas en imágenes, interpretar sus contenidos con inteligencia artificial y exportarlos a una hoja de cálculo.

---

## 🧱 Tecnologías

- ⚙️ **Backend:** Python + FastAPI + Tesseract OCR + OpenAI + Pandas
- 🌐 **Frontend:** Angular (standalone components + `provideHttpClient()` moderno)
- 📦 **Output:** Excel `.xlsx` con datos estructurados (proveedor, fecha, total, etc.)

---

## 🚀 Requisitos

### 📦 Backend

- Python 3.9+
- `tesseract-ocr` instalado (usa Homebrew)
- Clave de API de OpenAI

### 🌐 Frontend

- Node.js 18+ y Angular CLI

---

## 🔧 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/facturas-app.git
cd facturas-app
```

### 2. ⚙️ Backend (FastAPI)

```bash
cd backend
./setup.sh
source venv/bin/activate
uvicorn main:app --reload
```

### 3. 🌐 Frontend (Angular)

```bash
cd frontend
npm install
ng serve
```
📍 Aplicación disponible en: http://localhost:4200


🧪 Uso

    Subí un archivo .zip con imágenes de facturas en la landing principal.

    El backend procesará las imágenes:

        Extraerá texto con OCR

        Interpretará los datos con OpenAI

        Guardará un Excel con los resultados

    El frontend te mostrará un botón para descargar el archivo generado.


📁 Estructura del Proyecto
facturas-app/
├── backend/          # Código FastAPI
│   ├── main.py
│   ├── setup.sh
│   └── requirements.txt
├── frontend/         # App Angular
│   └── src/app/pages/main-page
├── README.md


🔐 Seguridad

    No compartas tu API key de OpenAI en público.

    Se recomienda agregar variables de entorno en producción.


✅ Próximos pasos (opcional)

    Validar formato de facturas

    Añadir autenticación básica

    Agregar campos personalizados

    Subida a la nube (Render, Vercel, Railway)


🧑‍💻 Autor

Desarrollado por Martín, con ❤️ y ayuda de ChatGPT.

------------------------------------------------
PARA CORRER EL BACKEND: parado en `./backend` -> `uvicorn main:app --reload`
