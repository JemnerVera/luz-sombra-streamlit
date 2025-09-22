# 🚀 Guía de Despliegue en Vercel

## 📋 Configuración Inicial

### 1. Variables de Entorno en Vercel

Configura las siguientes variables de entorno en tu proyecto de Vercel:

```bash
# Google Sheets Configuration
GOOGLE_SHEETS_SPREADSHEET_ID=tu_spreadsheet_id_aqui
GOOGLE_SHEETS_SHEET_NAME=Data-app

# Google Sheets Credentials (Base64 encoded)
GOOGLE_SHEETS_CREDENTIALS_BASE64=tu_credenciales_base64_aqui
GOOGLE_SHEETS_TOKEN_BASE64=tu_token_base64_aqui
```

### 2. Preparar Credenciales

#### Opción A: Usar Base64 (Recomendado)
```bash
# Convertir credentials.json a Base64
base64 -i credentials.json -o credentials_base64.txt

# Convertir token.json a Base64
base64 -i token.json -o token_base64.txt
```

#### Opción B: Usar Variables de Entorno Directas
```bash
# Copiar el contenido de credentials.json
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}

# Copiar el contenido de token.json
GOOGLE_SHEETS_TOKEN={"token":"ya29.a0AfH6SMC...",...}
```

### 3. Configurar en Vercel

1. Ve a tu proyecto en Vercel Dashboard
2. Ve a Settings > Environment Variables
3. Agrega las variables de entorno
4. Asegúrate de que estén disponibles en Production

## 🔧 Modificaciones Necesarias para Vercel

### Backend (api.py)
- El backend necesita ser desplegado por separado (Railway, Render, etc.)
- O usar Vercel Functions para endpoints específicos

### Frontend (React)
- Se despliega automáticamente en Vercel
- Configurar variables de entorno para la API

## 📁 Estructura de Archivos

```
├── frontend-react/          # React app (se despliega en Vercel)
├── api.py                   # Backend (desplegar por separado)
├── src/                     # Código Python
├── google_sheets_config.example.json
└── VERCEL_DEPLOYMENT.md
```

## ⚠️ Seguridad

- ✅ `credentials.json` está en .gitignore
- ✅ `token.json` está en .gitignore
- ✅ `google_sheets_config.json` está en .gitignore
- ✅ Usar variables de entorno para credenciales
- ✅ No hardcodear credenciales en el código

## 🚀 Pasos para Desplegar

1. **Preparar credenciales** (ver sección 2)
2. **Configurar variables de entorno** en Vercel
3. **Conectar repositorio** a Vercel
4. **Desplegar frontend** automáticamente
5. **Desplegar backend** por separado
6. **Configurar CORS** entre frontend y backend

## 🔗 URLs de Producción

- **Frontend**: `https://tu-proyecto.vercel.app`
- **Backend**: `https://tu-backend.railway.app` (ejemplo)

## 📞 Soporte

Si tienes problemas con el despliegue, revisa:
1. Variables de entorno configuradas correctamente
2. CORS configurado en el backend
3. URLs de API actualizadas en el frontend
