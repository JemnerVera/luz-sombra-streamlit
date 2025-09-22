import numpy as np

def calcular_porcentajes_luz_sombra(predicciones):
    predicciones = np.array(predicciones)

    # Filtramos sólo los píxeles de suelo: LUZ o SOMBRA
    suelo_mask = (predicciones == "LUZ") | (predicciones == "SOMBRA")

    # Contamos dentro de la zona válida
    sombra_pix = np.sum(predicciones[suelo_mask] == "SOMBRA")
    luz_pix = np.sum(predicciones[suelo_mask] == "LUZ")
    total_pix = sombra_pix + luz_pix

    if total_pix == 0:
        return 0.0, 0.0  # evitar división por cero

    # Calculamos proporciones normalizadas
    porcentaje_luz = round(luz_pix / total_pix, 4)
    porcentaje_sombra = round(sombra_pix / total_pix, 4)

    return porcentaje_luz, porcentaje_sombra