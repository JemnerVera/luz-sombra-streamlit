# 📊 Configuración de Google Sheets

## 🔧 Pasos para configurar Google Sheets

### 1. **Crear proyecto en Google Cloud Console**

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita la **Google Sheets API**:
   - Ve a "APIs y servicios" > "Biblioteca"
   - Busca "Google Sheets API"
   - Haz clic en "Habilitar"

### 2. **Crear credenciales OAuth 2.0**

1. Ve a "APIs y servicios" > "Credenciales"
2. Haz clic en "Crear credenciales" > "ID de cliente OAuth 2.0"
3. Selecciona "Aplicación de escritorio"
4. Descarga el archivo JSON de credenciales
5. Renómbralo como `credentials.json` y colócalo en la raíz del proyecto

### 3. **Configurar la hoja de cálculo**

1. Crea una nueva hoja de cálculo en Google Sheets
2. Comparte la hoja con la cuenta de la empresa
3. Copia el ID de la hoja de cálculo de la URL:
   ```
   https://docs.google.com/spreadsheets/d/[ID_DE_LA_HOJA]/edit
   ```
4. Actualiza el archivo `google_sheets_config.json` con el ID

### 4. **Estructura de la hoja de cálculo**

La hoja debe tener estas columnas:
- A: ID
- B: Fecha
- C: Hora
- D: Imagen
- E: Fundo
- F: Sector
- G: Hilera
- H: Latitud
- I: Longitud
- J: Porcentaje Luz
- K: Porcentaje Sombra
- L: Dispositivo
- M: Software
- N: Dirección
- O: Timestamp

### 5. **Probar la conexión**

Ejecuta el script de prueba:
```bash
python src/google_sheets/sheets_client.py
```

## 📋 Archivos necesarios

- `credentials.json` - Credenciales de Google Cloud (descargar)
- `google_sheets_config.json` - Configuración de la hoja
- `token.json` - Token de autenticación (se genera automáticamente)

## 🔒 Permisos necesarios

La cuenta de la empresa debe tener:
- Acceso a Google Sheets
- Permisos para crear y editar hojas de cálculo
- Acceso a Google Cloud Console (para crear credenciales)
