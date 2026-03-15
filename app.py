"""Interfaz principal del Crypto Security Operations Center."""

import streamlit as st
import plotly.graph_objects as go

from src.crypto_detector import detectar_algoritmo
from src.decryptor import decrypt_text
from src.entropy_analyzer import (
    ascii_range,
    numeric_ratio,
    shannon_entropy,
    threat_level,
)
from src.encriptacion import NeuralCryptAnalyzer


CLASS_LABELS = ["Base64", "ROT13", "Plain", "Cesar", "XOR"]


def inject_styles():
    """Aplica estilo visual futurista limpio."""
    st.markdown(
        """
        <style>
        :root {
            --bg-0: #02050b;
            --bg-1: #07111d;
            --bg-2: #0d1726;
            --panel: rgba(8, 14, 24, 0.82);
            --panel-2: rgba(4, 8, 15, 0.92);
            --line: rgba(0, 255, 157, 0.18);
            --line-strong: rgba(0, 255, 157, 0.34);
            --txt: #ddffee;
            --txt-soft: #9effd0;
            --green: #00ff9d;
            --cyan: #63d8ff;
            --ok: #4dffae;
            --warn: #ffd166;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(0,255,157,0.05), transparent 18%),
                radial-gradient(circle at top right, rgba(99,216,255,0.04), transparent 20%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-0) 100%);
            color: var(--txt);
        }

        /* Rejilla sutil estilo cyber */
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background-image:
                linear-gradient(rgba(0,255,157,0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,255,157,0.04) 1px, transparent 1px);
            background-size: 38px 38px;
            opacity: 0.22;
        }

        /* Glow suave */
        .stApp::after {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 0;
            background:
                radial-gradient(circle at 20% 20%, rgba(0,255,157,0.05), transparent 24%),
                radial-gradient(circle at 80% 15%, rgba(99,216,255,0.05), transparent 20%),
                radial-gradient(circle at 50% 85%, rgba(0,255,157,0.03), transparent 28%);
        }

        #MainMenu, header, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1380px;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            position: relative;
            z-index: 2;
        }

        html, body, [class*="css"] {
            color: var(--txt);
        }

        h1, h2, h3 {
            color: var(--green) !important;
            font-family: Consolas, "Courier New", monospace !important;
            text-shadow: 0 0 10px rgba(0,255,157,0.14);
        }

        h1 {
            font-size: 2.2rem !important;
            margin-bottom: 0.15rem !important;
            letter-spacing: 1px;
        }

        h2 {
            font-size: 1.08rem !important;
        }

        h3 {
            font-size: 0.98rem !important;
        }

        .hero-box {
            background: linear-gradient(180deg, var(--panel), var(--panel-2));
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 20px 22px 18px 22px;
            box-shadow:
                0 0 0 1px rgba(255,255,255,0.02),
                0 0 26px rgba(0,255,157,0.06),
                inset 0 0 26px rgba(0,255,157,0.02);
            margin-bottom: 14px;
            backdrop-filter: blur(6px);
        }

        .hero-title {
            font-family: Consolas, "Courier New", monospace;
            font-size: 2.2rem;
            font-weight: 800;
            color: #d9ffee;
            letter-spacing: 1.4px;
            text-shadow:
                0 0 10px rgba(0,255,157,0.16),
                0 0 20px rgba(99,216,255,0.08);
        }

        .hero-sub {
            color: var(--txt-soft);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.92rem;
            letter-spacing: 1px;
            margin-top: 4px;
            margin-bottom: 10px;
        }

        .hero-desc {
            color: #aef9d5;
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.88rem;
            opacity: 0.95;
        }

        .neon-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,255,157,0.70), transparent);
            box-shadow: 0 0 12px rgba(0,255,157,0.18);
            margin-top: 10px;
        }

        .panel-box {
            background: linear-gradient(180deg, rgba(9, 14, 23, 0.84), rgba(4, 8, 15, 0.95));
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 16px 18px;
            box-shadow:
                0 0 18px rgba(0,255,157,0.04),
                inset 0 0 18px rgba(0,255,157,0.02);
            margin-bottom: 14px;
            backdrop-filter: blur(6px);
        }

        .section-label {
            font-family: Consolas, "Courier New", monospace;
            color: var(--green);
            font-size: 1rem;
            letter-spacing: 0.7px;
            margin-bottom: 10px;
        }

        textarea, .stTextArea textarea {
            background: rgba(5, 10, 18, 0.96) !important;
            color: #dbffee !important;
            border: 1px solid var(--line-strong) !important;
            border-radius: 16px !important;
            font-family: Consolas, "Courier New", monospace !important;
            font-size: 15px !important;
            box-shadow: 0 0 16px rgba(0,255,157,0.05) !important;
        }

        label, .stTextArea label {
            color: var(--green) !important;
            font-weight: 700 !important;
            font-family: Consolas, "Courier New", monospace !important;
        }

        .helper-text {
            color: #97f7cb;
            font-size: 0.84rem;
            font-family: Consolas, "Courier New", monospace;
            opacity: 0.92;
            margin-top: 8px;
        }

        div[data-testid="stAlert"] {
            border-radius: 14px !important;
            border: 1px solid var(--line) !important;
            box-shadow: 0 0 14px rgba(0,255,157,0.04);
        }

        div[data-testid="metric-container"] {
            background: linear-gradient(180deg, rgba(8, 13, 22, 0.94), rgba(4, 8, 14, 0.98));
            border: 1px solid var(--line);
            padding: 16px;
            border-radius: 16px;
            box-shadow: 0 0 14px rgba(0,255,157,0.03);
        }

        div[data-testid="metric-container"] label {
            color: var(--txt-soft) !important;
            font-family: Consolas, "Courier New", monospace !important;
            font-size: 0.83rem !important;
        }

        .chip-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 14px;
        }

        .chip-card {
            background: rgba(0,255,157,0.05);
            border: 1px solid rgba(0,255,157,0.16);
            border-radius: 16px;
            padding: 12px 14px;
            box-shadow: inset 0 0 10px rgba(0,255,157,0.02);
        }

        .chip-label {
            display: block;
            color: var(--txt-soft);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.78rem;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }

        .chip-value {
            display: block;
            color: #ffffff;
            font-family: Consolas, "Courier New", monospace;
            font-size: 1rem;
            font-weight: 700;
        }

        .terminal-box {
            background: linear-gradient(180deg, rgba(3,7,12,0.98), rgba(1,3,7,0.99));
            border: 1px solid rgba(0,255,157,0.22);
            border-radius: 16px;
            padding: 12px 14px;
            box-shadow:
                inset 0 0 18px rgba(0,255,157,0.02),
                0 0 18px rgba(0,255,157,0.04);
        }

        .terminal-head {
            display: flex;
            gap: 8px;
            margin-bottom: 10px;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .dot-red { background: #ff5c8a; box-shadow: 0 0 8px #ff5c8a; }
        .dot-yellow { background: #ffd166; box-shadow: 0 0 8px #ffd166; }
        .dot-green { background: #00ff9d; box-shadow: 0 0 8px #00ff9d; }

        pre, code {
            background: rgba(4, 8, 14, 0.98) !important;
            color: #98ffd2 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(0,255,157,0.14) !important;
            font-family: Consolas, "Courier New", monospace !important;
        }

        .foot-note {
            color: #94f7c8;
            font-size: 0.82rem;
            font-family: Consolas, "Courier New", monospace;
            opacity: 0.84;
            margin-top: 8px;
        }

        @media (max-width: 900px) {
            .chip-grid {
                grid-template-columns: 1fr;
            }
        }

        ::-webkit-scrollbar {
            width: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #03060c;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(0,255,157,0.18);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(0,255,157,0.30);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_analyzer():
    """Carga el analizador neuronal una vez."""
    return NeuralCryptAnalyzer()


def build_radar(probabilities):
    """Construye el radar de probabilidades IA."""
    radar_values = list(probabilities) + [probabilities[0]]
    radar_theta = CLASS_LABELS + [CLASS_LABELS[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=radar_values,
            theta=radar_theta,
            fill="toself",
            name="AI",
            line=dict(width=2),
            opacity=0.75,
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor="rgba(0,255,157,0.14)",
                tickfont=dict(color="#9effd0"),
            ),
            angularaxis=dict(
                gridcolor="rgba(0,255,157,0.10)",
                tickfont=dict(color="#9effd0", size=12),
            ),
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        height=360,
    )
    return fig


def render_header(model_state):
    """Renderiza cabecera principal."""
    st.markdown(
        """
        <div class="hero-box">
            <div class="hero-title">CRYPTO SECURITY OPERATIONS CENTER</div>
            <div class="hero-sub">[ NEURAL CRYPT ANALYZER / CYBER INTERFACE / THREAT SOC PANEL ]</div>
            <div class="hero-desc">
                Motor híbrido con análisis por IA entrenada + reglas heurísticas para inspección de cadenas cifradas,
                codificadas o sospechosas.
            </div>
            <div class="neon-divider"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if model_state["model_loaded"] and model_state["scaler_loaded"]:
        st.success("✅ RED NEURONAL CONECTADA · Modelo y scaler cargados exitosamente")
    else:
        st.warning("⚠️ IA no disponible. Se usará detección por reglas.")


def render_input():
    """Renderiza bloque de entrada."""
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    user_text = st.text_area(
        "✍️ INGRESE TEXTO CIFRADO",
        height=150,
        placeholder="Ejemplo: Q3liZXJzZWN1cml0eSBhbmFseXN0cyBpbnZlc3RpZ2F0ZSBlbmNvZGVkIG1lc3NhZ2Vz",
    )
    st.markdown(
        '<div class="helper-text">Consejo: ingresa una sola cadena por análisis para una clasificación más precisa.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return user_text


def render_summary(detected_algorithm, confidence_value, detection_mode, decoded_result):
    """Renderiza resumen principal."""
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">⚡ RESUMEN DE ANÁLISIS</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="chip-grid">
            <div class="chip-card">
                <span class="chip-label">ALGORITMO</span>
                <span class="chip-value">{detected_algorithm}</span>
            </div>
            <div class="chip-card">
                <span class="chip-label">CONFIANZA</span>
                <span class="chip-value">{confidence_value:.2f}%</span>
            </div>
            <div class="chip-card">
                <span class="chip-label">MODO</span>
                <span class="chip-value">{detection_mode}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">🔓 RESULTADO</div>', unsafe_allow_html=True)
    st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="terminal-head">
            <div class="dot dot-red"></div>
            <div class="dot dot-yellow"></div>
            <div class="dot dot-green"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.code(decoded_result)
    st.markdown("</div>", unsafe_allow_html=True)

    if isinstance(decoded_result, str) and decoded_result.strip():
        st.success("✔ Texto procesado correctamente")

    st.markdown("</div>", unsafe_allow_html=True)


def render_metrics(entropy_value, ascii_span, numeric_value, threat_value):
    """Renderiza métricas."""
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">📊 TELEMETRÍA DEL MENSAJE</div>', unsafe_allow_html=True)

    col_1, col_2, col_3, col_4 = st.columns(4)

    with col_1:
        st.metric("Entropy", f"{entropy_value:.4f}")

    with col_2:
        st.metric("ASCII Range", f"{ascii_span[0]} - {ascii_span[1]}")

    with col_3:
        st.metric("Numeric Ratio", f"{numeric_value:.4f}")

    with col_4:
        st.metric("Threat Level", threat_value)

    st.markdown("</div>", unsafe_allow_html=True)


def render_ai_panel(probabilities):
    """Renderiza panel IA."""
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">🤖 AI CLASSIFICATION RADAR</div>', unsafe_allow_html=True)

    radar_col, detail_col = st.columns([1.15, 1])

    with radar_col:
        st.plotly_chart(build_radar(probabilities), use_container_width=True)

    with detail_col:
        st.markdown('<div class="section-label">📡 DETALLE DE PROBABILIDADES</div>', unsafe_allow_html=True)
        for label_name, prob_value in zip(CLASS_LABELS, probabilities):
            st.write(f"{label_name}: {prob_value:.4f}")
            st.progress(min(max(float(prob_value), 0.0), 1.0))

    st.markdown(
        '<div class="foot-note">Panel probabilístico generado por la red neuronal entrenada.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def main():
    """Ejecuta la aplicación."""
    st.set_page_config(
        page_title="Crypto SOC",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    inject_styles()

    analyzer = load_analyzer()
    model_state = analyzer.estado_modelo()

    render_header(model_state)
    user_text = render_input()

    if not user_text:
        return

    clean_text = user_text.strip()
    ai_result = analyzer.predecir(clean_text)

    if ai_result["algoritmo"] is not None:
        detected_algorithm = ai_result["algoritmo"]
        confidence_value = ai_result["confianza"]
        detection_mode = ai_result["modo"]
    else:
        detected_algorithm = detectar_algoritmo(clean_text)
        confidence_value = 96.0
        detection_mode = "Reglas"

    decoded_result = decrypt_text(clean_text, detected_algorithm)

    entropy_value = shannon_entropy(clean_text)
    ascii_span = ascii_range(clean_text)
    numeric_value = numeric_ratio(clean_text)
    threat_value = threat_level(entropy_value, numeric_value)

    print("=" * 80)
    print("[APP] Texto recibido desde frontend:", clean_text)
    print("[APP] Resultado final:")
    print("  - Algoritmo:", detected_algorithm)
    print("  - Confianza:", round(confidence_value, 2))
    print("  - Modo:", detection_mode)
    print("  - Descifrado:", decoded_result)
    print("=" * 80)

    render_summary(
        detected_algorithm=detected_algorithm,
        confidence_value=confidence_value,
        detection_mode=detection_mode,
        decoded_result=decoded_result,
    )
    render_metrics(
        entropy_value=entropy_value,
        ascii_span=ascii_span,
        numeric_value=numeric_value,
        threat_value=threat_value,
    )

    if ai_result["probabilidades"] is not None:
        render_ai_panel(ai_result["probabilidades"])


if __name__ == "__main__":
    main()