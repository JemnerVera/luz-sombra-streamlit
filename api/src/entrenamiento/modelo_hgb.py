import pickle
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np

def entrenar_modelo(X_train, y_train, modelo_path="modelo_hgb.pkl"):
    """
    Entrena un modelo HistGradientBoostingClassifier y guarda el clasificador junto con el LabelEncoder.

    Parámetros:
    - X_train: array de características (ej. píxeles normalizados)
    - y_train: array de etiquetas (ej. "LUZ", "SOMBRA", etc.)
    - modelo_path: ruta donde se guarda el modelo entrenado
    """

    if X_train is None or len(X_train) == 0:
        raise ValueError("❌ X_train está vacío")

    if len(X_train) != len(y_train):
        raise ValueError("❌ Longitudes de X_train y y_train no coinciden")

    print(f"📊 Entrenando modelo con {X_train.shape[0]} muestras y {X_train.shape[1]} características por píxel...")

    # Codificación de etiquetas
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y_train)

    # Entrenamiento del modelo
    model = HistGradientBoostingClassifier(random_state=42)
    model.fit(X_train, y_encoded)

    # Guardado del modelo y encoder
    with open(modelo_path, "wb") as f:
        pickle.dump((model, encoder), f)

    print("✅ Modelo entrenado (HGB) y guardado con clases:", list(encoder.classes_))