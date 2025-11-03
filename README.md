# LOG ANALYZER
Herramienta desarrollada en Python que utiliza el modelo **Gemini** de Google para analizar bloques de logs y generar etiquetas temáticas automáticamente según las operaciones detectadas.

## Requisitos

- Python **3.9+**
- Conexión a Internet
- Clave de API de Gemini

## Instalación de dependencias

Recomendado entornos virtuales:

Windows
```
# Crear el entorno virtual
python -m venv venv

# Activar
venv\Scripts\activate
```

Linux/macOS
```macos
# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate  
```


### Antes de ejecutar el proyecto debes instalar las librerías necesarias.

Puedes hacerlo de dos formas:

Opción A — Instalar solo la librería de Gemini

```
pip install -q -U google-genai
pip install python-dotenv  
```

Opción B — Instalar todas las dependencias del proyecto que se encuentran en:

```
pip install -r requirements.txt
```


## 🔐 Configurar la API Key de Google Gemini

Para que el proyecto pueda conectarse al modelo **Gemini**, necesitas obtener una **API Key** desde Google AI Studio.

### Obtener una API Key de Gemini

1. Entra a: https://aistudio.google.com
2. Inicia sesión con tu cuenta de Google
3. Ve a:  
   **Dashboard → API Keys → Create API Key**
4. Copia la clave generada (algo como: `AIzaSyBxxxxxxx...`)

⚠️ **Importante:** No compartir tu API Key en repositorios públicos.


### Configurar API KEY 

Puedes configurarla en tu sistema de tres formas distintas:

---

Opción A — Variable de entorno permanente (Windows)

Persiste después de reiniciar el equipo.

Ejecutar en **PowerShell**:

```powershell
setx GOOGLE_API_KEY "TU_API_KEY_AQUI" 
```

Reiniciar Terminal


Opción B — Variable de entorno temporal (solo sesión actual)

```powershell
$env:GOOGLE_API_KEY="TU_API_KEY_AQUI"
```

Opción C — Usando archivo .env 

Instala dependencia:

```
pip install python-dotenv
```

Crea archivo .env en la raíz del proyecto:

```ini
GOOGLE_API_KEY="TU_API_KEY_AQUI"
```

El proyecto ya lo carga automáticamente



## 📂 Estructura del proyecto

```plaintext
log-analyzer/
│
├─ data/
│   ├─ logs.txt  # Archivo de entrada con logs a analizar
│   └─ output.json  # Archivo generado con los resultados
│
├─ main.py  # Script principal que ejecuta el análisis
├─ client_config.py  # Configuración de cliente Gemini
├─ utils.py   # Funciones auxiliares: leer y guardar datos
│ 
│
├─ .env # API Key (NO EXPONER)
├─ requirements.txt  # Dependencias del proyecto
└─ README.md  # Documentación del proyecto
```
## Cómo funciona el código y decisiones técnicas

El proyecto analiza bloques de logs para generar etiquetas temáticas usando el modelo "gemini-2.5-flash" de Google.

### Flujo general del script (main.py):

- Inicializa el cliente Gemini usando la API Key (get_gemini_client()).

- Lee los logs desde data/logs.txt con la función read_logs().

- Procesa cada bloque de log usando analyze_log(), que envía el texto al modelo Gemini.

- Genera etiquetas según las operaciones detectadas (INFO, ERROR, SQL, USER INPUT, etc.).

- Guarda los resultados en data/output.json con save_results().

### Decisiones técnicas relevantes:

Se construyó un prompt para que Gemini devuelva solo etiquetas concisas, separadas por comas, sin explicaciones adicionales, garantizando consistencia este se encuentra en el archivo main.py en la variable prompt.

Configuración del modelo:

- temperature=0.1 → Baja aleatoriedad, resultados más consistentes.

- max_output_tokens=100 → Limita la longitud de la respuesta para evitar saturación de datos.

