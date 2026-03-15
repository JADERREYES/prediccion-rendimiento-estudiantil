"""Módulo de análisis criptográfico con red neuronal."""

import os
import pickle

import joblib
import numpy as np
import tensorflow as tf

from src.entropy_analyzer import (
    shannon_entropy,
    ascii_range,
    numeric_ratio,
)


class NeuralCryptAnalyzer:
    """Analizador criptográfico basado en modelo neuronal + scaler."""

    def __init__(
        self,
        model_path="modelos/trained_mlp_model.h5",
        scaler_path="modelos/scaler.joblib",
    ):
        """Inicializa modelo, scaler y mapa de clases."""
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self.scaler_loaded = False

        self.class_map = {
            0: "Base64",
            1: "ROT13",
            2: "Plain",
            3: "Cesar",
            4: "XOR",
        }

        try:
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                self.scaler_loaded = True
        except (
            OSError,
            ValueError,
            EOFError,
            ModuleNotFoundError,
            ImportError,
            AttributeError,
            pickle.UnpicklingError,
        ) as error:
            print(f"[ERROR] No se pudo cargar scaler.joblib: {error}")
            self.scaler = None
            self.scaler_loaded = False

        try:
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
                self.model_loaded = True
        except (
            OSError,
            ValueError,
            ImportError,
            TypeError,
            AttributeError,
        ) as error:
            print(f"[ERROR] No se pudo cargar trained_mlp_model.h5: {error}")
            self.model = None
            self.model_loaded = False

    def is_ready(self):
        """Indica si el modelo y el scaler están listos."""
        return self.model_loaded and self.scaler_loaded

    def extraer_caracteristicas(self, texto):
        """Extrae el vector de 17 características esperado por el modelo."""
        texto = texto or ""
        longitud = len(texto)

        entropia = shannon_entropy(texto)
        ratio_numerico = numeric_ratio(texto)

        ascii_min, ascii_max = ascii_range(texto)
        ascii_diff = ascii_max - ascii_min if texto else 0
        ascii_sum = sum(ord(c) for c in texto)

        uppercase_ratio = sum(1 for c in texto if c.isupper()) / max(longitud, 1)
        lowercase_ratio = sum(1 for c in texto if c.islower()) / max(longitud, 1)
        espacio_ratio = sum(1 for c in texto if c.isspace()) / max(longitud, 1)

        simbolo_ratio = sum(
            1 for c in texto if not c.isalnum() and not c.isspace()
        ) / max(longitud, 1)

        unique_ratio = len(set(texto)) / max(longitud, 1)
        vowel_ratio = sum(1 for c in texto if c.lower() in "aeiou") / max(longitud, 1)

        repetidos = sum(
            1 for indice in range(1, len(texto))
            if texto[indice] == texto[indice - 1]
        ) / max(longitud - 1, 1)

        base64_ratio = sum(
            1
            for c in texto
            if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        ) / max(longitud, 1)

        digit_ratio = sum(1 for c in texto if c.isdigit()) / max(longitud, 1)
        alpha_ratio = sum(1 for c in texto if c.isalpha()) / max(longitud, 1)

        features = [
            longitud,
            entropia,
            ratio_numerico,
            uppercase_ratio,
            lowercase_ratio,
            espacio_ratio,
            simbolo_ratio,
            ascii_min,
            ascii_max,
            ascii_diff,
            ascii_sum,
            unique_ratio,
            vowel_ratio,
            repetidos,
            base64_ratio,
            digit_ratio,
            alpha_ratio,
        ]

        return np.array(features, dtype=float).reshape(1, -1)

    def predecir(self, texto):
        """Realiza la predicción con IA y devuelve resultado estructurado."""
        if not self.is_ready():
            return {
                "algoritmo": None,
                "confianza": 0.0,
                "modo": "Reglas",
                "probabilidades": None,
            }

        try:
            caracteristicas = self.extraer_caracteristicas(texto)

            if caracteristicas.shape[1] != self.scaler.n_features_in_:
                return {
                    "algoritmo": None,
                    "confianza": 0.0,
                    "modo": "Reglas",
                    "probabilidades": None,
                }

            caracteristicas_scaled = self.scaler.transform(caracteristicas)
            pred = self.model.predict(caracteristicas_scaled, verbose=0)[0]

            best_index = int(np.argmax(pred))
            algoritmo = self.class_map.get(best_index, "Unknown")
            confianza = float(pred[best_index]) * 100.0

            return {
                "algoritmo": algoritmo,
                "confianza": confianza,
                "modo": "IA",
                "probabilidades": pred.tolist(),
            }

        except (
            ValueError,
            TypeError,
            AttributeError,
            IndexError,
        ) as error:
            print(f"[ERROR] Fallo en predicción IA: {error}")
            return {
                "algoritmo": None,
                "confianza": 0.0,
                "modo": "Reglas",
                "probabilidades": None,
            }

    def estado_modelo(self):
        """Devuelve el estado de carga del modelo y scaler."""
        return {
            "model_loaded": self.model_loaded,
            "scaler_loaded": self.scaler_loaded,
        }