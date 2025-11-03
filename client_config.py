import os
from google import genai
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

def get_gemini_client():

    api_key = os.environ.get("GOOGLE_API_KEY")

    mensaje_error = """GOOGLE_API_KEY no configurada\n"
                    "Configúrala usando uno de los siguientes métodos:\n"
                    "1. setx GOOGLE_API_KEY TU_API_KEY_AQUI\n"
                    "2. $env:GOOGLE_API_KEY=TU_API_KEY_AQUI\n"
                    "3. Archivo .env con GOOGLE_API_KEY=TU_API_KEY_AQUI\n"""

    if not api_key:
        raise ValueError(mensaje_error)

    return genai.Client(api_key=api_key)