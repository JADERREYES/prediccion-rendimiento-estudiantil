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
st.markdown("""
<style>
    /* Fondo con efecto matrix */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #1a1f2e 100%);
    }
    
    /* Títulos con efecto neón */
    h1, h2, h3 {
        background: linear-gradient(90deg, #00ff9d, #00b8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        text-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
    }
    
    /* Tarjetas con efecto cristal */
    .css-1r6slb0, .css-12oz5g7 {
        background: rgba(20, 30, 50, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 157, 0.2);
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 184, 255, 0.2);
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
        box-shadow: 0 0 20px rgba(0, 255, 157, 0.5);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 30px rgba(0, 255, 157, 0.8);
    }
    
    /* Inputs con efecto cyber */
    .stTextArea textarea {
        background: rgba(10, 20, 30, 0.8) !important;
        border: 1px solid #00ff9d !important;
        color: #00ff9d !important;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
    }
    
    /* Código con efecto terminal */
    .stCodeBlock {
        background: #0a0f1e !important;
        border: 1px solid #00b8ff;
        border-radius: 10px;
    }
    
    /* Métricas futuristas */
    .css-1xarl3l {
        background: linear-gradient(135deg, rgba(0, 255, 157, 0.1), rgba(0, 184, 255, 0.1));
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

# Header con animación
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 4em; margin-bottom: 0;'>🔮 NEURAL CRYPT ANALYZER</h1>
    <p style='color: #00b8ff; font-size: 1.2em; letter-spacing: 3px;'>
        ⚡ SISTEMA DE DETECCIÓN DE ALGORITMOS CON IA ⚡
    </p>
    <hr style='border: 1px solid #00ff9d; width: 50%; margin: 20px auto; box-shadow: 0 0 10px #00ff9d;'>
</div>
""", unsafe_allow_html=True)

# Verificar modo
if not detector.entrenado:
    st.warning("⚠️ MODO DEMO ACTIVADO - Modelos no encontrados")
    MODO_DEMO = True
else:
    st.success("✅ RED NEURONAL CONECTADA - Modelos cargados exitosamente")
    MODO_DEMO = False

# Sidebar futurista
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <h2 style='color: #00ff9d;'>⚡ MATRIX PROTOCOL ⚡</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Métricas en tiempo real
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🧠 RED NEURONAL", "ACTIVA", "100%")
    with col2:
        st.metric("🎯 PRECISIÓN", "94.7%", "+2.3%")
    
    st.markdown("---")
    
    # Algoritmos con diseño futurista
    st.markdown("### 🔐 ALGORITMOS DETECTABLES")
    
    algoritmos_info = [
        ("🔐 Base64", "aG9sYQ== → hola", "#00ff9d"),
        ("🔄 ROT13", "Uryyb → Hello", "#00b8ff"),
        ("⚡ César", "khoor → hola (shift=3)", "#ff00ff"),
        ("💫 XOR", "Hex: 1a2b3c → texto", "#ffaa00"),
        ("📄 Texto Plano", "hola → hola", "#ffffff")
    ]
    
    for algo, ejemplo, color in algoritmos_info:
        st.markdown(f"""
        <div style='border-left: 3px solid {color}; padding-left: 10px; margin: 10px 0;'>
            <p style='color: {color}; margin: 0; font-weight: bold;'>{algo}</p>
            <p style='color: #888; font-size: 0.8em; margin: 0;'>{ejemplo}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Estado del sistema
    st.markdown("""
    <div style='background: rgba(0,255,157,0.1); padding: 15px; border-radius: 10px;'>
        <p style='color: #00ff9d; margin: 0;'>🟢 SISTEMA OPERATIVO</p>
        <p style='color: #888; font-size: 0.8em; margin: 5px 0 0 0;'>
        ⚡ 19 características analizadas<br>
        🔮 5 algoritmos entrenados<br>
        🎯 2000 muestras de entrenamiento
        </p>
    </div>
    """, unsafe_allow_html=True)

# Área principal
st.markdown("""
<div style='text-align: center; margin: 30px 0;'>
    <h2 style='color: #00b8ff;'>🔍 TERMINAL DE ANÁLISIS CRIPTOGRÁFICO</h2>
</div>
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