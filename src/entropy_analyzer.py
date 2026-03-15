"""Funciones de análisis estadístico del texto cifrado."""

import math
from collections import Counter


def shannon_entropy(text):
    """Calcula la entropía de Shannon."""
    if not text:
        return 0.0

    freq = Counter(text)
    total = len(text)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in freq.values()
    )


def ascii_range(text):
    """Devuelve el rango ASCII mínimo y máximo del texto."""
    if not text:
        return "N/A"

    values = [ord(char) for char in text]
    return f"{min(values)} - {max(values)}"


def numeric_ratio(text):
    """Calcula la proporción de caracteres numéricos."""
    if not text:
        return 0.0

    numeric_count = sum(1 for char in text if char.isdigit())
    return numeric_count / len(text)


def threat_level(entropy, ratio):
    """Clasifica el nivel de riesgo según entropía y proporción numérica."""
    if entropy > 4.5 and ratio > 0.25:
        return "HIGH"
    if entropy > 3.0:
        return "MEDIUM"
    return "LOW"