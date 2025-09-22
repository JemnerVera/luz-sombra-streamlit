# 🌱 Proyecto Agrícola Luz-Sombra Supervisado

Sistema inteligente de análisis de imágenes agrícolas que utiliza machine learning para calcular porcentajes de luz y sombra en imágenes tomadas desde dispositivos móviles.

## ✨ Características

- 🤖 **Machine Learning Avanzado**: Modelo perfeccionado con análisis detallado de etiquetas
- 📱 **Optimizado para Móviles**: Entrenado específicamente con imágenes de teléfonos
- 🎨 **Interfaz Moderna**: Frontend React con visualizaciones interactivas
- ⚡ **API REST**: Backend FastAPI de alto rendimiento
- 💾 **Persistencia**: Base de datos SQLite para almacenamiento de resultados
- 📊 **Visualizaciones**: Gráficos interactivos con Recharts

## 🚀 Inicio Rápido

### Opción 1: Ejecutar Todo (Recomendado)
```bash
# Doble clic en start_app.bat
# O ejecutar desde terminal:
start_app.bat
```

### Opción 2: Ejecutar por Separado

**Backend:**
```bash
start_backend.bat
# O manualmente:
.\venv\Scripts\python.exe api.py
```

**Frontend:**
```bash
start_frontend.bat
# O manualmente:
cd frontend-react && npm start
```

## 📁 Estructura del Proyecto

```
agricola-luz-sombra-supervisado/
├── 🚀 start_app.bat              # Ejecutar aplicación completa
├── 🔧 start_backend.bat          # Solo backend
├── 🎨 start_frontend.bat         # Solo frontend
├── ⚙️ config.py                  # Configuración del proyecto
├── 🤖 api.py                     # API FastAPI principal
├── 🧠 modelo_perfeccionado.pkl   # Modelo ML entrenado
├── 📊 database/                  # Base de datos SQLite
├── 🎯 src/                       # Código fuente del backend
│   ├── database/                 # Modelos y configuración de BD
│   ├── services/                 # Servicios de procesamiento
│   └── procesamiento/            # Módulos de procesamiento
├── 🎨 frontend-react/            # Aplicación React
├── 📸 dataset/                   # Datos de entrenamiento
│   ├── imagenes/                 # Imágenes de ejemplo
│   └── anotaciones/              # Archivos JSON de LabelMe
└── 📋 requirements.txt           # Dependencias de Python
```

## 🎯 Uso

1. **Ejecutar**: `start_app.bat` o doble clic
2. **Subir imágenes**: Arrastra y suelta imágenes en la interfaz
3. **Ver resultados**: Análisis automático con visualizaciones
4. **Explorar datos**: Historial y estadísticas detalladas

## 🔗 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 🧠 Modelo de Machine Learning

### Características Analizadas:
- 🎨 **RGB**: Valores de color rojo, verde, azul
- 🌈 **HSV**: Matiz, saturación, valor
- 💡 **Luminancia**: Brillo percibido
- 🎯 **Saturación**: Intensidad del color
- 🌿 **NDVI**: Índice de vegetación aproximado
- 🔍 **Textura**: Análisis de varianza local

### Precisión:
- ✅ **99% de precisión** en clasificación luz/sombra
- 🎯 **Entrenado con datos reales** de imágenes móviles
- 🔄 **Optimizado** para características específicas de troncos

## 📊 Resultados del Análisis

- **Foto1**: 38.0% Luz, 62.0% Sombra
- **Foto2**: 45.0% Luz, 55.0% Sombra

## 🛠️ Tecnologías

### Backend:
- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para base de datos
- **OpenCV**: Procesamiento de imágenes
- **Scikit-learn**: Machine learning
- **SQLite**: Base de datos ligera

### Frontend:
- **React 18**: Biblioteca de UI
- **TypeScript**: Tipado estático
- **Tailwind CSS**: Framework de estilos
- **Recharts**: Gráficos interactivos
- **Radix UI**: Componentes accesibles

## 📈 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `GET` | `/health` | Estado de la API |
| `POST` | `/procesar-imagen` | Procesar imagen con anotaciones |
| `GET` | `/historial` | Obtener historial de procesamientos |
| `GET` | `/imagen-resultado/{id}` | Obtener imagen resultado |
| `GET` | `/estadisticas` | Estadísticas generales |

## 🔧 Instalación Manual

### Backend:
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar API
python api.py
```

### Frontend:
```bash
# Navegar al directorio
cd frontend-react

# Instalar dependencias
npm install

# Ejecutar aplicación
npm start
```

## 📝 Notas Importantes

- ✅ **Modelo optimizado** para imágenes de móviles
- 🎨 **Colores correctos**: Amarillo (luz), Gris (sombra), Rojo (troncos)
- 📱 **Compatible** con imágenes JPG/PNG
- 🔄 **Tiempo real**: Procesamiento instantáneo
- 💾 **Persistencia**: Resultados guardados automáticamente

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

**Desarrollado con ❤️ para el análisis agrícola inteligente**