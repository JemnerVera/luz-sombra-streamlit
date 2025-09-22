import os
import cv2
import numpy as np

def analizar_intensidad(path_img, path_mask, clases=["sombra", "luz"]):
    resultados = {}

    for archivo_mask in os.listdir(path_mask):
        ruta_mask = os.path.join(path_mask, archivo_mask)
        nombre_base = archivo_mask.replace(".png", "").replace("mask_", "")
        clase = [c for c in clases if c in archivo_mask]
        if not clase:
            continue
        clase = clase[0]

        # Imagen correspondiente
        nombre_img = "_".join(nombre_base.split("_")[:-1]) + ".JPG"
        ruta_img = os.path.join(path_img, nombre_img)

        img = cv2.imread(ruta_img, cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(ruta_mask, cv2.IMREAD_GRAYSCALE)
        if img is None or mask is None:
            print(f"❌ No se pudo cargar {ruta_img} o {ruta_mask}")
            continue

        # Extraer píxeles donde la máscara es blanca (valor 255)
        pixeles_clase = img[mask == 255]

        if len(pixeles_clase) == 0:
            print(f"⚠️ Máscara sin cobertura útil: {archivo_mask}")
            continue

        media = np.mean(pixeles_clase)
        std = np.std(pixeles_clase)
        min_val = np.min(pixeles_clase)
        max_val = np.max(pixeles_clase)

        resultados.setdefault(nombre_img, {})[clase] = {
            "media": round(media, 2),
            "std": round(std, 2),
            "min": int(min_val),
            "max": int(max_val),
            "pixeles": len(pixeles_clase)
        }

    return resultados