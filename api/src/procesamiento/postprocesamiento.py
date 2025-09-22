import numpy as np

def contar_clases(etiquetas, clases_validas=None):
    """
    Cuenta la cantidad de píxeles por clase, ignorando las etiquetas no deseadas.
    """
    if clases_validas is None:
        clases_validas = ["LUZ", "SOMBRA", "HOJAS", "TRONCO", "UVA", "CIELO"]
    
    conteo = {clase: np.sum(etiquetas == clase) for clase in clases_validas}
    total = sum(conteo.values())

    print("📊 Conteo por clase:")
    for clase, cantidad in conteo.items():
        porc = (cantidad / total) * 100 if total > 0 else 0
        print(f"  - {clase}: {cantidad} píxeles ({porc:.2f}%)")

    return conteo, total

def calcular_porcentaje_suelo(etiquetas):
    """
    Calcula porcentaje de LUZ y SOMBRA sobre el suelo evaluado, excluyendo IGNORADOS.
    """
    etiquetas = np.array(etiquetas)
    clases_suelo = ["LUZ", "SOMBRA"]
    mask_suelo = np.isin(etiquetas, clases_suelo)

    etiquetas_suelo = etiquetas[mask_suelo]
    total_suelo = len(etiquetas_suelo)

    cuenta_luz = np.sum(etiquetas_suelo == "LUZ")
    cuenta_sombra = np.sum(etiquetas_suelo == "SOMBRA")

    porc_luz = round((cuenta_luz / total_suelo) * 100, 2) if total_suelo > 0 else 0.0
    porc_sombra = round((cuenta_sombra / total_suelo) * 100, 2) if total_suelo > 0 else 0.0

    print(f"\n Porcentaje luz sobre suelo: {porc_luz:.2f}%")
    print(f" Porcentaje sombra sobre suelo: {porc_sombra:.2f}%")
    print(f" Suma total suelo evaluado: {porc_luz + porc_sombra:.2f}%")

    return porc_luz, porc_sombra, total_suelo