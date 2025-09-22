import numpy as np
import cv2
from sklearn.preprocessing import StandardScaler

def normalizar_pixeles(pixeles_rgb):
    """
    Aplica normalización estándar (media 0, desviación estándar 1) a los valores RGB.
    """
    if pixeles_rgb is None or len(pixeles_rgb) == 0:
        raise ValueError("❌ La lista de píxeles está vacía.")

    pixeles_array = np.array(pixeles_rgb, dtype=np.float32)
    if pixeles_array.ndim != 2 or pixeles_array.shape[1] != 3:
        raise ValueError("❌ Cada píxel debe tener exactamente 3 componentes: [R, G, B].")

    print(f"▶️ Normalizando {pixeles_array.shape[0]} píxeles RGB...")
    scaler = StandardScaler()
    return scaler.fit_transform(pixeles_array)

def calcular_textura_vectorizado(imagen, kernel_size=3):
    """
    Calcula mapa de textura por píxel usando varianza local.
    """
    gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY).astype(np.float32)
    mean = cv2.blur(gray, (kernel_size, kernel_size))
    sqr_mean = cv2.blur(gray ** 2, (kernel_size, kernel_size))
    varianza = sqr_mean - mean ** 2
    return varianza

def normalizar_pixeles_con_textura(imagen, coordenadas, kernel_size=3):
    """
    Extrae y normaliza características [R, G, B, textura] por coordenada.
    """
    textura_map = calcular_textura_vectorizado(imagen, kernel_size)
    datos = []

    for x, y in coordenadas:
        if y >= imagen.shape[0] or x >= imagen.shape[1]:
            continue
        rgb = imagen[y, x].astype(np.float32)
        textura = textura_map[y, x]
        datos.append(np.append(rgb, textura))

    if not datos:
        raise ValueError("❌ No se generaron vectores para normalización.")

    datos_array = np.array(datos, dtype=np.float32)

    print(f"▶️ Normalizando {len(datos_array)} vectores RGB+textura...")
    scaler = StandardScaler()
    return scaler.fit_transform(datos_array)

def filtrar_sombra_refinada(etiquetas_np, imagen_bgr, textura_map,
                            umbral_textura=60, umbral_luminancia=65,
                            umbral_saturacion=130, ndvi_min=-0.3):
    """
    Filtra píxeles etiquetados como SOMBRA que probablemente son objetos oscuros (UVA/TRONCO)
    usando textura, luminancia, saturación y NDVI aproximado.
    """

    # Convertir imagen a formatos auxiliares
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
    hsv = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2HSV).astype(np.float32)
    saturacion = hsv[..., 1]
    textura_flat = textura_map.flatten()

    # Luminancia
    R, G, B = imagen_rgb[..., 0], imagen_rgb[..., 1], imagen_rgb[..., 2]
    luminancia = (0.299 * R + 0.587 * G + 0.114 * B).flatten()

    # NDVI aproximado
    ndvi_aprox = ((G - R) / (G + R + 1e-5)).flatten()

    # Condiciones compuestas
    sombra_mask = etiquetas_np == "SOMBRA"
    condiciones = (
        sombra_mask &
        (textura_flat < umbral_textura) &
        (luminancia < umbral_luminancia) &
        (saturacion.flatten() < umbral_saturacion) &
        (ndvi_aprox > ndvi_min)
    )

    etiquetas_filtradas = etiquetas_np.copy()
    etiquetas_filtradas[condiciones] = "IGNORADO"

    print(f"🔍 Sombra refinada — ignorados: {np.sum(condiciones)} píxeles")
    return etiquetas_filtradas