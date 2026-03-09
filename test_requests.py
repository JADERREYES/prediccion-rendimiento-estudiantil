# test_requests.py
import sys
print(f"Python executable: {sys.executable}")

try:
    import requests
    print(f"✅ requests {requests.__version__} instalado correctamente")
    print(f"Ubicación: {requests.__file__}")
except ImportError as e:
    print(f"❌ Error: {e}")

print("\nVerificando otros paquetes:")
try:
    import numpy
    print(f"✅ numpy {numpy.__version__}")
except: print("❌ numpy")

try:
    import pandas
    print(f"✅ pandas {pandas.__version__}")
except: print("❌ pandas")