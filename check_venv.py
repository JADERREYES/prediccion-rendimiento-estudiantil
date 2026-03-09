# check_venv.py
import sys
import os

print("=" * 50)
print("🔍 VERIFICACIÓN DEL ENTORNO")
print("=" * 50)

print(f"📌 Python executable: {sys.executable}")
print(f"📌 Python version: {sys.version}")
print(f"📌 Current directory: {os.getcwd()}")

print("\n📦 Verificando paquetes instalados:")
print("-" * 30)

packages_ok = True

try:
    import numpy
    print(f"✅ numpy {numpy.__version__} - OK")
except ImportError:
    print("❌ numpy - NO INSTALADO")
    packages_ok = False

try:
    import pandas
    print(f"✅ pandas {pandas.__version__} - OK")
except ImportError:
    print("❌ pandas - NO INSTALADO")
    packages_ok = False

try:
    import matplotlib
    print(f"✅ matplotlib {matplotlib.__version__} - OK")
except ImportError:
    print("❌ matplotlib - NO INSTALADO")
    packages_ok = False

try:
    import sklearn
    print(f"✅ scikit-learn {sklearn.__version__} - OK")
except ImportError:
    print("❌ scikit-learn - NO INSTALADO")
    packages_ok = False

try:
    import requests
    print(f"✅ requests {requests.__version__} - OK")
except ImportError:
    print("❌ requests - NO INSTALADO")
    packages_ok = False

print("\n" + "=" * 50)

if packages_ok:
    print("🎉 ¡TODO ESTÁ CORRECTO! Puedes ejecutar el proyecto.")
else:
    print("⚠️  FALTAN PAQUETES. Ejecuta: pip install -r requirements.txt")

print("=" * 50)