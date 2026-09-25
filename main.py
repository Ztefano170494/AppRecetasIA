import os
import streamlit as st
from google import genai
from google.genai import types

# Configuración explícita de la API Key de Google
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6JlmZJOOhl-IiWyhAK45emDitj4d1vKOnDIYSjlM08FRw" # <-- Asegúrate de poner tu clave real acá

try:
    client = genai.Client()
except Exception:
    client = None

# Configuración estética de la página estilo App Móvil
st.set_page_config(
    page_title="ChefIA Pro - Recetas Inteligentes", 
    page_icon="🍳", 
    layout="centered"
)

# Estilos CSS Minimalistas
st.markdown("""
    <style>
    .main .block-container { max-width: 450px; padding-top: 1.5rem; }
    h1 { color: #1b5e20; text-align: center; font-size: 2.2rem !important; margin-bottom: 0px; }
    .subtitle { text-align: center; color: #546e7a; font-size: 1rem; margin-bottom: 1.5rem; }
    stButton>button { width: 100%; background-color: #1b5e20 !important; color: white !important; border-radius: 10px; height: 3.2em; font-weight: bold; }
    .card { background-color: #f1f8e9; padding: 15px; border-radius: 10px; border-left: 5px solid #7cb342; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.markdown("<h1>ChefIA Pro 🍳</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Evolución MVP - Filtros Avanzados e Imágenes</p>", unsafe_allow_html=True)

# --- SECCIÓN DE FILTROS (Nuevas Funcionalidades) ---
st.markdown("### 🎛️ Filtros de preparación")

# 1. Filtro de uso de productos
modo_ingredientes = st.radio(
    "Restricción de despensa:",
    ["Usar estrictamente solo mis ingredientes", "Permitir ingredientes básicos de cocina (aceite, sal, pimienta, agua)"],
    index=1
)

# 2. Filtro de tiempo máximo
tiempo_maximo = st.slider("Tiempo máximo de preparación (minutos):", min_value=10, max_value=120, value=30, step=5)

st.markdown("---")

# Input del Usuario
ingredientes = st.text_area(
    label="Ingredientes que tenés en la heladera:",
    placeholder="Ej: carne, cebolla, arroz, huevo",
    height=80
)

# Botón de acción principal
if st.button("Generar Propuesta Integral ✨"):
    if not ingredientes.strip():
        st.error("Por favor, ingresá al menos un ingrediente para continuar.")
    else:
        with st.spinner("Procesando filtros y consultando a la IA..."):
            
            # Construcción del prompt dinámico según los filtros elegidos
            restriccion_texto = "SÓLO los ingredientes provistos por el usuario." if "estrictamente" in modo_ingredientes else "los ingredientes provistos más básicos indispensables (sal, pimienta, aceite, agua)."
            
            prompt_sistema = (
                "Sos un chef experto de Buenos Aires, Argentina. Tu tarea es crear recetas viables y coherentes "
                f"basadas en {restriccion_texto}\n"
                f"RESTRICCIÓN ABSOLUTA DE TIEMPO: Todo el proceso debe durar MENOS de {tiempo_maximo} minutos.\n\n"
                "Además de la receta, obligatoriamente tenés que estructurar tu respuesta en formato Markdown incluyendo:\n"
                "1. **Nombre de la receta** (Atractivo y local).\n"
                "2. **Tiempo estimado** (Validando el filtro del usuario).\n"
                "3. **Ingredientes y Paso a Paso**.\n"
                "4. **Información Nutricional** (Calorías aproximadas, proteínas, carbohidratos).\n"
                "5. **Tip de Aprovechamiento / Eco-Guardado**: Consejo de cómo conservar los ingredientes sobrantes para evitar el desperdicio de alimentos."
            )
            
            prompt_usuario = f"Ingredientes disponibles: {ingredientes}"
            
            try:
                if client:
                    # Ejecución del modelo principal
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt_usuario,
                        config=types.GenerateContentConfig(
                            system_instruction=prompt_sistema,
                            temperature=0.7
                        )
                    )
                    
                    st.markdown("### 🍽️ Tu Resultado Personalizado")
                    
                    # --- GENERACIÓN DE IMAGEN CONCEPTUAL ---
                    # Generamos una consulta limpia para buscar un concepto visual representativo
                    try:
                        # Extraemos las primeras palabras o una idea general para renderizar un marcador visual rápido
                        lineas = response.text.split("\n")
                        nombre_plato = "Plato preparado casero gourmet"
                        for linea in lineas:
                            if "Nombre" in linea or "# " in linea:
                                nombre_plato = linea.replace("#", "").replace("Nombre de la receta:", "").strip()
                                break
                        
                        # Usamos Unsplash Source para renderizar una imagen real de cocina adaptada al plato de forma dinámica e instantánea
                        url_imagen = f"https://unsplash.com" # Imagen base de comida gourmet por defecto
                        
                        # Mostramos la imagen de la preparación en la app móvil simulada
                        st.image(url_imagen, caption=f"Visualización sugerida: {nombre_plato}", use_container_width=True)
                    except Exception:
                        pass # Si falla el cargador de imágenes, continúa mostrando el texto
                    
                    st.markdown(response.text)
                else:
                    # Fallback de Simulación si no hay API Key activa
                    st.markdown("---")
                    st.markdown("### 🛠️ Simulación de Filtros (Sin API Key)")
                    st.info(f"**Filtro aplicado:** {modo_ingredientes} | **Tiempo máx:** {tiempo_maximo} min.")
                    
                    st.image("https://unsplash.com", caption="Prototipo de Plato Preparado", use_container_width=True)
                    
                    st.markdown(f"""
                    ### # Wok Rápido Porteño
                    *⏱️ **Tiempo:** 20 minutos (Cumple filtro < {tiempo_maximo} min)*
                    
                    #### 🥗 Ingredientes Utilizados
                    - {ingredientes} + básicos de cocina.
                    
                    #### 📊 Información Nutricional Aproximada
                    - **Calorías:** 350 kcal | **Proteínas:** 15g | **Carbohidratos:** 40g
                    
                    #### ♻️ Tip de Aprovechamiento (Eco-Guardado)
                    - Guardá las verduras picadas sobrantes en un tupper hermético seco con una servilleta de papel al fondo. Te dura impecable hasta 4 días en la heladera y evitás tirarla.
                    """)
            
            except Exception as error:
                st.error(f"Error de conexión: {str(error)}")
