# 🌱 Análisis Agrícola Luz-Sombra - Streamlit

## 📋 Descripción

Aplicación web para análisis de luz y sombra en imágenes agrícolas usando **K-means clustering** y **OpenCV**.

## 🚀 Características

- **📸 Análisis de Imágenes**: Upload múltiple con información del campo
- **🧪 Probar Modelo**: Prueba individual con visualización
- **📊 Historial**: Registro de análisis con filtros
- **🎨 Interfaz Moderna**: Replica la interfaz React original
- **⚡ Procesamiento Rápido**: K-means clustering optimizado

## 🛠️ Instalación Local

### Opción 1: Ejecutar directamente
```bash
# Instalar dependencias
pip install -r requirements_streamlit.txt

# Ejecutar aplicación
streamlit run streamlit_app.py
```

### Opción 2: Usar script automático
```bash
# En Windows
run_streamlit.bat

# En Linux/Mac
chmod +x run_streamlit.sh
./run_streamlit.sh
```

## 🌐 Deploy en Streamlit Cloud

### 1. Subir a GitHub
```bash
git add .
git commit -m "Add Streamlit app"
git push origin main
```

### 2. Conectar con Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu cuenta GitHub
3. Selecciona el repositorio
4. Configura:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.11
5. Deploy automático

## 📱 Uso de la Aplicación

### Tab "Analizar Imágenes"
1. **Completa información del campo**:
   - Empresa, Fundo, Sector, Lote (obligatorios)
   - Hilera, N° Planta (opcionales)
2. **Sube imágenes** (múltiples)
3. **Haz clic en "Analizar Imágenes"**
4. **Ve resultados** con visualización

### Tab "Probar Modelo"
1. **Sube una imagen** para probar
2. **Ve análisis visual** con colores:
   - 🟡 **Amarillo**: Áreas de luz
   - ⚫ **Gris oscuro**: Áreas de sombra
3. **Revisa métricas** de porcentajes

### Tab "Historial"
1. **Filtra resultados** por empresa/fecha
2. **Ve tabla** con todos los análisis
3. **Exporta CSV** si es necesario

## 🔧 Configuración

### Tema Personalizado
El archivo `.streamlit/config.toml` configura:
- **Colores**: Verde (#22c55e) y azul oscuro
- **Fuente**: Sans serif
- **Layout**: Wide por defecto

### Parámetros de Análisis
En `streamlit_app.py` puedes ajustar:
```python
# Número de clusters para K-means
num_clusters = 4

# Tamaño mínimo de objetos
min_size = 500

# Redimensionamiento de imagen
fx=0.5, fy=0.5  # 50% del tamaño original
```

## 📊 Algoritmo de Análisis

### 1. Preprocesamiento
- **Conversión a Lab**: Mejor separación de luz/color
- **Redimensionamiento**: Acelera procesamiento
- **Normalización**: Valores float32 para K-means

### 2. K-means Clustering
- **4 clusters** por defecto
- **Criterios**: 100 iteraciones, 0.2 epsilon
- **Segmentación**: Regiones visualmente similares

### 3. Análisis de Sombra
- **Umbral Otsu**: Automático
- **Morfología**: Cierre para refinar
- **Máscara binaria**: Sombra vs luz

### 4. Visualización
- **Imagen original**: Sin modificar
- **Análisis**: Colores superpuestos
- **Métricas**: Porcentajes calculados

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements_streamlit.txt
```

### Error: "OpenCV not found"
```bash
pip install opencv-python==4.8.1.78
```

### Error: "Streamlit not found"
```bash
pip install streamlit==1.28.1
```

### Puerto ocupado
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📈 Próximas Mejoras

- [ ] **Integración Google Sheets**: Datos reales
- [ ] **Análisis GPS**: Coordenadas automáticas
- [ ] **Modelo ML**: Reemplazar K-means
- [ ] **Exportación**: PDF con resultados
- [ ] **Filtros avanzados**: Por fecha, empresa, etc.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Add nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📞 Soporte

Para soporte técnico, contacta al equipo de desarrollo.

---

**🌱 Desarrollado con Streamlit para análisis agrícola**



