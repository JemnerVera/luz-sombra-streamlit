# 🌱 Análisis Agrícola Luz-Sombra

Aplicación web para análisis de luz y sombra en imágenes agrícolas usando **Streamlit** y **Machine Learning**.

## 📋 Descripción

Esta aplicación permite analizar imágenes agrícolas para determinar el porcentaje de luz y sombra presente, utilizando un modelo de Random Forest entrenado. Los resultados se almacenan automáticamente en Google Sheets.

## 🚀 Características

- **📸 Análisis de Imágenes**: Upload múltiple con información del campo
- **🧪 Probar Modelo**: Prueba individual con visualización
- **📊 Historial**: Registro de análisis con filtros
- **🎨 Interfaz Moderna**: Diseño intuitivo y responsivo
- **⚡ Procesamiento Rápido**: Modelo Random Forest optimizado
- **📈 Integración Google Sheets**: Almacenamiento automático de resultados

## 📁 Estructura del Proyecto

```
app-luz-sombra-py/
├── 📁 config/                    # Archivos de configuración
│   ├── google_sheets_config.json
│   ├── service_account_google_sheets.json
│   └── token.json
├── 📁 docs/                      # Documentación
│   ├── README_STREAMLIT.md
│   ├── GOOGLE_SHEETS_SETUP.md
│   ├── SETUP_COMPLETO.md
│   ├── streamlit_deploy.md
│   └── streamlit_secrets_guide.md
├── 📁 models/                    # Modelos de ML
│   └── modelo_perfeccionado.pkl
├── 📁 scripts/                   # Scripts de ejecución
│   ├── start_app.bat
│   └── run_streamlit.bat
├── 📁 src/                       # Código fuente
│   ├── alertas/
│   ├── analisis/
│   ├── clasificacion/
│   ├── database/
│   ├── entrenamiento/
│   ├── evaluacion/
│   ├── google_sheets/
│   ├── metadata/
│   ├── procesamiento/
│   ├── services/
│   └── visualizacion/
├── 📁 dataset/                   # Datos de entrenamiento
│   ├── anotaciones/
│   └── imagenes/
├── 📁 resultados/                # Imágenes procesadas
├── 📁 venv/                      # Entorno virtual Python
├── streamlit_app.py              # Aplicación principal
└── requirements_streamlit.txt    # Dependencias
```

## 🛠️ Instalación y Uso

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
scripts/start_app.bat

# O directamente
scripts/run_streamlit.bat
```

## 🌐 Deploy en Streamlit Cloud

1. **Subir a GitHub**:
   ```bash
   git add .
   git commit -m "Add Streamlit app"
   git push origin main
   ```

2. **Conectar con Streamlit Cloud**:
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Conecta tu cuenta GitHub
   - Selecciona el repositorio
   - Configura:
     - **Main file path**: `streamlit_app.py`
     - **Python version**: 3.11

3. **Configurar Secrets**:
   - Ve a Settings > Secrets
   - Agrega las variables de Google Sheets

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

### Google Sheets
1. Configura las credenciales en `config/`
2. Actualiza `config/google_sheets_config.json`
3. Verifica permisos en Google Sheets

### Modelo ML
- El modelo se encuentra en `models/modelo_perfeccionado.pkl`
- Es un Random Forest entrenado con scikit-learn
- Procesa características de textura y color

## 📊 Algoritmo de Análisis

### 1. Preprocesamiento
- **Conversión a Lab**: Mejor separación de luz/color
- **Redimensionamiento**: Acelera procesamiento
- **Normalización**: Valores float32 para ML

### 2. Random Forest
- **100 árboles** por defecto
- **Características**: Textura, color, estadísticas
- **Clasificación**: Luz vs Sombra por píxel

### 3. Postprocesamiento
- **Morfología**: Refinamiento de máscaras
- **Filtrado**: Eliminación de ruido
- **Cálculo**: Porcentajes finales

### 4. Visualización
- **Imagen original**: Sin modificar
- **Análisis**: Colores superpuestos
- **Métricas**: Porcentajes calculados

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
pip install -r requirements_streamlit.txt
```

### Error: "Modelo no encontrado"
- Verifica que `models/modelo_perfeccionado.pkl` existe
- El modelo se descarga automáticamente si está en secrets

### Error: "Google Sheets no conecta"
- Verifica credenciales en `config/`
- Revisa permisos en Google Sheets
- Confirma que el spreadsheet_id es correcto

### Puerto ocupado
```bash
streamlit run streamlit_app.py --server.port 8502
```

## 📈 Próximas Mejoras

- [ ] **Análisis GPS**: Coordenadas automáticas
- [ ] **Modelo mejorado**: Deep Learning
- [ ] **Exportación**: PDF con resultados
- [ ] **Filtros avanzados**: Por fecha, empresa, etc.
- [ ] **Dashboard**: Estadísticas en tiempo real

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

## 🔗 Enlaces Útiles

- [Documentación Streamlit](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [scikit-learn](https://scikit-learn.org/)
- [OpenCV](https://opencv.org/)