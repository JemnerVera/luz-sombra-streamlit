import json
import cv2
import numpy as np

def extraer_pixeles(labelme_json_path, imagen_path):
    """
    Extrae píxeles etiquetados desde anotaciones LabelMe, devolviendo su coordenada,
    color RGB y etiqueta.

    Devuelve:
    - Lista de tuplas (x, y, [R, G, B], etiqueta)
    """

    # Carga anotaciones
    with open(labelme_json_path, encoding='utf-8') as f:
        data = json.load(f)

    # Carga imagen
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        raise FileNotFoundError(f"❌ No se pudo cargar la imagen: {imagen_path}")

    height, width = imagen.shape[:2]
    pixeles = []

    for shape in data['shapes']:
        label = shape['label'].strip().upper()  # Consistencia con otros módulos
        points = np.array(shape['points'], dtype=np.int32)

        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(mask, [points], 1)

        indices = np.where(mask == 1)
        for y, x in zip(*indices):
            pixel_rgb = imagen[y, x].tolist()
            pixeles.append((x, y, pixel_rgb, label))

    print(f"Total de píxeles etiquetados extraídos: {len(pixeles)}")
    return pixeles