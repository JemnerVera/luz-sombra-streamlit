import os
import json
import cv2
import numpy as np

def generar_mascaras(path_json, path_img, path_out, clases=["sombra", "luz"]):
    os.makedirs(path_out, exist_ok=True)

    for nombre_json in os.listdir(path_json):
        ruta_json = os.path.join(path_json, nombre_json)
        nombre_base = nombre_json.replace(".json", "")
        ruta_img = os.path.join(path_img, nombre_base + ".JPG")

        img = cv2.imread(ruta_img)
        if img is None:
            print(f"❌ Imagen no encontrada: {ruta_img}")
            continue

        height, width = img.shape[:2]

        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        etiquetas_encontradas = [shape["label"].lower() for shape in data.get("shapes", [])]

        for clase in clases:
            if clase not in etiquetas_encontradas:
                print(f"⚠️ Clase '{clase}' no encontrada en {nombre_json}")
                continue

            mask = np.zeros((height, width), dtype=np.uint8)
            dibujado = False

            for shape in data["shapes"]:
                if shape["label"].lower() == clase:
                    puntos = np.array(shape["points"], dtype=np.int32)
                    cv2.fillPoly(mask, [puntos], 255)
                    dibujado = True

            if dibujado:
                nombre_mask = f"mask_{nombre_base}_{clase}.png"
                ruta_mask = os.path.join(path_out, nombre_mask)
                cv2.imwrite(ruta_mask, mask)
                print(f"✅ Máscara guardada: {nombre_mask}")
            else:
                print(f"⚠️ No se pudo dibujar máscara para clase '{clase}' en {nombre_json}")