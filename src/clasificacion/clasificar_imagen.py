import pickle
import numpy as np

def clasificar_imagen(X_pixels, modelo_path="modelo_rf.pkl"):
    """
    Clasifica cada píxel usando un modelo Random Forest entrenado.
    
    Parámetros:
    - X_pixels: array de píxeles normalizados, forma (n_pixeles, 3)
    - modelo_path: ruta al archivo pickle del modelo y encoder

    Retorna:
    - Array con etiquetas por píxel (ej. ["LUZ", "SUELO", "SOMBRA", ...])
    """
    try:
        with open(modelo_path, "rb") as f:
            model, encoder = pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ No se encontró el archivo de modelo en: {modelo_path}")
    except Exception as e:
        raise RuntimeError(f"❌ Error al cargar el modelo: {e}")

    # Clasificación
    y_pred_encoded = model.predict(X_pixels)
    y_pred = encoder.inverse_transform(y_pred_encoded)

    print(f" Clasificación realizada sobre {len(X_pixels)} píxeles.")
    return np.array(y_pred)