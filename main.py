from client_config import get_gemini_client
from utils import read_logs, save_results
from google.genai import types

# Configuraciones
MODEL = "gemini-2.5-flash"
LOGS_FILE = "data/logs.txt"
OUTPUT_FILE = "data/output.json"



# Definir prompt para análisis de logs
prompt = """Eres un analista de logs experto. 
Tu tarea es analizar un bloque de log y generar un conjunto de etiquetas temáticas en inglés que clasifiquen cada operación realizada. 
1. Tipo de evento (INFO, ERROR, USER INPUT, SQL, etc.)
2. Acción realizada (consulta, actualización, eliminación, inicialización, etc.)
3. Resultado de la acción (exitosa, fallida, etc.)

Reglas estrictas:
1. Solo devuelve las etiquetas como lista separada por comas.
2. No agregues explicaciones ni texto adicional.
3. Cada etiqueta debe ser concisa y representar: tipo de evento, acción y resultado.
4. Usa inglés consistente y uniforme, sin símbolos innecesarios.
5. Si un bloque no tiene eventos, devuelve "SIN_ETIQUETAS".

Ejemplo:
Log: [INFO] Agente iniciado. [USER INPUT] Solicitud de datos. [SQL] SELECT * FROM cursos;
Etiquetas: Inicialización Agente, Solicitud Usuario, Consulta SQL

Ahora analiza este bloque de log: """

def analyze_log(client, log_text: str) -> list:

    response = client.models.generate_content(
        model=MODEL,
        contents=f"{prompt}{log_text}",
        config=types.GenerateContentConfig(
            temperature=0.1,              
            max_output_tokens=100,          
            thinking_config=types.ThinkingConfig(thinking_budget=1)  
        )
    )
    etiquetas = [tag.strip() for tag in response.text.split(",")]
    return etiquetas



def main():

    # Inicializar cliente
    client = get_gemini_client()

    # Leer logs
    logs = read_logs(LOGS_FILE)

    if not logs:
        print("No se encontraron logs para analizar.")
        return

    results = []
    for i, log_text in enumerate(logs, start=1):
        etiquetas = analyze_log(client, log_text)
        results.append({
            "log_id": i,
            "texto": log_text,
            "etiquetas": etiquetas
        })

    #Guardar resultados
    save_results(results, OUTPUT_FILE)
    print(f"Resultados guardados en {OUTPUT_FILE}")

if __name__ == "__main__":
    main()







