"""Funciones de decodificación y descifrado."""

import os
import base64
import codecs
import urllib.parse
from dotenv import load_dotenv

# ==========================================
# CARGAR VARIABLES DE ENTORNO
# ==========================================
load_dotenv()

# ==========================================
# CONFIGURACIÓN XOR
# ==========================================
# Clave XOR en HEX, por defecto "Key" => 4b6579
XOR_KEY_HEX = os.environ.get("XOR_KEY_HEX", "4b6579")

try:
    XOR_KEY = bytes.fromhex(XOR_KEY_HEX)
except ValueError:
    XOR_KEY = b"Key"


def is_readable(text):
    """Evalúa si un texto es legible."""
    if not text:
        return False

    printable = sum(1 for char in text if 32 <= ord(char) <= 126)
    ratio = printable / max(len(text), 1)
    return ratio > 0.85


def xor_with_key(data, key):
    """Aplica XOR con una clave fija."""
    if not key:
        return data

    result = bytearray()
    for index, byte in enumerate(data):
        result.append(byte ^ key[index % len(key)])
    return bytes(result)


def decode_base64(text):
    """Decodifica Base64 e intenta XOR si no es legible."""
    try:
        decoded = base64.b64decode(text, validate=False)

        decoded_text = decoded.decode("utf-8", errors="replace")
        if is_readable(decoded_text):
            return decoded_text

        xor_result = xor_with_key(decoded, XOR_KEY)
        xor_text = xor_result.decode("utf-8", errors="replace")
        if is_readable(xor_text):
            return (
                "Base64 decodificado + XOR con clave fija\n"
                f"Clave HEX: {XOR_KEY_HEX}\n"
                f"Texto: {xor_text}"
            )

        return f"Bytes decodificados (posible cifrado): {decoded.hex()}"

    except (ValueError, TypeError, base64.binascii.Error):
        return "No se pudo decodificar Base64."


def decode_hex(text):
    """Decodifica hexadecimal e intenta XOR si no es legible."""
    try:
        cleaned = text.replace(" ", "").strip()
        raw = bytes.fromhex(cleaned)

        decoded_text = raw.decode("utf-8", errors="replace")
        if is_readable(decoded_text):
            return decoded_text

        xor_result = xor_with_key(raw, XOR_KEY)
        xor_text = xor_result.decode("utf-8", errors="replace")
        if is_readable(xor_text):
            return (
                "HEX decodificado + XOR con clave fija\n"
                f"Clave HEX: {XOR_KEY_HEX}\n"
                f"Texto: {xor_text}"
            )

        return f"HEX decodificado a bytes (posible XOR/AES): {raw.hex()}"

    except (ValueError, TypeError):
        return "No se pudo decodificar HEX."


def decode_binary(text):
    """Decodifica binario e intenta XOR si no es legible."""
    try:
        cleaned = text.replace(" ", "").strip()

        if len(cleaned) % 8 != 0:
            return "Longitud binaria inválida."

        raw = bytes(
            int(cleaned[index:index + 8], 2)
            for index in range(0, len(cleaned), 8)
        )

        decoded_text = raw.decode("utf-8", errors="replace")
        if is_readable(decoded_text):
            return decoded_text

        xor_result = xor_with_key(raw, XOR_KEY)
        xor_text = xor_result.decode("utf-8", errors="replace")
        if is_readable(xor_text):
            return (
                "Binario decodificado + XOR con clave fija\n"
                f"Clave HEX: {XOR_KEY_HEX}\n"
                f"Texto: {xor_text}"
            )

        return "Binario convertido pero no parece texto."

    except (ValueError, TypeError):
        return "No se pudo decodificar Binario."


def decode_rot13(text):
    """Aplica ROT13."""
    try:
        return codecs.decode(text, "rot_13")
    except (ValueError, TypeError):
        return "No se pudo aplicar ROT13."


def decode_url(text):
    """Decodifica URL encoding."""
    try:
        return urllib.parse.unquote_plus(text)
    except (TypeError, ValueError):
        return "No se pudo decodificar URL Encoding."


