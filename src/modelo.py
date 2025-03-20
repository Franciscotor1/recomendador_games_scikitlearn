import pandas as pd
import json
import os
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from datetime import datetime
import pytz

# Guardar datos en formato CSV
def guardar_a_csv(datos, ruta_csv):
    df = pd.DataFrame(datos)
    df.to_csv(ruta_csv, index=False)

# Cargar datos desde JSON
def cargar_datos_json(ruta_json):
    try:
        with open(ruta_json, 'r') as f:
            datos = json.load(f)
        return datos
    except FileNotFoundError:
        return []

# Guardar datos en formato JSON
def guardar_datos_json(datos, ruta_json):
    with open(ruta_json, 'w') as f:
        json.dump(datos, f, indent=4)

# Función para obtener la fecha y hora en Mazatlán
def obtener_fecha_hora():
    tz = pytz.timezone('America/Mazatlan')
    ahora = datetime.now(tz)
    return ahora.strftime('%Y-%m-%d %H:%M:%S')

# Función para guardar las recomendaciones en un archivo JSON
def guardar_recomendaciones_json(recomendacion, nombre, correo, edad, ruta_json):
    # Verificar si el archivo de recomendaciones ya existe
    if os.path.exists(ruta_json):
        with open(ruta_json, 'r') as f:
            recomendaciones = json.load(f)
    else:
        recomendaciones = []

    # Agregar fecha y hora
    fecha_hora = obtener_fecha_hora()

    # Crear el diccionario con los nuevos campos
    recomendacion_usuario = {
        "Nombre": nombre,
        "Correo": correo,
        "Edad": edad,
        "Fecha_Hora": fecha_hora,
        "Recomendacion": recomendacion
    }

    recomendaciones.append(recomendacion_usuario)

    # Guardar las recomendaciones en el archivo JSON
    with open(ruta_json, 'w') as f:
        json.dump(recomendaciones, f, indent=4)

# Entrenamiento del modelo de Machine Learning
def entrenar_modelo(datos):
    # Extraer las características y etiquetas
    X = np.array([ [d['IGN'], d['Vandal'], d['Puntaje']] for d in datos ])  # Usamos IGN, Vandal y Puntaje
    y = np.array([ d['Genero'] for d in datos ])  # Predecir el género
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X, y)
    return modelo

# Hacer una predicción de acuerdo a los puntajes
def predecir(modelo, ign, vandal, puntaje):
    return modelo.predict([[ign, vandal, puntaje]])[0]
