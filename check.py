import sys
import os

print("=" * 50)
print("🔍 VERIFICACIÓN DEL ENTORNO")
print("=" * 50)

print(f"📌 Python: {sys.executable}")
print(f"📌 Versión: {sys.version}")
print(f"📌 Carpeta: {os.getcwd()}")

print("\n📦 Paquetes instalados:")
print("-" * 30)

try:
    import numpy as np
    print(f"✅ numpy {np.__version__}")
except: print("❌ numpy")

try:
    import pandas as pd
    print(f"✅ pandas {pd.__version__}")
except: print("❌ pandas")

try:
    import matplotlib.pyplot as plt
    print(f"✅ matplotlib {plt.matplotlib.__version__}")
except: print("❌ matplotlib")

try:
    import sklearn
    print(f"✅ scikit-learn {sklearn.__version__}")
except: print("❌ scikit-learn")

try:
    import requests
    print(f"✅ requests {requests.__version__}")
except: print("❌ requests")

print("=" * 50)
