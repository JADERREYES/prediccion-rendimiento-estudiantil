# src/encriptacion.py - VERSIÓN FINAL CON DETECCIÓN MEJORADA PARA TODOS LOS ALGORITMOS
import joblib
import numpy as np
import os
import base64
import codecs
import tensorflow as tf
from pathlib import Path

# Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
MODELOS_DIR = os.path.join(BASE_DIR, "modelos")

class DetectorEncriptacion:
    def __init__(self):
        """Carga los modelos entrenados en Colab"""
        try:
            # Cargar scaler
            self.scaler = joblib.load(os.path.join(MODELOS_DIR, "scaler.joblib"))
            
            # Cargar modelo .h5
            self.modelo = tf.keras.models.load_model(os.path.join(MODELOS_DIR, "trained_mlp_model.h5"))
            
            self.entrenado = True
            print("✅ Modelos de encriptación cargados correctamente")
        except Exception as e:
            print(f"❌ Error cargando modelos: {e}")
            self.entrenado = False
    
    def extraer_caracteristicas(self, texto):
        """Convierte texto cifrado a 17 características numéricas"""
        if not texto or len(texto) == 0:
            return np.zeros(17)
        
        # 1. Métricas básicas
        longitud = len(texto)
        mayusculas = sum(1 for c in texto if c.isupper())
        minusculas = sum(1 for c in texto if c.islower())
        digitos = sum(1 for c in texto if c.isdigit())
        espacios = sum(1 for c in texto if c.isspace())
        especiales = longitud - mayusculas - minusculas - digitos - espacios
        
        # 2. Caracteres específicos por algoritmo
        hex_chars = sum(1 for c in texto if c.lower() in '0123456789abcdef')
        base64_chars = sum(1 for c in texto if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=')
        
        # 3. Entropía
        from collections import Counter
        import math
        freqs = Counter(texto)
        entropia = 0
        if longitud > 0:
            entropia = -sum((freq/longitud) * math.log2(freq/longitud) for freq in freqs.values())
        
        # 4. Patrones específicos
        padding = texto.count('=')
        termina_en_igual = 1 if texto.endswith('=') else 0
        
        # 5. 17 CARACTERÍSTICAS
        features = [
            longitud,                 # 1
            mayusculas,               # 2
            minusculas,                # 3
            digitos,                   # 4
            espacios,                  # 5
            especiales,                # 6
            hex_chars,                 # 7
            base64_chars,              # 8
            entropia,                  # 9
            padding,                   # 10
            len(set(texto)),           # 11
            texto.count('+'),          # 12
            texto.count('/'),          # 13
            termina_en_igual,          # 14
            1 if texto.replace(' ', '').isdigit() else 0,  # 15
            1 if all(c in '01' for c in texto.replace(' ', '')) else 0,  # 16
            1 if texto.isupper() else 0,  # 17
        ]
        
        return np.array(features).reshape(1, -1)
    
    def detectar_rot13(self, texto):
        """Detecta si el texto está en ROT13"""
        try:
            # Aplicar ROT13
            probar = codecs.decode(texto, 'rot_13')
            
            # Lista de palabras comunes en español para detectar
            palabras_comunes = [
                'hola', 'como', 'estas', 'mundo', 'cifrado', 'encriptado',
                'texto', 'mensaje', 'clave', 'secreto', 'hola', 'adios',
                'buenos', 'dias', 'tardes', 'noches', 'por', 'favor',
                'gracias', 'perdon', 'disculpa', 'ayuda', 'sistema',
                'todo', 'puede', 'ser', 'para', 'con', 'sin', 'sobre',
                'entre', 'durante', 'mediante', 'segun', 'segun'
            ]
            
            probar_lower = probar.lower()
            
            # Verificar si el resultado contiene palabras comunes
            for palabra in palabras_comunes:
                if palabra in probar_lower:
                    return True, probar
            
            # Verificar proporción de letras y espacios
            letras = sum(1 for c in probar if c.isalpha())
            espacios = sum(1 for c in probar if c.isspace())
            
            # Si tiene buena proporción de letras y espacios
            if letras > len(probar) * 0.5:
                return True, probar
            
            return False, texto
        except:
            return False, texto
    
    def detectar_cesar(self, texto):
        """Detecta si el texto está en Cifrado César"""
        try:
            mejores_resultados = []
            
            for shift in range(1, 26):
                resultado = ""
                for char in texto:
                    if char.isalpha():
                        mayus = char.isupper()
                        base = ord('A') if mayus else ord('a')
                        nuevo_char = chr((ord(char) - base - shift) % 26 + base)
                        resultado += nuevo_char
                    else:
                        resultado += char
                
                # Calcular puntuación de legibilidad
                palabras_comunes = ['hola', 'como', 'esta', 'mundo', 'texto', 'mensaje']
                puntaje = sum(1 for palabra in palabras_comunes if palabra in resultado.lower())
                puntaje += sum(1 for c in resultado if c.isalpha()) * 0.1
                
                mejores_resultados.append((puntaje, shift, resultado))
            
            # Elegir el mejor resultado
            mejor = max(mejores_resultados, key=lambda x: x[0])
            
            # Si tiene buena puntuación, devolverlo
            if mejor[0] > len(texto) * 0.3:
                return True, mejor[2], mejor[1]
            
            return False, texto, 0
        except:
            return False, texto, 0
    
    def detectar_base64(self, texto):
        """Detecta si el texto está en Base64"""
        try:
            # Verificar formato Base64
            if texto.endswith('=') and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in texto):
                # Intentar decodificar
                decodificado = base64.b64decode(texto).decode('utf-8', errors='ignore')
                # Verificar si el resultado tiene letras
                if any(c.isalpha() for c in decodificado):
                    return True, decodificado
            return False, texto
        except:
            return False, texto
    
    def detectar_xor(self, texto):
        """Detecta si el texto podría ser XOR (hexadecimal)"""
        try:
            # Verificar si es hexadecimal
            if all(c in '0123456789abcdef' for c in texto) and len(texto) % 2 == 0:
                return True
            return False
        except:
            return False
    
    def predecir_algoritmo(self, texto):
        """Predice qué algoritmo de encriptación se usó - VERSIÓN MEJORADA"""
        
        # 1. DETECTAR BASE64
        es_base64, resultado_base64 = self.detectar_base64(texto)
        if es_base64:
            print(f"🔍 Detectado BASE64: '{resultado_base64[:50]}...'")
            return "🔐 Base64"
        
        # 2. DETECTAR ROT13
        es_rot13, resultado_rot13 = self.detectar_rot13(texto)
        if es_rot13:
            print(f"🔍 Detectado ROT13: '{resultado_rot13[:50]}...'")
            return "🔄 ROT13"
        
        # 3. DETECTAR CÉSAR
        es_cesar, resultado_cesar, shift = self.detectar_cesar(texto)
        if es_cesar:
            print(f"🔍 Detectado CÉSAR (shift={shift}): '{resultado_cesar[:50]}...'")
            return "⚡ Cifrado César"
        
        # 4. DETECTAR XOR (hexadecimal)
        if self.detectar_xor(texto):
            print(f"🔍 Detectado XOR (formato hexadecimal)")
            return "💫 XOR"
        
        # 5. VERIFICAR SI ES TEXTO PLANO
        letras = sum(1 for c in texto if c.isalpha())
        espacios = sum(1 for c in texto if c.isspace())
        
        # Si tiene muchas letras y espacios, es texto plano
        if letras > len(texto) * 0.5:
            palabras_comunes = ['hola', 'como', 'esta', 'mundo', 'texto', 'clave']
            texto_lower = texto.lower()
            for palabra in palabras_comunes:
                if palabra in texto_lower:
                    print(f"🔍 Detectado TEXTO PLANO (contiene '{palabra}')")
                    return "📄 Texto Plano"
        
        # 6. USAR EL MODELO DE IA SOLO SI TODO LO ANTERIOR FALLÓ
        if self.entrenado:
            try:
                caracteristicas = self.extraer_caracteristicas(texto)
                caracteristicas_scaled = self.scaler.transform(caracteristicas)
                
                prediccion_proba = self.modelo.predict(caracteristicas_scaled, verbose=0)
                prediccion = np.argmax(prediccion_proba, axis=1)[0]
                
                algoritmos = {
                    0: "🔐 Base64",
                    1: "🔄 ROT13",
                    2: "⚡ Cifrado César",
                    3: "💫 XOR",
                    4: "📄 Texto Plano"
                }
                
                algoritmo = algoritmos.get(prediccion, "❓ Desconocido")
                print(f"🔍 IA detectó: {algoritmo}")
                return algoritmo
            except Exception as e:
                print(f"❌ Error en IA: {e}")
                return self._detectar_por_reglas(texto)
        else:
            return self._detectar_por_reglas(texto)
    
    def _detectar_por_reglas(self, texto):
        """Detección por reglas simples (modo DEMO)"""
        if texto.endswith('=') and all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in texto):
            return "🔐 Base64"
        elif all(c in '0123456789abcdef' for c in texto) and len(texto) % 2 == 0:
            return "💫 XOR"
        elif all(c.isalpha() or c.isspace() for c in texto):
            # Probar si es ROT13
            try:
                probar = codecs.decode(texto, 'rot_13')
                palabras = ['hola', 'hello', 'como', 'mundo', 'cifrado']
                if any(palabra in probar.lower() for palabra in palabras):
                    return "🔄 ROT13"
            except:
                pass
            return "⚡ Cifrado César"
        else:
            return "📄 Texto Plano"
    
    def descifrar_xor(self, texto, clave=None):
        """Descifra XOR - VERSIÓN MEJORADA"""
        try:
            # Si es hexadecimal, convertir
            if all(c in '0123456789abcdef' for c in texto) and len(texto) % 2 == 0:
                texto_bytes = bytes.fromhex(texto)
                es_hex = True
            else:
                texto_bytes = texto.encode('utf-8')
                es_hex = False
            
            # Si no hay clave, usar "clave" por defecto
            if clave is None or clave == "":
                clave = "clave"
            
            clave_bytes = clave.encode('utf-8')
            
            # Aplicar XOR
            resultado_bytes = bytearray()
            for i, b in enumerate(texto_bytes):
                resultado_bytes.append(b ^ clave_bytes[i % len(clave_bytes)])
            
            # Convertir a string
            resultado = resultado_bytes.decode('utf-8', errors='ignore')
            
            # Verificar si el resultado es legible
            letras = sum(1 for c in resultado if c.isalpha())
            if letras > len(resultado) * 0.3:
                return resultado
            else:
                return f"🔑 Resultado con clave '{clave}': {resultado}"
                    
        except Exception as e:
            return f"❌ Error XOR: {str(e)}"
    
    def descifrar_cesar_avanzado(self, texto):
        """Intenta varios desplazamientos para César"""
        mejores_resultados = []
        
        for shift in range(1, 26):
            resultado = ""
            for char in texto:
                if char.isalpha():
                    mayus = char.isupper()
                    base = ord('A') if mayus else ord('a')
                    nuevo_char = chr((ord(char) - base - shift) % 26 + base)
                    resultado += nuevo_char
                else:
                    resultado += char
            
            # Calcular puntuación
            palabras_comunes = ['hola', 'como', 'esta', 'mundo', 'texto', 'mensaje', 'clave']
            puntaje = sum(2 for palabra in palabras_comunes if palabra in resultado.lower())
            puntaje += sum(0.1 for c in resultado if c.isalpha())
            puntaje += sum(0.5 for c in resultado if c.isspace())
            
            mejores_resultados.append((puntaje, shift, resultado))
        
        # Elegir el mejor resultado
        mejor = max(mejores_resultados, key=lambda x: x[0])
        
        # Si el mejor resultado tiene buena puntuación
        if mejor[0] > 0:
            return f"{mejor[2]} (shift={mejor[1]})"
        else:
            return texto
    
    def descifrar(self, texto, algoritmo, clave_xor=None):
        """Descifra el texto según el algoritmo detectado"""
        try:
            if "Base64" in algoritmo:
                try:
                    return base64.b64decode(texto).decode('utf-8', errors='ignore')
                except:
                    return f"❌ Error decodificando Base64"
            
            elif "ROT13" in algoritmo:
                try:
                    return codecs.decode(texto, 'rot_13')
                except:
                    return f"❌ Error decodificando ROT13"
            
            elif "César" in algoritmo:
                return self.descifrar_cesar_avanzado(texto)
            
            elif "XOR" in algoritmo:
                return self.descifrar_xor(texto, clave_xor)
            
            elif "Plano" in algoritmo:
                return texto
            
            else:
                return f"⚠️ Algoritmo no soportado: {algoritmo}"
                
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def procesar(self, texto, clave_xor=None):
        """Método principal: detecta algoritmo Y descifra"""
        algoritmo = self.predecir_algoritmo(texto)
        texto_descifrado = self.descifrar(texto, algoritmo, clave_xor)
        
        # Para debugging
        print("="*60)
        print(f"📊 TEXTO ORIGINAL: {texto}")
        print(f"🔍 ALGORITMO DETECTADO: {algoritmo}")
        print(f"✅ TEXTO DESCIFRADO: {texto_descifrado}")
        print("="*60)
        
        return {
            "algoritmo": algoritmo,
            "texto_original": texto,
            "texto_descifrado": texto_descifrado
        }

detector = DetectorEncriptacion()