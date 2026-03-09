# ============================================================
# PROYECTO: PREDICCIÓN DEL RENDIMIENTO ESTUDIANTIL
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import zipfile
import requests
import io
import warnings
warnings.filterwarnings('ignore')

print("✅ Proyecto iniciado correctamente")
print("=" * 50)

# Cargar datos
url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
response = requests.get(url)
outer_zip = zipfile.ZipFile(io.BytesIO(response.content))
inner_zip_data = outer_zip.read('student.zip')
inner_zip = zipfile.ZipFile(io.BytesIO(inner_zip_data))
csv_data = inner_zip.read('student-mat.csv').decode('utf-8')
Data = pd.read_csv(io.StringIO(csv_data), sep=';')

print(f"✅ Datos cargados: {Data.shape}")
print(Data.head())
