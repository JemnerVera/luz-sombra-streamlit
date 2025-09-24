# Cambios Pendientes para Implementar

## Resumen
Este documento describe las funcionalidades que se implementaron durante el desarrollo pero que fueron revertidas para mantener una versión estable. Estas funcionalidades deben ser implementadas nuevamente de manera cuidadosa.

## 1. Mejoras de Diseño UI/UX

### 1.1 Layout de Imágenes Subidas
- **Problema**: Container vacío entre el nombre del archivo y los campos de entrada
- **Solución**: Refactorizar el layout usando `st.container()` y `st.columns()` para un diseño más compacto
- **Ubicación**: Sección de "📸 Imágenes Subidas" en `streamlit_app.py`

### 1.2 Información Extraída
- **Eliminar**: Texto "🔍 Info extraída: Hilera: 114, Planta: 22"
- **Razón**: La información se extrae automáticamente, no necesita mostrarse

### 1.3 Indicador GPS
- **Implementar**: Badge "❌ Sin GPS" en container rojo con letras blancas
- **Posición**: Misma fila que el botón "Ver", más cerca del nombre de la imagen
- **Funcionalidad**: Mostrar "📍 GPS: lat, lon" si hay datos GPS disponibles

### 1.4 Botón "Ver"
- **Problema**: Aparecía con letras verticales
- **Solución**: Ajustar proporciones de columnas de `st.columns([2, 1])` a `st.columns([1, 1])`

### 1.5 Líneas Separadoras
- **Agregar**: Línea horizontal (`---`) arriba de "📸 Imágenes Subidas"
- **Eliminar**: Línea duplicada después del mensaje de guardado

## 2. Funcionalidad de Guardado en Google Drive

### 2.1 Opciones de Guardado
- **Implementar**: Sección "💾 Opciones de Guardado" con dos checkboxes:
  - "📊 Guardar en Histórico" (por defecto: ✅)
  - "📋 Guardar Aparte (Nueva Google Sheet)" (por defecto: ❌)
- **Validación**: Al menos una opción debe estar seleccionada

### 2.2 Creación de Nueva Hoja de Cálculo
- **Funcionalidad**: Crear una nueva Google Sheet para cada batch de imágenes
- **Ubicación**: Carpeta específica en Google Drive (`1rwsV0tZOUDxhBXwU2DHA1WxhU7aQXpvu`)
- **Nombre**: Basado en fecha y hora del batch
- **Configuración**: 19 columnas con encabezados apropiados

### 2.3 Integración con Google Drive API
- **Scope adicional**: `https://www.googleapis.com/auth/drive`
- **Service Account**: Configurar permisos para crear archivos en Shared Drives
- **Parámetros**: Usar `supportsAllDrives=True` en todas las llamadas a la API

## 3. Extracción Automática de Información

### 3.1 Función de Extracción de Nombre de Archivo
```python
def extract_info_from_filename(filename):
    """
    Extrae información de Hilera y Planta del nombre del archivo
    Formato esperado: H###_P### o similar
    """
    import re
    # Patrón para extraer H### y P###
    pattern = r'H(\d+).*?P(\d+)'
    match = re.search(pattern, filename, re.IGNORECASE)
    
    if match:
        hilera = match.group(1)
        planta = match.group(2)
        return hilera, planta
    return None, None
```

### 3.2 Pre-llenado Automático
- **Implementar**: Extracción automática al subir imágenes
- **Campos**: Pre-llenar "Hilera" y "N° Planta" basado en el nombre del archivo
- **Ejemplo**: `E07_92_H122_P22.jpg` → Hilera: 122, Planta: 22

## 4. Funcionalidad GPS/EXIF

### 4.1 Función de Extracción GPS
```python
def extract_gps_info(image_bytes):
    """
    Extrae información GPS de los metadatos EXIF de la imagen
    """
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    import io
    
    try:
        image = Image.open(io.BytesIO(image_bytes))
        exifdata = image.getexif()
        
        # Buscar datos GPS
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_data = exifdata[tag_id]
                # Procesar datos GPS...
                return True, latitude, longitude
        
        return False, None, None
    except Exception as e:
        return False, None, None
```

### 4.2 Lógica Condicional de Campos
- **Con GPS**: Deshabilitar campos "Hilera" y "N° Planta", mostrar coordenadas
- **Sin GPS**: Habilitar campos para entrada manual, mostrar badge "Sin GPS"

### 4.3 Integración con Guardado
- **Agregar**: Columnas "Latitud" y "Longitud" en el guardado de datos
- **Mapeo**: Incluir coordenadas GPS en el registro de Google Sheets

## 5. Botón "Subir más fotos"

### 5.1 Funcionalidad
- **Ubicación**: Al final de los resultados del análisis
- **Acción**: Limpiar toda la sesión y preparar para nuevas subidas
- **Limpieza**: Eliminar archivos subidos, campos llenos, y datos de sesión

### 5.2 Implementación
```python
if st.button("📸 Subir más fotos", type="primary", use_container_width=True):
    # Limpiar todos los datos de la sesión
    keys_to_clear = [
        'uploaded_files', 'empresa', 'fundo', 'sector', 'lote',
        'guardar_historico', 'guardar_aparte', 'hilera_values', 
        'planta_values', 'gps_info_values'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
```

## 6. Eliminaciones de UI

### 6.1 Elementos a Remover
- **Botón**: "Extraer Info Automáticamente" (ya es automático)
- **Resumen**: "Opciones seleccionadas" después de los checkboxes
- **Estadísticas**: "Total registros", "Luz promedio", "Sombra promedio" del historial

## 7. Consideraciones Técnicas

### 7.1 Manejo de Errores
- **OpenCV**: Validación robusta de bytes de imagen y decodificación
- **Google Drive**: Manejo de permisos y errores de creación de archivos
- **EXIF**: Manejo de imágenes sin metadatos GPS

### 7.2 Optimización de Lectura de Archivos
- **Problema**: `uploaded_file.read()` se llamaba múltiples veces
- **Solución**: Leer una vez y almacenar en `st.session_state`
- **Implementación**: `st.session_state[f"image_bytes_{i}"] = image_bytes`

### 7.3 Compatibilidad de Streamlit
- **Problema**: `st.dialog()` y `st.modal()` no compatibles con la versión actual
- **Solución**: Usar `st.warning()` y `st.error()` con botones para validaciones

## 8. Orden de Implementación Recomendado

1. **Primero**: Mejoras de diseño UI/UX (sección 1)
2. **Segundo**: Extracción automática de información (sección 3)
3. **Tercero**: Funcionalidad GPS/EXIF (sección 4)
4. **Cuarto**: Botón "Subir más fotos" (sección 5)
5. **Quinto**: Funcionalidad de Google Drive (sección 2)
6. **Último**: Eliminaciones de UI (sección 6)

## 9. Archivos Principales a Modificar

- `streamlit_app.py`: Funcionalidad principal y UI
- `src/google_sheets/sheets_client.py`: Integración con Google Drive API
- `requirements.txt`: Dependencias adicionales si es necesario

## 10. Testing

- **Local**: Probar cada funcionalidad individualmente
- **Google Drive**: Verificar permisos y creación de archivos
- **GPS**: Probar con imágenes que tengan y no tengan metadatos GPS
- **UI**: Verificar que el diseño se vea correcto en diferentes tamaños de pantalla