def caesar_shift(text, shift):
    """Aplica desplazamiento César."""
    result = []

    for char in text:
        if "a" <= char <= "z":
            result.append(chr((ord(char) - ord("a") - shift) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            result.append(chr((ord(char) - ord("A") - shift) % 26 + ord("A")))
        else:
            result.append(char)

    return "".join(result)


def caesar_auto(text):
    """Intenta descifrar César probando todos los desplazamientos."""
    best = text
    best_score = 0

    for shift in range(1, 26):
        candidate = caesar_shift(text, shift)
        score = sum(1 for char in candidate if char in "aeiouAEIOU ") + (
            20 if is_readable(candidate) else 0
        )

        if score > best_score:
            best_score = score
            best = candidate

    return best


def xor_bruteforce(hex_text):
    """Intenta XOR simple por fuerza bruta sobre texto hexadecimal."""
    try:
        data = bytes.fromhex(hex_text.replace(" ", "").strip())
        results = []

        for key in range(1, 256):
            decoded = bytes(byte ^ key for byte in data)

            try:
                decoded_text = decoded.decode("utf-8", errors="strict")
                if is_readable(decoded_text):
                    results.append((key, decoded_text))
            except UnicodeDecodeError:
                continue

        if results:
            key, txt = results[0]
            return (
                f"XOR posible\n"
                f"Key decimal: {key}\n"
                f"Key hex: {hex(key)}\n"
                f"Texto: {txt}"
            )

        return "No se encontró clave XOR simple."

    except ValueError:
        return "No se pudo aplicar XOR."


def decrypt_xor_with_env_key(text, input_format="hex"):
    """Descifra XOR usando la clave del .env según formato de entrada."""
    try:
        cleaned = text.strip()

        if input_format == "hex":
            raw = bytes.fromhex(cleaned.replace(" ", ""))
        elif input_format == "base64":
            raw = base64.b64decode(cleaned, validate=False)
        elif input_format == "binary":
            cleaned = cleaned.replace(" ", "")
            if len(cleaned) % 8 != 0:
                return "Longitud binaria inválida para XOR."

            raw = bytes(
                int(cleaned[index:index + 8], 2)
                for index in range(0, len(cleaned), 8)
            )
        else:
            return "Formato de entrada XOR no soportado."

        result = xor_with_key(raw, XOR_KEY)
        text_result = result.decode("utf-8", errors="replace")

        if is_readable(text_result):
            return (
                "XOR con clave fija aplicado correctamente\n"
                f"Clave HEX: {XOR_KEY_HEX}\n"
                f"Texto: {text_result}"
            )

        return (
            "XOR con clave fija aplicado, pero el resultado no parece texto.\n"
            f"Resultado HEX: {result.hex()}"
        )

    except (ValueError, TypeError, UnicodeDecodeError, base64.binascii.Error) as error:
        return f"No se pudo aplicar XOR con clave fija: {error}"


def decrypt_text(text, algorithm):
    """Decodifica o descifra según el algoritmo detectado."""
    algorithm = (algorithm or "").strip().lower()
    result = "No se pudo descifrar."

    if algorithm == "base64":
        result = decode_base64(text)

    elif algorithm == "hex":
        result = decode_hex(text)

        if "posible XOR" in result or "HEX decodificado a bytes" in result:
            xor_try = xor_bruteforce(text)
            result = result + "\n\nIntento XOR:\n" + xor_try

    elif algorithm == "binary":
        result = decode_binary(text)

    elif algorithm == "rot13":
        result = decode_rot13(text)

    elif algorithm == "caesar":
        result = caesar_auto(text)

    elif algorithm == "url encoding":
        result = decode_url(text)

    elif algorithm == "xor":
        env_try = decrypt_xor_with_env_key(text, "hex")
        brute_try = xor_bruteforce(text)
        result = (
            f"{env_try}\n\n"
            f"Intento adicional por fuerza bruta:\n{brute_try}"
        )

    elif algorithm == "vigenere":
        result = "Detectado Vigenere pero requiere clave."

    elif algorithm == "aes":
        result = "AES detectado pero requiere clave."

    elif algorithm == "rsa":
        result = "RSA detectado pero requiere clave privada."

    return result