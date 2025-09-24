import streamlit as st
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
from datetime import datetime
import json
import os
import requests
import gc  # Para limpieza de memoria

# Configuración de página
st.set_page_config(
    page_title="Análisis Agrícola Luz-Sombra",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para descargar modelo si no existe
@st.cache_data
def download_model_if_needed():
    """Descarga el modelo si no existe localmente"""
    model_path = "modelo_perfeccionado.pkl"
    
    if not os.path.exists(model_path):
        st.warning("⚠️ Modelo no encontrado localmente. Necesitas subirlo manualmente.")
        st.info("""
        **Para usar la aplicación:**
        1. Descarga `modelo_perfeccionado.pkl` desde tu repositorio local
        2. Súbelo a la raíz del proyecto
        3. O configura la URL de descarga en secrets
        """)
        return False
    return True

# Verificar si el modelo existe
model_available = download_model_if_needed()

# CSS personalizado para replicar la interfaz actual
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #22c55e;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        margin: 0.5rem 0;
    }
    
    .file-row {
        background-color: transparent !important;
        padding: 0.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
        display: block;
    }
    
    .file-row .stColumns {
        background-color: transparent !important;
    }
    
    .file-row .stTextInput {
        background-color: transparent !important;
    }
    
    .file-row .stButton {
        background-color: transparent !important;
    }
    
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 0.375rem;
        padding: 0.5rem;
        font-size: 0.875rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
        background-color: white !important;
    }
    
    .stButton > button {
        background-color: #22c55e;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #16a34a;
    }
    
    .view-button {
        background-color: #3b82f6 !important;
    }
    
    .view-button:hover {
        background-color: #2563eb !important;
    }
    
    .crop-button {
        background-color: #f59e0b !important;
    }
    
    .crop-button:hover {
        background-color: #d97706 !important;
    }
    
    .upload-area {
        border: 2px dashed #22c55e;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        background-color: #0f172a;
    }
    
    .result-card {
        background-color: #1e293b;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        margin: 1rem 0;
    }
    
    .file-row {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar datos reales de Google Sheets
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_dropdown_data():
    """Cargar datos reales de Google Sheets"""
    try:
        # Importar el cliente de Google Sheets
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from google_sheets.sheets_client import GoogleSheetsClient
        
        # Inicializar cliente
        client = GoogleSheetsClient()
        
        # Cargar datos de la hoja "Data-campo"
        empresas = client.get_column_data('Data-campo', 'B')[1:]  # Columna B, sin header
        fundos = client.get_column_data('Data-campo', 'D')[1:]    # Columna D, sin header
        sectores = client.get_column_data('Data-campo', 'G')[1:]  # Columna G, sin header
        lotes = client.get_column_data('Data-campo', 'I')[1:]     # Columna I, sin header
        
        # Filtrar valores únicos y no vacíos
        empresas = list(set([emp for emp in empresas if emp and emp.strip()]))
        fundos = list(set([fun for fun in fundos if fun and fun.strip()]))
        sectores = list(set([sec for sec in sectores if sec and sec.strip()]))
        lotes = list(set([lot for lot in lotes if lot and lot.strip()]))
        
        # Ordenar alfabéticamente
        empresas.sort()
        fundos.sort()
        sectores.sort()
        lotes.sort()
        
        return {
            'empresas': empresas,
            'fundos': fundos,
            'sectores': sectores,
            'lotes': lotes
        }
        
    except Exception as e:
        st.error(f"Error cargando datos de Google Sheets: {str(e)}")
        # Fallback a datos simulados
        return {
            'empresas': ['Empresa A', 'Empresa B', 'Empresa C'],
            'fundos': ['Fundo 1', 'Fundo 2', 'Fundo 3'],
            'sectores': ['Sector A', 'Sector B', 'Sector C'],
            'lotes': ['Lote 1', 'Lote 2', 'Lote 3']
        }

# Función para cargar todos los datos de la hoja con cache
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_sheet_data():
    """Cargar todos los datos de la hoja Data-campo"""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from google_sheets.sheets_client import GoogleSheetsClient
        
        client = GoogleSheetsClient()
        return client.get_sheet_data('Data-campo')
        
    except Exception as e:
        print(f"Error cargando datos de hoja: {e}")
        return []

# Función para análisis de imagen con modelo Random Forest original
def analizar_imagen_ml(image_bytes):
    """Analizar imagen usando el modelo Random Forest original"""
    try:
        # Verificar si el modelo está disponible
        if not model_available:
            st.error("❌ Modelo no disponible. Por favor, sube el archivo modelo_perfeccionado.pkl")
            return None
            
        # Importar el servicio de procesamiento original
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from services.procesamiento_service_v2 import ProcesamientoServiceV2
        
        # Crear instancia del servicio
        servicio = ProcesamientoServiceV2("modelo_perfeccionado.pkl")
        
        # Convertir bytes a imagen OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Optimización para imágenes grandes: redimensionar si es necesario
        original_height, original_width = img.shape[:2]
        max_dimension = 2048  # Máximo 2048px en cualquier dimensión
        
        if original_height > max_dimension or original_width > max_dimension:
            # Calcular factor de escala
            scale_factor = min(max_dimension / original_height, max_dimension / original_width)
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            
            # Redimensionar imagen
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            st.info(f"📏 Imagen redimensionada de {original_width}x{original_height} a {new_width}x{new_height} para optimizar memoria")
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Procesar imagen con el modelo original
        light_percentage, shadow_percentage, light_mask = servicio.procesar_imagen_visual(img_rgb)
        
        # Crear imagen de análisis visual
        analysis_img = img_rgb.copy()
        # Aplicar colores
        analysis_img[light_mask == 128] = [50, 50, 50]  # Gris oscuro para sombra
        analysis_img[light_mask == 255] = [255, 255, 0]  # Amarillo para luz
        
        result = {
            'light_percentage': light_percentage,
            'shadow_percentage': shadow_percentage,
            'analysis_image': analysis_img,
            'original_image': img_rgb,
            'processing_time': 0
        }
        
        # Limpiar variables grandes de memoria
        del img, img_rgb, nparr
        if 'light_mask' in locals():
            del light_mask
        if 'analysis_img' in locals():
            del analysis_img
        
        # Forzar limpieza de memoria
        gc.collect()
            
        return result
        
    except Exception as e:
        st.error(f"Error en análisis ML: {str(e)}")
        # Limpiar memoria en caso de error
        if 'img' in locals():
            del img
        if 'img_rgb' in locals():
            del img_rgb
        if 'nparr' in locals():
            del nparr
        gc.collect()
        return None

# Función para extraer información del nombre del archivo
def extract_info_from_filename(filename):
    """
    Extrae información de Hilera y Planta del nombre del archivo
    Formato esperado: H###_P### o similar
    Ejemplo: E07_92_H122_P22.jpg -> Hilera: 122, Planta: 22
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

# Función para mostrar resultados
def mostrar_resultados(resultado, nombre_archivo, mostrar_imagenes=False):
    """Mostrar resultados del análisis"""
    if resultado:
        if mostrar_imagenes:
            # Mostrar comparación de imágenes
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📸 Imagen Original")
                st.image(resultado['original_image'], use_container_width=True)
            
            with col2:
                st.subheader("🔍 Análisis del Modelo")
                st.image(resultado['analysis_image'], use_container_width=True)
        
        # Métricas
        col_light, col_shadow = st.columns(2)
        with col_light:
            st.metric("Luz detectada", f"{resultado['light_percentage']:.1f}%")
        with col_shadow:
            st.metric("Sombra detectada", f"{resultado['shadow_percentage']:.1f}%")
        
        st.info(f"📁 Archivo: {nombre_archivo}")

# Sidebar
st.sidebar.title("🌱 Análisis Agrícola")
st.sidebar.markdown("---")

# Navegación
page = st.sidebar.radio(
    "Navegación",
    ["Analizar Imágenes", "Probar Modelo", "Historial"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Versión 2.0**")

# Cargar datos para dropdowns
dropdown_data = load_dropdown_data()

# Página principal
if page == "Analizar Imágenes":
    st.markdown('<h1 class="main-header">📸 Analizar Imágenes</h1>', unsafe_allow_html=True)
    
    # Formulario con dropdowns y filtro cascada en una sola fila
    st.subheader("📋 Información del Campo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        empresa = st.selectbox("Empresa *", [""] + dropdown_data['empresas'], index=0)
    
    with col2:
        # Filtrar fundos por empresa seleccionada
        if empresa:
            # Obtener todos los datos de la hoja (con cache)
            all_data = load_sheet_data()
            
            # Filtrar fundos por empresa
            filtered_fundos = []
            if all_data:
                for row in all_data[1:]:  # Saltar header
                    if len(row) > 1 and row[1] == empresa:  # Columna B (índice 1)
                        if len(row) > 3 and row[3]:  # Columna D (índice 3)
                            filtered_fundos.append(row[3])
            
            # Eliminar duplicados y ordenar
            filtered_fundos = sorted(list(set(filtered_fundos)))
            
            if filtered_fundos:
                fundo = st.selectbox("Fundo *", [""] + filtered_fundos, index=0)
            else:
                st.warning("⚠️ No hay fundos disponibles para esta empresa")
                fundo = None
        else:
            fundo = st.selectbox("Fundo *", [""] + dropdown_data['fundos'], index=0)
    
    with col3:
        # Filtrar sectores por fundo seleccionado
        if fundo:
            # Obtener todos los datos de la hoja (con cache)
            all_data = load_sheet_data()
            
            # Filtrar sectores por fundo
            filtered_sectores = []
            if all_data:
                for row in all_data[1:]:  # Saltar header
                    if len(row) > 3 and row[3] == fundo:  # Columna D (índice 3)
                        if len(row) > 6 and row[6]:  # Columna G (índice 6)
                            filtered_sectores.append(row[6])
            
            # Eliminar duplicados y ordenar
            filtered_sectores = sorted(list(set(filtered_sectores)))
            
            if filtered_sectores:
                sector = st.selectbox("Sector *", [""] + filtered_sectores, index=0)
            else:
                st.warning("⚠️ No hay sectores disponibles para este fundo")
                sector = None
        else:
            sector = st.selectbox("Sector *", [""] + dropdown_data['sectores'], index=0)
    
    with col4:
        # Filtrar lotes por sector seleccionado
        if sector:
            # Obtener todos los datos de la hoja (con cache)
            all_data = load_sheet_data()
            
            # Filtrar lotes por sector
            filtered_lotes = []
            if all_data:
                for row in all_data[1:]:  # Saltar header
                    if len(row) > 6 and row[6] == sector:  # Columna G (índice 6)
                        if len(row) > 8 and row[8]:  # Columna I (índice 8)
                            filtered_lotes.append(row[8])
            
            # Eliminar duplicados y ordenar
            filtered_lotes = sorted(list(set(filtered_lotes)))
            
            if filtered_lotes:
                lote = st.selectbox("Lote *", [""] + filtered_lotes, index=0)
            else:
                st.warning("⚠️ No hay lotes disponibles para este sector")
                lote = None
        else:
            lote = st.selectbox("Lote *", [""] + dropdown_data['lotes'], index=0)
    
    # Upload de imágenes
    st.subheader("📁 Subir Imágenes")
    uploaded_files = st.file_uploader(
        "Arrastra y suelta las imágenes aquí",
        type=['jpg', 'png', 'jpeg'],
        accept_multiple_files=True,
        help="Puedes subir múltiples imágenes para análisis. Tamaño máximo recomendado: 5MB por imagen"
    )
    
    # Mostrar imágenes subidas con botones
    if uploaded_files:
        # Validar tamaño de archivos
        max_file_size = 10 * 1024 * 1024  # 10MB en bytes
        large_files = []
        
        for file in uploaded_files:
            if file.size > max_file_size:
                large_files.append(f"{file.name} ({file.size / (1024*1024):.1f}MB)")
        
        if large_files:
            st.warning(f"⚠️ **Archivos muy grandes detectados:**")
            for file_info in large_files:
                st.warning(f"• {file_info}")
            st.info("💡 **Recomendación:** Las imágenes grandes pueden causar problemas de memoria. Considera redimensionarlas antes de subir.")
        
        st.markdown("---")
        st.subheader("📸 Imágenes Subidas")
        
        # Mostrar cada imagen en una fila compacta
        for i, file in enumerate(uploaded_files):
            # Container compacto para cada imagen
            with st.container():
                # Extraer información del nombre del archivo si no está ya guardada
                if f"hilera_{i}" not in st.session_state or f"n_planta_{i}" not in st.session_state:
                    extracted_hilera, extracted_planta = extract_info_from_filename(file.name)
                    if extracted_hilera and extracted_planta:
                        st.session_state[f"hilera_{i}"] = extracted_hilera
                        st.session_state[f"n_planta_{i}"] = extracted_planta
                
                # Todo en una sola fila: nombre, botón ver, hilera, planta
                col1, col2, col3, col4 = st.columns([4, 1, 2, 2])
                
                with col1:
                    st.write(f"📁 **{file.name}**")
                
                with col2:
                    if st.button("👁️ Ver", key=f"view_{i}"):
                        st.session_state[f"show_image_{i}"] = True
                
                with col3:
                    hilera = st.text_input(
                        "Hilera", 
                        key=f"hilera_{i}",
                        placeholder="Ej: 114"
                    )
                
                with col4:
                    n_planta = st.text_input(
                        "N° Planta", 
                        key=f"n_planta_{i}",
                        placeholder="Ej: 22"
                    )
            
            # Mostrar imagen en modal si se presiona Ver
            if st.session_state.get(f"show_image_{i}", False):
                with st.expander(f"👁️ Vista: {file.name}", expanded=True):
                    # Imagen más pequeña (1/3 del tamaño)
                    st.image(file, caption=f"Vista completa: {file.name}", width=300)
                    if st.button("❌ Cerrar", key=f"close_view_{i}"):
                        st.session_state[f"show_image_{i}"] = False
                        st.rerun()
            
            
            # Separador entre filas
            st.markdown("---")
    
    # Botón de análisis
    if st.button("🔍 Analizar Imágenes", type="primary"):
        if not uploaded_files:
            st.error("⚠️ Por favor, sube al menos una imagen")
        elif not empresa or empresa == "" or not fundo or fundo == "" or not sector or sector == "" or not lote or lote == "":
            st.error("⚠️ Por favor, completa todos los campos obligatorios")
        else:
            st.success("✅ Iniciando análisis...")
            
            # Mostrar información del campo
            st.subheader("📋 Información del Campo")
            st.info(f"""
            **Empresa:** {empresa} | **Fundo:** {fundo} | **Sector:** {sector} | **Lote:** {lote}
            """)
            
            # Procesar cada imagen
            for i, uploaded_file in enumerate(uploaded_files):
                # Obtener información específica de esta imagen
                hilera_info = st.session_state.get(f"hilera_{i}", "")
                n_planta_info = st.session_state.get(f"n_planta_{i}", "")
                
                # Leer imagen
                image_bytes = uploaded_file.read()
                
                # Analizar imagen
                resultado = analizar_imagen_ml(image_bytes)
                
                if resultado:
                    mostrar_resultados(resultado, uploaded_file.name)
                    
                    # Guardar en Google Sheets
                    try:
                        import sys
                        import os
                        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
                        
                        from google_sheets.sheets_client import GoogleSheetsClient
                        
                        client = GoogleSheetsClient()
                        
                        # Verificar autenticación
                        if not client.authenticate():
                            st.error("❌ Error de autenticación con Google Sheets")
                            print("❌ Error de autenticación")
                        else:
                            # Preparar datos para guardar
                            record_data = {
                                'id': '',  # Se generará automáticamente
                                'fecha': datetime.now().strftime('%Y-%m-%d'),
                                'hora': datetime.now().strftime('%H:%M:%S'),
                                'imagen': uploaded_file.name,
                                'empresa': empresa,
                                'fundo': fundo,
                                'sector': sector,
                                'lote': lote,
                                'hilera': hilera_info if hilera_info else '',
                                'numero_planta': n_planta_info if n_planta_info else '',
                                'latitud': '',
                                'longitud': '',
                                'porcentaje_luz': float(resultado['light_percentage']),  # Convertir a float
                                'porcentaje_sombra': float(resultado['shadow_percentage']),  # Convertir a float
                                'dispositivo': '{}',
                                'software': 'Streamlit App',
                                'direccion': 'None',
                                'timestamp': datetime.now().isoformat()
                            }
                            
                            # Guardar en Google Sheets
                            print(f"🔄 Intentando guardar en Google Sheets...")
                            print(f"📋 Datos: {record_data}")
                            
                            if client.add_processing_record(client.spreadsheet_id, record_data, 'Data-app'):
                                st.success("✅ Resultados guardados en Google Sheets")
                                print("✅ Guardado exitoso")
                            else:
                                st.warning("⚠️ Error guardando en Google Sheets")
                                print("❌ Error en el guardado")
                            
                    except Exception as e:
                        st.error(f"❌ Error guardando resultados: {str(e)}")
                    
                    st.markdown("---")

elif page == "Probar Modelo":
    st.markdown('<h1 class="main-header">🧪 Probar Modelo</h1>', unsafe_allow_html=True)
    
    st.subheader("📸 Subir Imagen para Probar")
    uploaded_file = st.file_uploader(
        "Arrastra y suelta una imagen aquí",
        type=['jpg', 'png', 'jpeg'],
        help="Sube una imagen para probar el modelo de análisis"
    )
    
    if uploaded_file:
        # Leer imagen
        image_bytes = uploaded_file.read()
        
        # Analizar imagen
        resultado = analizar_imagen_ml(image_bytes)
        
        if resultado:
            mostrar_resultados(resultado, uploaded_file.name, mostrar_imagenes=True)
            
            # Información adicional
            st.subheader("ℹ️ Información del Análisis")
            st.info("""
            **Colores del análisis:**
            - 🟡 **Amarillo**: Áreas de luz
            - ⚫ **Gris oscuro**: Áreas de sombra
            
            **Método:** Random Forest (scikit-learn) con modelo perfeccionado
            """)

elif page == "Historial":
    st.markdown('<h1 class="main-header">📊 Historial de Análisis</h1>', unsafe_allow_html=True)
    
    # Tabla de resultados (datos reales)
    st.subheader("📋 Resultados")
    
    try:
        # Cargar datos reales de Google Sheets
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from google_sheets.sheets_client import GoogleSheetsClient
        
        client = GoogleSheetsClient()
        if client.spreadsheet_id:
            if client.authenticate():
                # Cargar configuración para obtener el nombre de la hoja
                import json
                try:
                    with open('google_sheets_config.json', 'r') as f:
                        config = json.load(f)
                        sheet_name = config.get('sheet_name', 'Data-app')
                except:
                    sheet_name = 'Data-app'
                
                records = client.get_processing_records(client.spreadsheet_id, limit=50, sheet_name=sheet_name)
            else:
                st.error("❌ Error de autenticación con Google Sheets")
                records = []
        else:
            st.error("❌ No se pudo cargar el ID de la hoja de cálculo")
            records = []
        
        if records:
            # Convertir a DataFrame
            df = pd.DataFrame(records)
            
            # Mostrar tabla
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Estadísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total registros", len(df))
            with col2:
                if len(df) > 0:
                    # Convertir a float y calcular promedio
                    light_values = pd.to_numeric(df['porcentaje_luz'], errors='coerce')
                    avg_light = light_values.mean()
                    st.metric("Luz promedio", f"{avg_light:.1f}%")
            with col3:
                if len(df) > 0:
                    # Convertir a float y calcular promedio
                    shadow_values = pd.to_numeric(df['porcentaje_sombra'], errors='coerce')
                    avg_shadow = shadow_values.mean()
                    st.metric("Sombra promedio", f"{avg_shadow:.1f}%")
        else:
            st.info("📝 No hay registros de análisis aún. Sube algunas imágenes para comenzar.")
            
    except Exception as e:
        st.error(f"❌ Error cargando historial: {str(e)}")
        st.info("📝 No se pudieron cargar los registros. Verifica la conexión con Google Sheets.")
    
    # Botón de exportar (solo si hay datos)
    if 'df' in locals() and not df.empty:
        if st.button("📥 Exportar CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f"historial_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    🌱 Análisis Agrícola Luz-Sombra v2.0 | Desarrollado con Streamlit
</div>
""", unsafe_allow_html=True)