import numpy as np
import cv2

def etiquetas_a_rgb(etiquetas, height, width, incluir_leyenda=False):
    # Mapeo de colores solo para LUZ y SOMBRA
    color_map = {
        "LUZ": [255, 255, 0],     # Amarillo
        "SOMBRA": [50, 50, 50],   # Gris oscuro
    }

    # Imagen de salida inicializada como negra
    resultado = np.zeros((height * width, 3), dtype=np.uint8)

    for i, etiqueta in enumerate(etiquetas):
        if etiqueta in color_map:
            resultado[i] = color_map[etiqueta]

    resultado = resultado.reshape((height, width, 3))

    # Leyenda visual (opcional)
    if incluir_leyenda:
        cv2.rectangle(resultado, (20, 20), (280, 100), (255, 255, 255), -1)
        cv2.putText(resultado, "LUZ = Amarillo", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(resultado, "SOMBRA = Gris", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    return resultado