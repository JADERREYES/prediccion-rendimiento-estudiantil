import streamlit as st
import pandas as pd
import time
import numpy as np
from src.encriptacion import detector

# Configuración futurista
st.set_page_config(
    page_title="NEURAL CRYPT ANALYZER",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para efecto futurista
# CSS personalizado para efecto futurista
st.markdown("""
<style>

/* Fondo con efecto matrix */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #1a1f2e 100%);
}

/* TITULOS FUTURISTAS SIN BLUR */
h1, h2, h3 {
    color: #00ff9d;
    font-weight: 700 !important;
    text-shadow: 0 0 6px rgba(0,255,157,0.6);
}

/* Tarjetas con efecto cristal (blur reducido) */
.css-1r6slb0, .css-12oz5g7 {
    background: rgba(20, 30, 50, 0.8) !important;
    backdrop-filter: blur(3px);
    border: 1px solid rgba(0, 255, 157, 0.3);
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0, 184, 255, 0.2);
}

/* Botones con efecto neón */
.stButton > button {
    background: linear-gradient(90deg, #00ff9d, #00b8ff);
    color: #0a0f1e;
    border: none;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px rgba(0, 255, 157, 0.5);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(0, 255, 157, 0.8);
}

/* Inputs con efecto cyber */
.stTextArea textarea {
    background: rgba(10, 20, 30, 0.9) !important;
    border: 1px solid #00ff9d !important;
    color: #00ff9d !important;
    font-family: 'Courier New', monospace;
    font-size: 16px;
    box-shadow: 0 0 6px rgba(0, 255, 157, 0.3);
}

/* Código estilo terminal */
.stCodeBlock {
    background: #0a0f1e !important;
    border: 1px solid #00b8ff;
    border-radius: 10px;
}

/* Métricas futuristas */
.css-1xarl3l {
    background: linear-gradient(
        135deg,
        rgba(0, 255, 157, 0.1),
        rgba(0, 184, 255, 0.1)
    );
    border: 1px solid #00ff9d;
    border-radius: 10px;
    padding: 15px;
}

/* Animación de carga */
@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

.loading {
    animation: pulse 1.5s infinite;
    color: #00ff9d;
    font-family: 'Courier New', monospace;
}

/* Línea de tiempo futurista */
.timeline {
    border-left: 2px solid #00ff9d;
    padding-left: 20px;
    margin-left: 10px;
}

/* Efecto glitch para resultados */
@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

.glitch-text {
    animation: glitch 0.3s infinite;
}

</style>
""", unsafe_allow_html=True)

# Input con diseño futurista
texto_ingresado = st.text_area(
    "📡 INGRESE TEXTO CIFRADO:",
    height=100,
    placeholder="Ej: aG9sYQ==  |  Uryyb Jbeyq  |  khoor  |  1a2b3c  |  hola",
    key="input_text"
)

# Botón con efecto
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analizar_btn = st.button("🔮 INICIAR ANÁLISIS NEURONAL", use_container_width=True)

# Resultados
if analizar_btn and texto_ingresado:
    texto_limpio = texto_ingresado.strip()
    
    with st.spinner("⚡ PROCESANDO CON RED NEURONAL..."):
        time.sleep(1.5)
        resultado = detector.procesar(texto_limpio)
    
    # Timeline de análisis
    st.markdown("---")
    st.markdown("### 📊 MATRIZ DE RESULTADOS")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown("""
        <div style='background: rgba(0,255,157,0.05); padding: 20px; border-radius: 15px;'>
            <p style='color: #00ff9d; font-size: 0.9em;'>📥 INPUT</p>
            <p style='color: white; font-family: monospace; font-size: 1.2em;'>{}</p>
        </div>
        """.format(resultado['texto_original']), unsafe_allow_html=True)
    
    with col_res2:
        algoritmo_color = {
            "Base64": "#00ff9d",
            "ROT13": "#00b8ff",
            "César": "#ff00ff",
            "XOR": "#ffaa00",
            "Plano": "#ffffff"
        }
        color = next((v for k, v in algoritmo_color.items() if k in resultado['algoritmo']), "#00ff9d")
        
        st.markdown(f"""
        <div style='background: rgba(0,255,157,0.05); padding: 20px; border-radius: 15px;'>
            <p style='color: {color}; font-size: 0.9em;'>🔍 ALGORITMO DETECTADO</p>
            <p style='color: white; font-size: 1.5em; font-weight: bold;'>{resultado['algoritmo']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_res3:
        st.markdown("""
        <div style='background: rgba(0,255,157,0.05); padding: 20px; border-radius: 15px;'>
            <p style='color: #00ff9d; font-size: 0.9em;'>📤 OUTPUT</p>
            <p style='color: white; font-family: monospace; font-size: 1.2em;'>{}</p>
        </div>
        """.format(resultado['texto_descifrado']), unsafe_allow_html=True)
    
    # Resultado destacado
    st.markdown("---")
    st.markdown("### 🔓 TEXTO DESCIFRADO")
    
    if "Error" in resultado["texto_descifrado"] or "no se puede" in resultado["texto_descifrado"].lower():
        st.error(f"### ❌ {resultado['texto_descifrado']}")
    else:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #00ff9d20, #00b8ff20); 
                    padding: 30px; border-radius: 20px; 
                    border: 2px solid #00ff9d; text-align: center;'>
            <h1 style='color: white; font-size: 3em; text-shadow: 0 0 20px #00ff9d;'>
                {resultado['texto_descifrado']}
            </h1>
            <p style='color: #00b8ff;'>Decodificado con {resultado['algoritmo']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Información técnica
    with st.expander("🔬 VER ANÁLISIS TÉCNICO"):
        st.markdown("""
        <div style='background: #0a0f1e; padding: 20px; border-radius: 10px;'>
            <p style='color: #00ff9d;'>📊 CARACTERÍSTICAS EXTRAÍDAS:</p>
        """, unsafe_allow_html=True)
        
        # Mostrar características
        chars = detector.extraer_caracteristicas(texto_limpio).flatten()
        chars_names = [
            "Longitud", "Mayúsculas", "Minúsculas", "Dígitos", "Espacios",
            "Especiales", "Hex chars", "Base64 chars", "Entropía", "Padding",
            "Chars únicos", "Tiene +", "Tiene /", "Termina en =", 
            "Solo números", "Solo binario", "Todo mayúsculas"
        ]
        
        df_chars = pd.DataFrame({
            "Característica": chars_names,
            "Valor": chars
        })
        st.dataframe(df_chars, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

elif analizar_btn and not texto_ingresado:
    st.error("❌ ERROR: INGRESE UN TEXTO PARA ANALIZAR")

# Footer futurista
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='color: #00b8ff; font-size: 0.8em; letter-spacing: 2px;'>
        ⚡ NEURAL CRYPT ANALYZER v2.0 ⚡
    </p>
    <p style='color: #00ff9d; font-size: 0.7em;'>
        [ Base64 · ROT13 · César · XOR · Texto Plano ]
    </p>
    <p style='color: #444; font-size: 0.6em;'>
        Red Neuronal · 19 Características · 2000 Muestras
    </p>
</div>
""", unsafe_allow_html=True)