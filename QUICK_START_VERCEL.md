# ⚡ Guía Rápida: Vercel en 15 Minutos

## 🎯 Resumen Ejecutivo

**Objetivo**: Desplegar tu aplicación agrícola en Vercel para que otros usuarios puedan usarla.

**Tiempo estimado**: 15-20 minutos

**Resultado**: App pública en `https://tu-proyecto.vercel.app`

## 🚀 Pasos Rápidos

### 1️⃣ Preparar Credenciales (2 min)
```bash
# Ejecutar script
venv\Scripts\python prepare_vercel_credentials.py

# Copiar variables del archivo vercel_env_vars.txt
```

### 2️⃣ Railway Backend (5 min)
1. Ve a [railway.app](https://railway.app) → New Project
2. Conecta tu repositorio de GitHub
3. Ve a Variables → Agrega:
   - `GOOGLE_SHEETS_SPREADSHEET_ID`
   - `GOOGLE_SHEETS_SHEET_NAME`
   - `GOOGLE_SHEETS_CREDENTIALS_BASE64`
   - `GOOGLE_SHEETS_TOKEN_BASE64`
4. **Guarda la URL del backend** (ej: `https://tu-proyecto-production.up.railway.app`)

### 3️⃣ Vercel Frontend (5 min)
1. Ve a [vercel.com](https://vercel.com) → New Project
2. Conecta tu repositorio de GitHub
3. Configura:
   - **Root Directory**: `frontend-react`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. Variables de entorno:
   - `REACT_APP_API_URL` = URL del backend de Railway
5. Deploy

### 4️⃣ CORS (2 min)
1. En Railway → Variables
2. Agrega: `CORS_ORIGINS` = URL de Vercel
3. Reinicia backend

### 5️⃣ Verificar (1 min)
1. Ve a tu URL de Vercel
2. Prueba subir una imagen
3. ¡Listo! 🎉

## 📋 Variables de Entorno

### Railway (Backend)
```bash
GOOGLE_SHEETS_SPREADSHEET_ID=1H3oobEJdidbJ2S7Ms3nW0ZbSR-yKiZHQNZp2pubXIU4
GOOGLE_SHEETS_SHEET_NAME=Data-app
GOOGLE_SHEETS_CREDENTIALS_BASE64=eyJpbnN0YWxsZWQiOnsiY2xpZW50X2lkIjoiNTEwMTAxMjA4MzYxLW1pMGk5NjVkOGlhM29sbW85bDFnNDZzZjlkbjI4ZTFlLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwicHJvamVjdF9pZCI6ImFwcC1sdXotc29tYnJhIiwiYXV0aF91cmkiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsInRva2VuX3VyaSI6Imh0dHBzOi8vb2F1dHgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjoiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dHgyL3YxL2NlcnRzIiwiY2xpZW50X3NlY3JldCI6IkdPQ1NQWC0tdUwxU1B0N2RROW0tZ1VLRWpoYkZBZ0ljdjNaIiwicmVkaXJlY3RfdXJpcyI6WyJodHRwOi8vbG9jYWxob3N0Il19fQ==
GOOGLE_SHEETS_TOKEN_BASE64=eyJ0b2tlbiI6ICJ5YTI5LmEwQVFRX0JEVGdveVgwQU9lSVRCdUhVbVpGOHI3Y05wMWdUc2pGc2c3cGdnM084WTBudGRxSjNXSzljejRNS3RkUy1OaUVrNDlEdldCbVczaEhhLXpkSGM2UGQwdnRVNWMyNmJldmhOc0FHVWpKdll6SndPZHV2YVJfV0dRYW84cUhzeHVwa1hXZjZtOHA4TlRJQnkzeWhzVGFyZlZxUjJNSTJUQ3FzbDBuRDB5eUNibDBLbjhjNWRYWnQ5a29GczFwTVYyc05VbXlhQ2dZS0FYb1NBUkVTRlFIR1gyTWk0ZHJXY2hQdE9VZzZSWG1hb2FCd1JnMDIwNyIsICJyZWZyZXNoX3Rva2VuIjogIjEvLzBoZDYtUklzcWU2WDJDZ1lJQVJBQUdCRVNOd0YtTDlJclY3cFZMUmNNNWkwdWZfQnktT1JGYTFHWm9GdU43NGNEYnVxMEVValpILXBKT2tPYy1nQ1MyR2pJNkQwa0V1eURPN3ciLCAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dHgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwgImNsaWVudF9pZCI6ICI1MTAxMDEyMDgzNjEtbWkwaTk2NWQ4aWEzb2xtbzlsMWc0NnNmOWRuMjhlMWUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCAiY2xpZW50X3NlY3JldCI6ICJHT0NTUFgtLXVMMVNQdDdkUTltLWdVS0VqaGJGQWdJY3YzWiIsICJzY29wZXMiOiBbImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvc3ByZWFkc2hlZXRzIl0sICJ1bml2ZXJzZV9kb21haW4iOiAiZ29vZ2xlYXBpcy5jb20iLCAiYWNjb3VudCI6ICIiLCAiZXhwaXJ5IjogIjIwMjUtMDktMjJUMTk6MzE6MTguNjgwNDY2WiJ9
CORS_ORIGINS=https://tu-proyecto.vercel.app
```

### Vercel (Frontend)
```bash
REACT_APP_API_URL=https://tu-proyecto-production.up.railway.app
```

## 🚨 Troubleshooting Rápido

### ❌ CORS Error
**Solución**: Verificar `CORS_ORIGINS` en Railway = URL exacta de Vercel

### ❌ 500 Error
**Solución**: Revisar variables de entorno en Railway

### ❌ Build Fallido
**Solución**: Verificar `REACT_APP_API_URL` en Vercel

## 📊 URLs Finales

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-backend.railway.app`
- **API Docs**: `https://tu-backend.railway.app/docs`

## 🎉 ¡Listo!

Tu aplicación estará disponible públicamente y otros usuarios podrán:
- ✅ Subir y analizar imágenes
- ✅ Ver historial
- ✅ Probar el modelo
- ✅ Exportar datos

**¡En 15 minutos tendrás tu app en producción!** 🚀
