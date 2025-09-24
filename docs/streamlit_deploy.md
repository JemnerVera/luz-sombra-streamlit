# 🚀 Guía de Despliegue en Streamlit Cloud

## 📋 Pasos para desplegar en Streamlit Cloud

### 1. **Preparar el repositorio**
- ✅ Repositorio en GitHub: `https://github.com/JemnerVera/luz-sombra-streamlit`
- ✅ Archivos principales: `streamlit_app.py`, `requirements_streamlit.txt`
- ✅ Configuración: `.streamlit/config.toml`

### 2. **Configurar Streamlit Cloud**
1. Ve a [share.streamlit.io](https://share.streamlit.io/)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"
4. Selecciona el repositorio: `JemnerVera/luz-sombra-streamlit`
5. Branch: `master`
6. Main file path: `streamlit_app.py`

### 3. **Configurar Secrets**
En la sección "Secrets" de Streamlit Cloud, agrega:

```toml
[google_sheets]
spreadsheet_id = "TU_SPREADSHEET_ID"
sheet_name = "Data-app"
model_path = "modelo_perfeccionado.pkl"
```

### 4. **Archivos necesarios en el repositorio**
- ✅ `streamlit_app.py` - Aplicación principal
- ✅ `requirements_streamlit.txt` - Dependencias
- ✅ `src/` - Código fuente
- ✅ `.streamlit/config.toml` - Configuración
- ❌ `modelo_perfeccionado.pkl` - **FALTA** (archivo grande)
- ❌ `credentials.json` - **FALTA** (credenciales)

### 5. **Problemas a resolver**

#### **Modelo ML (modelo_perfeccionado.pkl)**
- **Problema**: Archivo muy grande para GitHub
- **Solución**: Usar Git LFS o subir a un servicio de almacenamiento

#### **Credenciales Google Sheets**
- **Problema**: Archivos sensibles
- **Solución**: Usar Streamlit Secrets o variables de entorno

### 6. **Alternativas de despliegue**

#### **Opción A: Streamlit Cloud (Recomendado)**
- ✅ Gratuito
- ✅ Fácil configuración
- ✅ Integración con GitHub
- ❌ Limitaciones de tamaño de archivo

#### **Opción B: Heroku**
- ✅ Soporte para archivos grandes
- ✅ Variables de entorno
- ❌ Requiere tarjeta de crédito

#### **Opción C: Railway**
- ✅ Soporte para archivos grandes
- ✅ Variables de entorno
- ❌ Requiere configuración adicional

### 7. **Configuración recomendada para Streamlit Cloud**

#### **Modificar streamlit_app.py para usar secrets:**
```python
import streamlit as st

# Cargar configuración desde secrets
if 'google_sheets' in st.secrets:
    spreadsheet_id = st.secrets['google_sheets']['spreadsheet_id']
    sheet_name = st.secrets['google_sheets']['sheet_name']
else:
    st.error("❌ Configuración de Google Sheets no encontrada")
    st.stop()
```

#### **Subir modelo a un servicio de almacenamiento:**
- Google Drive
- Dropbox
- AWS S3
- GitHub Releases (con Git LFS)

### 8. **Pasos siguientes**
1. **Subir modelo** a un servicio de almacenamiento
2. **Modificar código** para descargar modelo automáticamente
3. **Configurar secrets** en Streamlit Cloud
4. **Desplegar** la aplicación

## 🔗 Enlaces útiles
- [Streamlit Cloud](https://share.streamlit.io/)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Git LFS](https://git-lfs.github.io/)



