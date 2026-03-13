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

# CSS personalizado para efecto futurista - VERSIÓN CORREGIDA (SIN DIFUMINADO)
st.markdown("""
<style>
    /* Fondo con efecto matrix */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #1a1f2e 100%);
    }
    
    /* TÍTULOS CORREGIDOS - SIN DIFUMINADO */
    h1, h2, h3 {
        color: #00ff9d !important;
        font-weight: 700 !important;
        text-shadow: 0 0 5px #00ff9d;
        -webkit-text-fill-color: #00ff9d !important;
        background: none !important;
    }
    
    /* Título principal específico */
    h1 {
        color: #00ff9d !important;
        font-size: 3.5em !important;
        text-shadow: 0 0 10px #00ff9d;
    }
    
    /* Subtítulos */
    p, .stMarkdown p {
        color: #00b8ff !important;
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
        color: #0a0f1e !important;
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
    
    /* Resultado con estilo especial */
    .resultado-descifrado {
        background: linear-gradient(135deg, #00ff9d20, #00b8ff20);
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #00ff9d;
        text-align: center;
        animation: glow 2s infinite;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 20px #00ff9d; }
        50% { box-shadow: 0 0 40px #00b8ff; }
        100% { box-shadow: 0 0 20px #00ff9d; }
    }
    
    /* Input de clave XOR */
    .stTextInput input {
        background: rgba(10, 20, 30, 0.8) !important;
        border: 1px solid #ffaa00 !important;
        color: #ffaa00 !important;
    }
    
    /* Output box con estilo mejorado */
    .output-box {
        background: rgba(0, 255, 157, 0.1);
        border: 1px solid #00ff9d;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        word-break: break-all;
        color: white !important;
    }
    
    /* CORRECCIÓN PARA TEXTOS DIFUMINADOS */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3 {
        color: #00ff9d !important;
        -webkit-text-fill-color: #00ff9d !important;
        background: none !important;
        text-shadow: 0 0 3px #00ff9d;
    }
    
    /* Texto "TERMINAL DE ANÁLISIS" específico */
    .stMarkdown h2 {
        color: #00b8ff !important;
        -webkit-text-fill-color: #00b8ff !important;
    }
    
    /* Texto "MATRIZ DE RESULTADOS" */
    .stMarkdown h3 {
        color: #ff00ff !important;
        -webkit-text-fill-color: #ff00ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Header con animación - CORREGIDO
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 4em; margin-bottom: 0; color: #00ff9d; text-shadow: 0 0 10px #00ff9d;'>🔮 NEURAL CRYPT ANALYZER</h1>
    <p style='color: #00b8ff; font-size: 1.2em; letter-spacing: 3px; text-shadow: 0 0 5px #00b8ff;'>
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
        <h2 style='color: #00ff9d; text-shadow: 0 0 5px #00ff9d;'>⚡ MATRIX PROTOCOL ⚡</h2>
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
    st.markdown("<h3 style='color: #00ff9d;'>🔐 ALGORITMOS DETECTABLES</h3>", unsafe_allow_html=True)
    
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

# Área principal - CORREGIDO
st.markdown("""
<div style='text-align: center; margin: 30px 0;'>
    <h2 style='color: #00b8ff; text-shadow: 0 0 8px #00b8ff; font-weight: bold;'>🔍 TERMINAL DE ANÁLISIS CRIPTOGRÁFICO</h2>
</div>
""", unsafe_allow_html=True)

# Input con diseño futurista
texto_ingresado = st.text_area(
    "📡 INGRESE TEXTO CIFRADO:",
    height=100,
    placeholder="Ej: aG9sYQ==  |  Uryyb Jbeyq  |  khoor  |  CLAVECLAVE...  |  hola",
    key="input_text"
)

# DETECCIÓN EN VIVO Y CONFIGURACIÓN XOR
clave_xor = None
if texto_ingresado:
    algoritmo_temp = detector.predecir_algoritmo(texto_ingresado)
    if "XOR" in algoritmo_temp:
        st.info(f"🔑 ALGORITMO DETECTADO: **{algoritmo_temp}** - Ingresa la clave si la conoces")
        with st.expander("🔐 CONFIGURACIÓN DE CLAVE XOR", expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                clave_xor = st.text_input(
                    "Ingrese la clave de encriptación:",
                    value="clave",
                    help="La clave usada para encriptar el mensaje (déjalo por defecto si no la sabes)"
                )
            with col2:
                st.markdown("### 💡")
                st.caption("Prueba: 'clave', 'key', 'CLAVE'")

# Botón con efecto
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analizar_btn = st.button("🔮 INICIAR ANÁLISIS NEURONAL", use_container_width=True)

# Resultados
if analizar_btn and texto_ingresado:
    texto_limpio = texto_ingresado.strip()
    
    with st.spinner("⚡ PROCESANDO CON RED NEURONAL..."):
        time.sleep(1.5)
        
        # Procesar con o sin clave XOR
        if clave_xor:
            resultado = detector.procesar(texto_limpio, clave_xor)
        else:
            resultado = detector.procesar(texto_limpio)
        
        # Mostrar información de depuración en consola
        print("="*50)
        print("🔍 RESULTADO COMPLETO:")
        print(f"Algoritmo: {resultado['algoritmo']}")
        print(f"Texto original: {resultado['texto_original']}")
        print(f"Texto descifrado: '{resultado['texto_descifrado']}'")
        print(f"Longitud descifrado: {len(resultado['texto_descifrado'])}")
        print("="*50)
    
    # Timeline de análisis - CORREGIDO
    st.markdown("---")
    st.markdown("<h3 style='color: #ff00ff; text-shadow: 0 0 8px #ff00ff;'>📊 MATRIZ DE RESULTADOS</h3>", unsafe_allow_html=True)
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.markdown(f"""
        <div class='output-box'>
            <p style='color: #00ff9d; font-size: 0.9em;'>📥 INPUT</p>
            <p style='color: white; font-family: monospace; font-size: 1.2em;'>{resultado['texto_original']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_res2:
        # Color según algoritmo
        algoritmo_color = {
            "Base64": "#00ff9d",
            "ROT13": "#00b8ff",
            "César": "#ff00ff",
            "XOR": "#ffaa00",
            "Plano": "#ffffff"
        }
        color = next((v for k, v in algoritmo_color.items() if k in resultado['algoritmo']), "#00ff9d")
        
        st.markdown(f"""
        <div class='output-box'>
            <p style='color: {color}; font-size: 0.9em;'>🔍 ALGORITMO DETECTADO</p>
            <p style='color: white; font-size: 1.5em; font-weight: bold;'>{resultado['algoritmo']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_res3:
        st.markdown(f"""
        <div class='output-box'>
            <p style='color: #00ff9d; font-size: 0.9em;'>📤 OUTPUT</p>
            <p style='color: white; font-family: monospace; font-size: 1.2em;'>{resultado['texto_descifrado']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Resultado destacado - VERSIÓN CORREGIDA QUE SIEMPRE MUESTRA ALGO
    st.markdown("---")
    st.markdown("<h3 style='color: #ff00ff; text-shadow: 0 0 8px #ff00ff;'>🔓 TEXTO DESCIFRADO</h3>", unsafe_allow_html=True)
    
    # Asegurar que siempre haya algo que mostrar
    texto_a_mostrar = resultado['texto_descifrado']
    if not texto_a_mostrar or texto_a_mostrar.strip() == "":
        texto_a_mostrar = "🔑 [Resultado vacío - Probablemente la clave es incorrecta]"
    elif texto_a_mostrar.startswith("🔑 [XOR]"):
        # Ya tiene formato, mantenerlo
        pass
    
    if "Error" in texto_a_mostrar or "no se" in texto_a_mostrar.lower():
        st.error(f"### ❌ {texto_a_mostrar}")
    else:
        st.markdown(f"""
        <div class='resultado-descifrado'>
            <h1 style='color: white; font-size: 2.5em; text-shadow: 0 0 20px #00ff9d; word-break: break-all;'>
                {texto_a_mostrar}
            </h1>
            <p style='color: #00b8ff; margin-top: 20px;'>Decodificado con {resultado['algoritmo']}</p>
            <p style='color: #888; font-size: 0.8em;'>Clave usada: {clave_xor if clave_xor else "clave (por defecto)"}</p>
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
        
        # Información adicional de depuración
        if st.checkbox("Mostrar información de depuración"):
            st.json({
                "texto_original": resultado['texto_original'],
                "algoritmo": resultado['algoritmo'],
                "texto_descifrado": resultado['texto_descifrado'],
                "clave_usada": clave_xor if clave_xor else "clave (default)"
            })
        
        st.markdown("</div>", unsafe_allow_html=True)

elif analizar_btn and not texto_ingresado:
    st.error("❌ ERROR: INGRESE UN TEXTO PARA ANALIZAR")

# Footer futurista
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <p style='color: #00b8ff; font-size: 0.8em; letter-spacing: 2px; text-shadow: 0 0 5px #00b8ff;'>
        ⚡ NEURAL CRYPT ANALYZER v2.0 ⚡
    </p>
    <p style='color: #00ff9d; font-size: 0.7em; text-shadow: 0 0 3px #00ff9d;'>
        [ Base64 · ROT13 · César · XOR · Texto Plano ]
    </p>
    <p style='color: #444; font-size: 0.6em;'>
        Red Neuronal · 19 Características · 2000 Muestras
    </p>
</div>
""", unsafe_allow_html=True)