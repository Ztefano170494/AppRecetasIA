import os
import streamlit as st
from google import genai
from google.genai import types

# Agregamos la clave aquí de forma explícita:
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6JlmZJOOhl-IiWyhAK45emDitj4d1vKOnDIYSjlM08FRw"

# Configuración de la IA (Para producción usar variables de entorno)
try:
    client = genai.Client()
except Exception:
    client = None

# Configuración estética de la página para que parezca una App Móvil
st.set_page_config(
    page_title="ChefIA - Recetas Inteligentes", 
    page_icon="🍳", 
    layout="centered"
)

# Estilos CSS para forzar una estética minimalista y limpia
st.markdown("""
    <style>
    .main .block-container { max-width: 450px; padding-top: 2rem; }
    h1 { color: #2e7d32; text-align: center; font-size: 2.2rem !important; }
    .subtitle { text-align: center; color: #546e7a; font-size: 1.1rem; margin-bottom: 2rem; }
    stButton>button { width: 100%; background-color: #2e7d32 !important; color: white !important; border-radius: 10px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# Encabezado de la App
st.markdown("<h1>ChefIA 🍳</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>¿Qué tenés en la heladera hoy?</p>", unsafe_allow_html=True)

# Input del Usuario
ingredientes = st.text_area(
    label="Ingredientes disponibles (separados por comas):",
    placeholder="Ej: tomate, huevos, arroz, queso devoto",
    height=100
)

# Botón de acción
if st.button("Generar Receta Mágica ✨"):
    if not ingredientes.strip():
        st.error("Por favor, ingresá al menos un ingrediente para continuar.")
    else:
        with st.spinner("Pensando tu receta ideal con IA..."):
            
            prompt_sistema = (
                "Sos un chef experto de Buenos Aires, Argentina. Tu tarea es crear recetas viables y coherentes "
                "basadas ESTRICTAMENTE en los ingredientes proporcionados por el usuario. Si los ingredientes "
                "son totalmente incompatibles, peligrosos o atípicos al punto de no ser comestibles, "
                "explicalo amablemente con humor porteño y sugerí una alternativa lógica. "
                "Formatea la respuesta usando Markdown con encabezados claros: Nombre de la receta, Tiempo estimado, Ingredientes y Paso a Paso."
            )
            
            prompt_usuario = f"Ingredientes disponibles: {ingredientes}"
            
            try:
                if client:
                    try:
                        # 1. Intento principal con el modelo más nuevo del mercado
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=prompt_usuario,
                            config=types.GenerateContentConfig(
                                system_instruction=prompt_sistema,
                                temperature=0.7
                            )
                        )
                    except Exception as e:
                        # 2. Respaldo inteligente si el servidor 3.8 está saturado o da error
                        st.warning("⚠️ El servidor principal está experimentando alta demanda. Conectando al nodo de respaldo (Gemini 3.5)...")
                        response = client.models.generate_content(
                            model='gemini-3.5-flash',
                            contents=prompt_usuario,
                            config=types.GenerateContentConfig(
                                system_instruction=prompt_sistema,
                                temperature=0.7
                            )
                        )
                            
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.markdown("---")
                    st.markdown("### 🛠️ Modo simulación activado (Sin API Key)")
                    st.info(f"Ingredientes recibidos por el equipo de QA: *{ingredientes}*")
            
            except Exception as error:
                st.error(f"Ambos servidores de IA están saturados temporalmente. Por favor, reintentá en unos segundos. Detalles: {str(error)}")
