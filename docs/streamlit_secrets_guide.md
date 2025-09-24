# 🔐 Guía de Configuración de Secrets para Streamlit Cloud

## 📋 Pasos para configurar las credenciales

### 1. **Obtener el Spreadsheet ID de Google Sheets**

1. Ve a tu Google Sheet
2. Copia la URL completa
3. El ID está entre `/d/` y `/edit`
   
   **Ejemplo:**
   ```
   https://docs.google.com/spreadsheets/d/1ABC123DEF456GHI789JKL/edit#gid=0
   ```
   **ID:** `1ABC123DEF456GHI789JKL`

### 2. **Configurar Secrets en Streamlit Cloud**

1. Ve a tu app en [share.streamlit.io](https://share.streamlit.io/)
2. Haz clic en "Manage App"
3. Ve a la pestaña "Secrets"
4. Agrega el siguiente contenido:

```toml
[google_sheets]
spreadsheet_id = "TU_SPREADSHEET_ID_AQUI"
sheet_name = "Data-app"
model_path = "modelo_perfeccionado.pkl"
```

### 3. **Configurar credenciales de Google Sheets API**

#### **Opción A: Usar archivos de credenciales (Recomendado)**

1. **Subir `credentials.json`:**
   - Ve a "Manage App" → "Files"
   - Sube tu archivo `credentials.json`
   - Asegúrate de que esté en la raíz del proyecto

2. **Subir `google_sheets_config.json`:**
   - Sube tu archivo `google_sheets_config.json`
   - Asegúrate de que esté en la raíz del proyecto

#### **Opción B: Usar variables de entorno**

En la sección "Secrets", agrega:

```toml
[google_sheets]
spreadsheet_id = "TU_SPREADSHEET_ID"
sheet_name = "Data-app"
model_path = "modelo_perfeccionado.pkl"

# Credenciales como variables de entorno
credentials_json = "TU_CREDENTIALS_JSON_BASE64"
```

### 4. **Verificar configuración**

Después de configurar los secrets:

1. Haz clic en "Redeploy" en Streamlit Cloud
2. Espera a que termine el despliegue
3. Verifica que la app funcione correctamente

### 5. **Troubleshooting**

#### **Error: "spreadsheet_id not found"**
- Verifica que el Spreadsheet ID sea correcto
- Asegúrate de que esté en la sección `[google_sheets]`

#### **Error: "Authentication failed"**
- Verifica que `credentials.json` esté subido
- Verifica que `google_sheets_config.json` esté subido
- Asegúrate de que las credenciales sean válidas

#### **Error: "Model not found"**
- Verifica que `modelo_perfeccionado.pkl` esté en el repositorio
- Verifica que el archivo no esté corrupto

### 6. **Estructura final de secrets**

```toml
[google_sheets]
spreadsheet_id = "1ABC123DEF456GHI789JKL"
sheet_name = "Data-app"
model_path = "modelo_perfeccionado.pkl"
```

### 7. **Archivos necesarios en el repositorio**

- ✅ `streamlit_app.py`
- ✅ `requirements_streamlit.txt`
- ✅ `src/` (código fuente)
- ✅ `modelo_perfeccionado.pkl`
- ✅ `.streamlit/config.toml`

### 8. **Archivos necesarios en Streamlit Cloud**

- ✅ `credentials.json` (subir manualmente)
- ✅ `google_sheets_config.json` (subir manualmente)

## 🔗 Enlaces útiles

- [Streamlit Cloud](https://share.streamlit.io/)
- [Streamlit Secrets](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [Google Sheets API](https://developers.google.com/sheets/api)



