import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from modelo import cargar_datos_json, guardar_datos_json, entrenar_modelo, predecir, guardar_recomendaciones_json

# Colores personalizados para la interfaz
BG_COLOR = "#4A00E0"  # Violeta moderno
SECONDARY_BG_COLOR = "#6A1B9A"  # Púrpura oscuro
BUTTON_COLOR = "#00C853"  # Verde brillante
BUTTON_HOVER_COLOR = "#00B64F"  # Verde claro al hacer hover
BUTTON_RESET_COLOR = "#D32F2F"  # Rojo intenso
LABEL_COLOR = "#FFFFFF"  # Blanco
TEXT_COLOR = "#F5F5F5"  # Gris claro
RESULT_COLOR = "#FFD600"  # Amarillo brillante

# Función para iniciar la interfaz
def iniciar_interfaz():
    # Ruta del archivo JSON
    ruta_json = 'data/dataset.json'
    
    # Cargar datos
    datos = cargar_datos_json(ruta_json)

    # Sección de captura de datos
    def agregar_datos():
        nombre = entry_nombre.get()
        genero = combo_genero.get()
        plataforma = combo_plataforma.get()
        ign = entry_ign.get()
        vandal = entry_vandal.get()
        puntaje = entry_puntaje.get()
        recomendacion = entry_recomendacion.get()

        if not nombre or not genero or not plataforma or not ign or not vandal or not puntaje or not recomendacion:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos.")
            return

        try:
            ign = float(ign)
            vandal = float(vandal)
            puntaje = float(puntaje)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para los puntajes.")
            return

        nuevo_dato = {
            "Nombre": nombre, 
            "Genero": genero, 
            "Plataforma": plataforma, 
            "IGN": ign, 
            "Vandal": vandal, 
            "Puntaje": puntaje, 
            "Recomendacion": recomendacion
        }
        datos.append(nuevo_dato)
        guardar_datos_json(datos, ruta_json)
        messagebox.showinfo("Éxito", "Datos guardados correctamente")

        # Limpiar campos
        entry_nombre.delete(0, tk.END)
        combo_genero.set('')
        combo_plataforma.set('')
        entry_ign.delete(0, tk.END)
        entry_vandal.delete(0, tk.END)
        entry_puntaje.delete(0, tk.END)
        entry_recomendacion.delete(0, tk.END)

    # Limpiar los campos de la interfaz
    def limpiar_campos():
        entry_nombre.delete(0, tk.END)
        combo_genero.set('')
        combo_plataforma.set('')
        entry_ign.delete(0, tk.END)
        entry_vandal.delete(0, tk.END)
        entry_puntaje.delete(0, tk.END)
        entry_recomendacion.delete(0, tk.END)
        entry_recomendacion_puntaje.delete(0, tk.END)
        entry_nombre_usuario.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        label_resultado.config(text="Recomendación:")

    # Sección de recomendación
    def hacer_recomendacion():
        genero = combo_recomendacion_genero.get()
        puntaje = entry_recomendacion_puntaje.get()
        nombre_usuario = entry_nombre_usuario.get()
        correo_usuario = entry_correo.get()
        edad_usuario = entry_edad.get()

        if not genero or not puntaje or not nombre_usuario or not correo_usuario or not edad_usuario:
            messagebox.showerror("Error", "Por favor, ingrese todos los campos.")
            return

        try:
            puntaje = float(puntaje)
            edad_usuario = int(edad_usuario)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")
            return

        recomendados = []
        for dato in datos:
            if dato['Genero'] == genero and dato['Puntaje'] >= puntaje:
                recomendados.append(dato)

        if len(recomendados) < 3:
            recomendacion_texto = "No hay suficientes videojuegos para recomendar."
        else:
            recomendados = recomendados[:3]
            recomendacion_texto = "\n".join([f"{r['Nombre']} ({r['Plataforma']}) - IGN: {r['IGN']} - Vandal: {r['Vandal']} - Recomendación: {r['Recomendacion']}" for r in recomendados])

        # Guardar las recomendaciones en un archivo JSON con los datos del usuario
        ruta_recomendaciones_json = 'data/recomendaciones.json'
        guardar_recomendaciones_json(recomendacion_texto, nombre_usuario, correo_usuario, edad_usuario, ruta_recomendaciones_json)
        
        label_resultado.config(text=f"Recomendación:\n{recomendacion_texto}")

    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Recomendador de Videojuegos")
    ventana.geometry("600x650")
    ventana.config(bg=BG_COLOR)

    # Título
    label_titulo = tk.Label(ventana, text="Recomendador de Videojuegos", font=("Roboto", 22, "bold"), bg=BG_COLOR, fg=LABEL_COLOR)
    label_titulo.pack(pady=20)

    ### Sección de Captura ###
    frame_captura = tk.Frame(ventana, bg=SECONDARY_BG_COLOR, relief="groove", bd=5)
    frame_captura.pack(pady=20, padx=10, fill="both", expand=True)

    # Nombre del videojuego
    tk.Label(frame_captura, text="Nombre del Videojuego:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_nombre = tk.Entry(frame_captura, width=40, font=("Roboto", 12), relief="flat", bd=2, highlightbackground="black", highlightthickness=1)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    # Género
    tk.Label(frame_captura, text="Género del Videojuego:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    combo_genero = ttk.Combobox(frame_captura, values=[ 
        "Acción", "Aventura", "Deportes", "Estrategia", "RPG", "Shooter", "Simulación", "Carreras", "Lucha", "Aventura Gráfica",
        "Puzzle", "Horror", "Plataforma", "Mundo Abierto", "Battle Royale", "MOBA", "Otros"], width=37, font=("Roboto", 12))
    combo_genero.grid(row=1, column=1, padx=10, pady=5)

    # Plataforma
    tk.Label(frame_captura, text="Plataforma:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    combo_plataforma = ttk.Combobox(frame_captura, values=[
        "XBOX SERIES S/X", "Playstation 5", "Nintendo Switch", "PC", "Smartphone"], width=37, font=("Roboto", 12))
    combo_plataforma.grid(row=2, column=1, padx=10, pady=5)

    # Puntaje IGN
    tk.Label(frame_captura, text="Puntaje IGN:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_ign = tk.Entry(frame_captura, width=40, font=("Roboto", 12))
    entry_ign.grid(row=3, column=1, padx=10, pady=5)

    # Puntaje Vandal
    tk.Label(frame_captura, text="Puntaje Vandal:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_vandal = tk.Entry(frame_captura, width=40, font=("Roboto", 12))
    entry_vandal.grid(row=4, column=1, padx=10, pady=5)

    # Puntaje personal
    tk.Label(frame_captura, text="Tu Puntaje:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_puntaje = tk.Entry(frame_captura, width=40, font=("Roboto", 12))
    entry_puntaje.grid(row=5, column=1, padx=10, pady=5)

    # Recomendación personal
    tk.Label(frame_captura, text="Recomendación personal:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entry_recomendacion = tk.Entry(frame_captura, width=40, font=("Roboto", 12))
    entry_recomendacion.grid(row=6, column=1, padx=10, pady=5)

    # Botón para agregar datos
    button_agregar = tk.Button(frame_captura, text="Agregar Videojuego", command=agregar_datos, bg=BUTTON_COLOR, fg="white", font=("Roboto", 12), relief="flat")
    button_agregar.grid(row=7, column=0, columnspan=2, pady=10)

    # Botón para limpiar campos
    button_limpiar = tk.Button(frame_captura, text="Limpiar Campos", command=limpiar_campos, bg=BUTTON_RESET_COLOR, fg="white", font=("Roboto", 12), relief="flat")
    button_limpiar.grid(row=8, column=0, columnspan=2, pady=10)

    ### Sección de Recomendación ###
    frame_recomendacion = tk.Frame(ventana, bg=SECONDARY_BG_COLOR, relief="groove", bd=5)
    frame_recomendacion.pack(pady=20, padx=10, fill="both", expand=True)

    # Género para recomendación
    tk.Label(frame_recomendacion, text="Género para Recomendación:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    combo_recomendacion_genero = ttk.Combobox(frame_recomendacion, values=[
        "Acción", "Aventura", "Deportes", "Estrategia", "RPG", "Shooter", "Simulación", "Carreras", "Lucha", "Aventura Gráfica",
        "Puzzle", "Horror", "Plataforma", "Mundo Abierto", "Battle Royale", "MOBA", "Otros"], width=37, font=("Roboto", 12))
    combo_recomendacion_genero.grid(row=0, column=1, padx=10, pady=5)

    # Puntaje para recomendación
    tk.Label(frame_recomendacion, text="Puntaje mínimo:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_recomendacion_puntaje = tk.Entry(frame_recomendacion, width=40, font=("Roboto", 12))
    entry_recomendacion_puntaje.grid(row=1, column=1, padx=10, pady=5)

    # Nombre de usuario
    tk.Label(frame_recomendacion, text="Nombre del Usuario:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_nombre_usuario = tk.Entry(frame_recomendacion, width=40, font=("Roboto", 12))
    entry_nombre_usuario.grid(row=2, column=1, padx=10, pady=5)

    # Correo del usuario
    tk.Label(frame_recomendacion, text="Correo del Usuario:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_correo = tk.Entry(frame_recomendacion, width=40, font=("Roboto", 12))
    entry_correo.grid(row=3, column=1, padx=10, pady=5)

    # Edad del usuario
    tk.Label(frame_recomendacion, text="Edad del Usuario:", bg=SECONDARY_BG_COLOR, fg=TEXT_COLOR, font=("Roboto", 10)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_edad = tk.Entry(frame_recomendacion, width=40, font=("Roboto", 12))
    entry_edad.grid(row=4, column=1, padx=10, pady=5)

    # Botón para hacer la recomendación
    button_recomendacion = tk.Button(frame_recomendacion, text="Obtener Recomendación", command=hacer_recomendacion, bg=BUTTON_COLOR, fg="white", font=("Roboto", 12), relief="flat")
    button_recomendacion.grid(row=5, column=0, columnspan=2, pady=10)

    # Resultado de recomendación
    label_resultado = tk.Label(ventana, text="Recomendación:", bg=BG_COLOR, fg=RESULT_COLOR, font=("Roboto", 12, "bold"))
    label_resultado.pack(pady=10)

    # Ejecutar la interfaz
    ventana.mainloop()
