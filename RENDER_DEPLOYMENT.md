# 🚀 Despliegue en Render.com

## 📋 Pasos para Desplegar

### 1. Crear cuenta en Render
- Ve a [render.com](https://render.com)
- Regístrate con tu cuenta de GitHub

### 2. Conectar repositorio
- Haz clic en "New +"
- Selecciona "Web Service"
- Conecta tu repositorio: `JemnerVera/agricola-luz-sombra-supervisado`

### 3. Configurar el servicio
- **Name**: `agricola-luz-sombra-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`

### 4. Variables de entorno
Render ya tiene las variables configuradas en `render.yaml`:
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SHEETS_SHEET_NAME`
- `GOOGLE_SHEETS_CREDENTIALS_BASE64`
- `GOOGLE_SHEETS_TOKEN_BASE64`

### 5. Desplegar
- Haz clic en "Create Web Service"
- Espera 5-10 minutos para el build

## 🔧 Configurar Frontend

### 1. Actualizar URL de API
En `frontend-react/src/App.tsx`, cambiar:
```typescript
const API_URL = 'https://tu-backend.onrender.com';
```

### 2. Ejecutar frontend localmente
```bash
cd frontend-react
npm install
npm start
```

## ✅ Verificar funcionamiento

1. **Backend**: `https://tu-backend.onrender.com/docs`
2. **Frontend**: `http://localhost:3000`

## 🆘 Solución de problemas

- **Build lento**: Render puede tomar 10-15 minutos
- **Timeout**: El plan gratuito tiene limitaciones
- **OpenCV**: Render maneja mejor las dependencias del sistema