- thinking_config=ThinkingConfig(thinking_budget=1) → Define el "presupuesto de pensamiento" del modelo.

- Funciones reutilizables: read_logs() y save_results() separan la lógica de lectura/escritura de archivos del procesamiento de logs, facilitando mantenimiento y pruebas.

- Seguridad de la API Key: uso de .env o variables de entorno para no exponer la clave en el código.

⚡Estas configuraciones están pensadas para mejorar el tiempo de respuesta y obtener respuestas correctas de forma rápida. Sin embargo, pueden ajustarse para obtener resultados más creativos, detallados o largos según la necesidad del proyecto.

## Diagrama o flujo de proyecto
```
Logs.txt --> main.py --> Gemini --> etiquetas --> output.json
```

## Ejecución del proyecto

Una vez activado el entorno virtual y configurada tu API Key:

Ejecutar el comando python + ruta donde se encuentra el archivo main.py del proyecto

``` 
python ..(Completar ruta)../main.py
```

Si todo está configurado correctamente, verás un mensaje como:

``` 
Resultados guardados en data/output.json
```

Los cuales se guardarán en el directorio data/ dentro del proyecto.

## Ejemplo de resultados
```json
[
  {
    "log_id": 1,
    "texto": "[2025-10-20 09:13:42] [INFO] Agent DBConnector initialized. Awaiting query request.\n[2025-10-20 09:13:45] [USER INPUT] \"Muéstrame los cursos disponibles de Power BI con certificación.\"\n[2025-10-20 09:13:45] [DEBUG] Building SQL query...\n[2025-10-20 09:13:46] [SQL] SELECT nombre, certificacion, disponible FROM cursos WHERE tecnologia_id = 'Power BI';\n[2025-10-20 09:13:47] [INFO] Query executed successfully. 12 records retrieved.\n[2025-10-20 09:13:48] [LLM RESPONSE] “Encontré 12 cursos disponibles con certificación Power BI.”",
    "etiquetas": [
      "INFO Agent Initialization Success",
      "USER INPUT Query Request",
      "DEBUG SQL Query Building",
      "SQL Query Execution",
      "INFO Query Execution Success",
      "LLM RESPONSE Data Retrieval"
    ]
  },
  {
    "log_id": 2,
    "texto": "[2025-10-20 10:02:11] [INFO] Agent DBConnector received new query request.\n[2025-10-20 10:02:12] [USER INPUT] \"Actualiza el estatus del curso 143 a inactivo.\"\n[2025-10-20 10:02:12] [DEBUG] Preparing SQL update...\n[2025-10-20 10:02:13] [SQL] UPDATE cursos SET estatus_curso = 'Inactivo' WHERE id = 143;\n[2025-10-20 10:02:14] [ERROR] SQLExecutionError: Cannot update record — permission denied.\n[2025-10-20 10:02:15] [LLM RESPONSE] “Parece que no tengo permisos para modificar ese curso.”",
    "etiquetas": [
      "INFO Agent Query Request Received",
      "USER INPUT Course Status Update Request",
      "DEBUG SQL Update Preparation",
      "SQL Course Status Update",
      "ERROR SQL Update Failed Permission Denied",
      "LLM RESPONSE Permission Denied"
    ]
  },
  {
    "log_id": 3,
    "texto": "[2025-10-20 10:45:03] [INFO] Agent received task to retrieve latest session info.\n[2025-10-20 10:45:04] [SQL] SELECT * FROM sesiones ORDER BY fecha_inicio DESC LIMIT 5;\n[2025-10-20 10:45:05] [INFO] Query returned 5 results.\n[2025-10-20 10:45:05] [LLM RESPONSE] “Aquí tienes las 5 sesiones más recientes.”",
    "etiquetas": [
      "INFO Agent Task Reception",
      "SQL Query Execution",
      "INFO Query Result",
      "LLM Response Generation"
    ]
  }
]
```


