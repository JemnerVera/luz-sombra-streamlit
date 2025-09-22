# ✅ Checklist de Despliegue en Vercel

## 📋 Preparación

### ✅ Credenciales
- [ ] Ejecutar `venv\Scripts\python prepare_vercel_credentials.py`
- [ ] Copiar variables de entorno del archivo `vercel_env_vars.txt`
- [ ] Verificar que `credentials.json` y `token.json` existan
- [ ] Confirmar que `google_sheets_config.json` tenga el spreadsheet_id correcto

### ✅ Repositorio
- [ ] Hacer push de todos los cambios a GitHub
- [ ] Verificar que `.gitignore` excluya archivos sensibles
- [ ] Confirmar que el repositorio sea público o que tengas acceso

## 🚂 Railway (Backend)

### ✅ Cuenta y Proyecto
- [ ] Crear cuenta en [railway.app](https://railway.app)
- [ ] Conectar con GitHub
- [ ] Crear nuevo proyecto
- [ ] Seleccionar repositorio

### ✅ Variables de Entorno
- [ ] `GOOGLE_SHEETS_SPREADSHEET_ID`
- [ ] `GOOGLE_SHEETS_SHEET_NAME`
- [ ] `GOOGLE_SHEETS_CREDENTIALS_BASE64`
- [ ] `GOOGLE_SHEETS_TOKEN_BASE64`
- [ ] `CORS_ORIGINS` (se actualizará después)

### ✅ Despliegue
- [ ] Railway detecta automáticamente Python
- [ ] Build exitoso
- [ ] Obtener URL del backend
- [ ] Probar endpoint `/docs`

## ⚡ Vercel (Frontend)

### ✅ Cuenta y Proyecto
- [ ] Crear cuenta en [vercel.com](https://vercel.com)
- [ ] Conectar con GitHub
- [ ] Crear nuevo proyecto
- [ ] Seleccionar repositorio

### ✅ Configuración
- [ ] Root Directory: `frontend-react`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `build`
- [ ] Install Command: `npm install`

### ✅ Variables de Entorno
- [ ] `REACT_APP_API_URL` = URL del backend de Railway

### ✅ Despliegue
- [ ] Build exitoso
- [ ] Obtener URL del frontend
- [ ] Probar que la app cargue

## 🔗 Integración

### ✅ CORS
- [ ] Actualizar `CORS_ORIGINS` en Railway con URL de Vercel
- [ ] Reiniciar backend en Railway
- [ ] Verificar que no hay errores de CORS

### ✅ Funcionalidad
- [ ] Subir imagen en el frontend
- [ ] Analizar imagen
- [ ] Verificar que se guarde en Google Sheets
- [ ] Revisar historial
- [ ] Probar "Probar Modelo"

## 🧪 Testing

### ✅ Frontend
- [ ] Carga correctamente
- [ ] Dropdowns funcionan
- [ ] Subida de imágenes funciona
- [ ] Modales aparecen correctamente
- [ ] Tabla de historial se ve bien

### ✅ Backend
- [ ] API responde correctamente
- [ ] Documentación en `/docs` accesible
- [ ] Endpoints funcionan
- [ ] Google Sheets se actualiza

### ✅ Integración Completa
- [ ] Análisis de imagen completo funciona
- [ ] Datos se guardan correctamente
- [ ] Historial se actualiza
- [ ] Exportación CSV funciona

## 🚨 Problemas Comunes

### ❌ CORS Error
**Síntoma**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`
**Solución**: 
- [ ] Verificar `CORS_ORIGINS` en Railway
- [ ] Reiniciar backend
- [ ] Verificar URLs exactas

### ❌ 500 Error en Backend
**Síntoma**: Error 500 al hacer requests
**Solución**:
- [ ] Revisar logs en Railway
- [ ] Verificar variables de entorno
- [ ] Comprobar credenciales de Google Sheets

### ❌ Build Fallido en Vercel
**Síntoma**: Build falla durante deployment
**Solución**:
- [ ] Verificar `REACT_APP_API_URL` está configurada
- [ ] Revisar logs de build
- [ ] Verificar que `frontend-react` sea el root directory

### ❌ Variables de Entorno No Funcionan
**Síntoma**: App usa localhost en lugar de Railway
**Solución**:
- [ ] Verificar que variables estén en Production
- [ ] Reiniciar deployment
- [ ] Verificar nombres exactos de variables

## 📊 URLs Finales

### ✅ Documentar URLs
- [ ] Frontend: `https://tu-proyecto.vercel.app`
- [ ] Backend: `https://tu-backend.railway.app`
- [ ] API Docs: `https://tu-backend.railway.app/docs`

### ✅ Compartir
- [ ] Enviar URL del frontend a usuarios
- [ ] Documentar URLs en README
- [ ] Crear bookmark para acceso rápido

## 🎉 ¡Completado!

### ✅ Verificación Final
- [ ] App funciona completamente
- [ ] Otros usuarios pueden acceder
- [ ] Todas las funcionalidades operativas
- [ ] Datos se guardan correctamente
- [ ] Performance aceptable

### ✅ Documentación
- [ ] URLs documentadas
- [ ] Instrucciones para usuarios
- [ ] Troubleshooting guide
- [ ] Backup de configuración

---

## 📞 Soporte

Si algo no funciona:
1. **Revisar logs** en Railway y Vercel
2. **Verificar variables** de entorno
3. **Comprobar CORS** configuration
4. **Testear endpoints** individualmente
5. **Revisar credenciales** de Google Sheets

**¡Tu aplicación estará lista para que otros usuarios la usen!** 🚀
