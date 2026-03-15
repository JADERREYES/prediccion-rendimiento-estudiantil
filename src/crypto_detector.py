"""Detector de algoritmos criptográficos por reglas."""

import base64
import re


def es_hex(text):
    """Verifica si el texto parece hexadecimal válido."""
    cleaned = text.replace(" ", "").strip()
    return (
        len(cleaned) > 0
        and len(cleaned) % 2 == 0
        and re.fullmatch(r"[0-9a-fA-F]+", cleaned) is not None
    )


def es_binario(text):
    """Verifica si el texto parece binario válido."""
    cleaned = text.replace(" ", "").strip()
    return (
        len(cleaned) > 0
        and len(cleaned) % 8 == 0
        and re.fullmatch(r"[01]+", cleaned) is not None
    )


def es_base64(text):
    """Verifica si el texto parece Base64 válido."""
    cleaned = text.strip()

    if not cleaned:
        return False

    if len(cleaned) % 4 != 0:
        return False

    if re.fullmatch(r"[A-Za-z0-9+/=]+", cleaned) is None:
        return False

    try:
        decoded = base64.b64decode(cleaned, validate=True)
        return len(decoded) > 0
    except (ValueError, TypeError):
        return False


def es_url_encoding(text):
    """Verifica si el texto parece URL encoding."""
    return "%" in text or "+" in text


def es_rot13_probable(text):
    """Heurística simple para ROT13."""
    return re.search(r"[A-Za-z]", text) is not None


def detectar_algoritmo(text):
    """Detecta el algoritmo probable usando reglas."""
    text = text.strip()

    if not text:
        return "Unknown"

    if es_binario(text):
        return "Binary"

    if es_hex(text):
        return "Hex"

    if es_base64(text):
        return "Base64"

    if es_url_encoding(text):
        return "URL Encoding"

    if es_rot13_probable(text):
        return "ROT13"

    return "Unknown"


def calcular_confianza(_text):
    """Confianza por reglas."""
    return 96.0


def obtener_estado_modelo():
    """Estado simulado del modelo."""
    return {
        "model_loaded": True,
        "scaler_loaded": True,
    }


def obtener_modo_deteccion(_text):
    """Modo de detección."""
    return "Reglas"