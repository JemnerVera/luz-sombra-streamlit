# 🌱 Análisis Agrícola - Luz y Sombra

Aplicación Streamlit para el análisis de luz y sombra en imágenes agrícolas usando Machine Learning.

## 🚀 Características

- **Análisis de Imágenes**: Procesamiento de múltiples imágenes con modelo Random Forest
- **Probar Modelo**: Visualización comparativa de análisis de luz y sombra
- **Historial**: Registro completo de análisis en Google Sheets
- **Interfaz Intuitiva**: Dropdowns dinámicos con filtros jerárquicos
- **Integración Google Sheets**: Sincronización automática de datos

## 📋 Requisitos

- Python 3.8+
- Streamlit
- OpenCV
- scikit-learn
- Google Sheets API

## 🛠️ Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/JemnerVera/luz-sombra-streamlit.git
cd luz-sombra-streamlit
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Instalar dependencias:**
```bash
pip install -r requirements_streamlit.txt
```

4. **Configurar Google Sheets:**
   - Copiar `google_sheets_config.json` con tus credenciales
   - Configurar `credentials.json` para la API de Google Sheets

## 🎯 Uso

1. **Ejecutar la aplicación:**
```bash
streamlit run streamlit_app.py --server.port 8504
```

2. **Abrir en el navegador:**
   - URL: http://localhost:8504

## 📊 Funcionalidades

### Analizar Imágenes
- Selección de campos: Empresa, Fundo, Sector, Lote
- Carga múltiple de imágenes
- Análisis con modelo Random Forest
- Guardado automático en Google Sheets

### Probar Modelo
- Visualización comparativa
- Análisis de luz (amarillo) y sombra (gris oscuro)
- Métricas de porcentaje

### Historial
- Registro completo de análisis
- Filtros y búsqueda
- Exportación a CSV

## 🔧 Configuración

### Google Sheets
1. Crear proyecto en Google Cloud Console
2. Habilitar Google Sheets API
3. Crear credenciales OAuth 2.0
4. Configurar `google_sheets_config.json`

### Modelo ML
- El modelo se carga desde `modelo_perfeccionado.pkl`
- Usa Random Forest de scikit-learn
- Análisis de características de imagen optimizadas

## 📁 Estructura del Proyecto

```
luz-sombra-streamlit/
├── streamlit_app.py              # Aplicación principal
├── requirements_streamlit.txt    # Dependencias Python
├── src/
│   ├── services/
│   │   └── procesamiento_service_v2.py  # Servicio de ML
│   └── google_sheets/
│       └── sheets_client.py      # Cliente Google Sheets
├── modelo_perfeccionado.pkl      # Modelo entrenado
├── google_sheets_config.json     # Configuración Google Sheets
├── credentials.json              # Credenciales API
└── README.md
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Autores

- **Jemner Vera** - *Desarrollo inicial* - [JemnerVera](https://github.com/JemnerVera)

## 🙏 Agradecimientos

- Modelo de Machine Learning desarrollado con scikit-learn
- Integración con Google Sheets API
- Interfaz desarrollada con Streamlit