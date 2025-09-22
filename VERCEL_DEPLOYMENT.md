# 🚀 Guía Paso a Paso: Despliegue en Vercel

## 📋 Prerrequisitos

- ✅ Cuenta en [Vercel](https://vercel.com)
- ✅ Cuenta en [Railway](https://railway.app) o [Render](https://render.com) para el backend
- ✅ Repositorio en GitHub
- ✅ Archivos de credenciales de Google Sheets

## 🎯 Paso 1: Preparar Credenciales

### 1.1 Ejecutar Script de Preparación
```bash
# En tu terminal, desde la raíz del proyecto
venv\Scripts\python prepare_vercel_credentials.py
```

### 1.2 Copiar Variables de Entorno
El script generará un archivo `vercel_env_vars.txt` con las variables necesarias. **NO subas este archivo al repositorio.**

## 🎯 Paso 2: Desplegar Backend en Railway

### 2.1 Crear Cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Inicia sesión con GitHub
3. Haz clic en "New Project"

### 2.2 Conectar Repositorio
1. Selecciona "Deploy from GitHub repo"
2. Busca y selecciona tu repositorio
3. Railway detectará automáticamente que es un proyecto Python

### 2.3 Configurar Variables de Entorno en Railway
1. Ve a tu proyecto en Railway
2. Haz clic en la pestaña "Variables"
3. Agrega las siguientes variables:

```bash
# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=1H3oobEJdidbJ2S7Ms3nW0ZbSR-yKiZHQNZp2pubXIU4
GOOGLE_SHEETS_SHEET_NAME=Data-app

# Google Sheets Credentials (Base64)
GOOGLE_SHEETS_CREDENTIALS_BASE64=eyJpbnN0YWxsZWQiOnsiY2xpZW50X2lkIjoiNTEwMTAxMjA4MzYxLW1pMGk5NjVkOGlhM29sbW85bDFnNDZzZjlkbjI4ZTFlLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwicHJvamVjdF9pZCI6ImFwcC1sdXotc29tYnJhIiwiYXV0aF91cmkiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsInRva2VuX3VyaSI6Imh0dHBzOi8vb2F1dHgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjoiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dHgyL3YxL2NlcnRzIiwiY2xpZW50X3NlY3JldCI6IkdPQ1NQWC0tdUwxU1B0N2RROW0tZ1VLRWpoYkZBZ0ljdjNaIiwicmVkaXJlY3RfdXJpcyI6WyJodHRwOi8vbG9jYWxob3N0Il19fQ==
GOOGLE_SHEETS_TOKEN_BASE64=eyJ0b2tlbiI6ICJ5YTI5LmEwQVFRX0JEVGdveVgwQU9lSVRCdUhVbVpGOHI3Y05wMWdUc2pGc2c3cGdnM084WTBudGRxSjNXSzljejRNS3RkUy1OaUVrNDlEdldCbVczaEhhLXpkSGM2UGQwdnRVNWMyNmJldmhOc0FHVWpKdll6SndPZHV2YVJfV0dRYW84cUhzeHVwa1hXZjZtOHA4TlRJQnkzeWhzVGFyZlZxUjJNSTJUQ3FzbDBuRDB5eUNibDBLbjhjNWRYWnQ5a29GczFwTVYyc05VbXlhQ2dZS0FYb1NBUkVTRlFIR1gyTWk0ZHJXY2hQdE9VZzZSWG1hb2FCd1JnMDIwNyIsICJyZWZyZXNoX3Rva2VuIjogIjEvLzBoZDYtUklzcWU2WDJDZ1lJQVJBQUdCRVNOd0YtTDlJclY3cFZMUmNNNWkwdWZfQnktT1JGYTFHWm9GdU43NGNEYnVxMEVValpILXBKT2tPYy1nQ1MyR2pJNkQwa0V1eURPN3ciLCAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dHgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwgImNsaWVudF9pZCI6ICI1MTAxMDEyMDgzNjEtbWkwaTk2NWQ4aWEzb2xtbzlsMWc0NnNmOWRuMjhlMWUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCAiY2xpZW50X3NlY3JldCI6ICJHT0NTUFgtLXVMMVNQdDdkUTltLWdVS0VqaGJGQWdJY3YzWiIsICJzY29wZXMiOiBbImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvc3ByZWFkc2hlZXRzIl0sICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20iLCAiYWNjb3VudCI6ICIiLCAiZXhwaXJ5IjogIjIwMjUtMDktMjJUMTk6MzE6MTguNjgwNDY2WiJ9

# CORS Configuration
CORS_ORIGINS=https://tu-proyecto.vercel.app
```

### 2.4 Configurar Railway para Python
1. Railway detectará automáticamente `requirements.txt`
2. Configurará el comando de inicio: `uvicorn api:app --host 0.0.0.0 --port $PORT`
3. El despliegue comenzará automáticamente

### 2.5 Obtener URL del Backend
1. Una vez desplegado, Railway te dará una URL como: `https://tu-proyecto-production.up.railway.app`
2. **Guarda esta URL** - la necesitarás para Vercel

## 🎯 Paso 3: Desplegar Frontend en Vercel

### 3.1 Conectar Repositorio a Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Inicia sesión con GitHub
3. Haz clic en "New Project"
4. Selecciona tu repositorio
5. Vercel detectará automáticamente que es un proyecto React

### 3.2 Configurar Variables de Entorno en Vercel
1. En la configuración del proyecto, ve a "Environment Variables"
2. Agrega la siguiente variable:

```bash
# API Configuration
REACT_APP_API_URL=https://tu-proyecto-production.up.railway.app
```

**⚠️ IMPORTANTE**: Reemplaza `https://tu-proyecto-production.up.railway.app` con la URL real de tu backend en Railway.

### 3.3 Configurar Build Settings
1. **Root Directory**: `frontend-react`
2. **Build Command**: `npm run build`
3. **Output Directory**: `build`
4. **Install Command**: `npm install`

### 3.4 Desplegar
1. Haz clic en "Deploy"
2. Vercel construirá y desplegará tu aplicación automáticamente
3. Te dará una URL como: `https://tu-proyecto.vercel.app`

## 🎯 Paso 4: Configurar CORS en el Backend

### 4.1 Actualizar CORS en Railway
1. Ve a tu proyecto en Railway
2. Ve a "Variables"
3. Agrega/actualiza:

```bash
CORS_ORIGINS=https://tu-proyecto.vercel.app
```

### 4.2 Reiniciar Backend
1. Railway detectará el cambio automáticamente
2. O puedes reiniciar manualmente desde el dashboard

## 🎯 Paso 5: Verificar Despliegue

### 5.1 Probar Frontend
1. Ve a tu URL de Vercel: `https://tu-proyecto.vercel.app`
2. Verifica que la aplicación cargue correctamente
3. Prueba subir una imagen y analizarla

### 5.2 Probar Backend
1. Ve a `https://tu-backend.railway.app/docs`
2. Deberías ver la documentación de la API
3. Prueba algunos endpoints

### 5.3 Verificar Integración
1. En el frontend, intenta analizar una imagen
2. Verifica que los datos se guarden en Google Sheets
3. Revisa el historial

## 🔧 Solución de Problemas

### Error: CORS
**Síntoma**: Error de CORS en el navegador
**Solución**: 
1. Verifica que `CORS_ORIGINS` en Railway incluya tu URL de Vercel
2. Reinicia el backend

### Error: Variables de Entorno
**Síntoma**: Error 500 en el backend
**Solución**:
1. Verifica que todas las variables estén configuradas en Railway
2. Revisa los logs en Railway

### Error: Build Fallido
**Síntoma**: Build falla en Vercel
**Solución**:
1. Verifica que `REACT_APP_API_URL` esté configurada
2. Revisa los logs de build en Vercel

## 📊 URLs Finales

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-backend.railway.app`
- **API Docs**: `https://tu-backend.railway.app/docs`

## 🎉 ¡Listo!

Tu aplicación estará disponible públicamente y otros usuarios podrán:
- ✅ Subir imágenes
- ✅ Analizar luz y sombra
- ✅ Ver historial
- ✅ Probar el modelo
- ✅ Exportar datos

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway y Vercel
2. Verifica las variables de entorno
3. Comprueba la configuración de CORS
4. Asegúrate de que las credenciales de Google Sheets sean válidas
