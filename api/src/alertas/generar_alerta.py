import numpy as np

def generar_alerta(mascara_sombra, umbral=0.4):
    """
    Genera una alerta si el porcentaje de sombra sobre la imagen supera el umbral especificado.

    Parámetros:
    - mascara_sombra: array binario (mismo tamaño que imagen), con 255 indicando sombra
    - umbral: float, umbral de alerta entre 0 y 1 (default = 0.4 → 40%)

    Retorna:
    - alerta_activa: bool, True si porcentaje ≥ umbral
    - porcentaje: float, proporción de píxeles de sombra
    """

    if mascara_sombra is None or mascara_sombra.size == 0:
        raise ValueError("❌ La máscara de sombra está vacía o no es válida.")

    total_pixeles = mascara_sombra.size
    pixeles_sombra = np.sum(mascara_sombra == 255)
    porcentaje = round(pixeles_sombra / total_pixeles, 4)

    alerta_activa = porcentaje >= umbral
    print(f"Porcentaje sombra: {porcentaje*100:.2f}%. Umbral: {umbral*100:.0f}% → {'ALERTA' if alerta_activa else 'OK'}")
    return alerta_activa, porcentaje