# src/ejecutar.py
import json
import os
from modelo import guardar_a_csv

# Ruta del archivo JSON (relativa desde 'src' a 'data')
ruta_json = '../data/recomendaciones.json'

# Cargar el contenido del archivo JSON
with open(ruta_json, 'r') as file:
    datos_json = json.load(file)

# Crear la carpeta "transformaciones" si no existe (relativa al directorio raíz)
carpeta_transformaciones = '../transformaciones'
os.makedirs(carpeta_transformaciones, exist_ok=True)

# Ruta del archivo CSV donde deseas guardar los datos dentro de "transformaciones"
ruta_csv = os.path.join(carpeta_transformaciones, 'recomendaciones.csv')

# Llamar a la función para guardar los datos en un archivo CSV
guardar_a_csv(datos_json, ruta_csv)

print(f"Datos guardados correctamente en {ruta_csv}")
