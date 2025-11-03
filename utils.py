import json

# Lee logs desde un archivo
def read_logs(file_path):
    try:
        # Leer el archivo de logs
        with open(file_path, 'r', encoding='utf-8') as f:
            # Leer todo el contenido del archivo y eliminar espacios en blanco innecesarios
            content = f.read().strip()

            # Dividir el contenido en bloques separados por líneas en blanco
            cleaned_blocks =[]
            blocks = content.split('\n\n')
            for block in blocks:
                cleaned_block = block.strip()
                if cleaned_block:
                    cleaned_blocks.append(cleaned_block)
            return cleaned_blocks
        
    # Manejar el error si el archivo no existe
    except FileNotFoundError:
        print(f"ERROR: El archivo '{file_path}' no fue encontrado.")
        return []

# Guarda los resultados en un archivo JSON
def save_results(results, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
