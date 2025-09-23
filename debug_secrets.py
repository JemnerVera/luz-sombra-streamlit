#!/usr/bin/env python3
"""
Script de diagnóstico para verificar secrets en Streamlit Cloud
"""

import streamlit as st
import os
import traceback

st.set_page_config(page_title="Debug Secrets", layout="wide")

st.title("🔍 Diagnóstico de Secrets - Streamlit Cloud")

# Verificar entorno
st.subheader("🌍 Información del Entorno")
st.write(f"**STREAMLIT_SHARING_MODE**: {os.environ.get('STREAMLIT_SHARING_MODE', 'No definido')}")
st.write(f"**STREAMLIT_SERVER_PORT**: {os.environ.get('STREAMLIT_SERVER_PORT', 'No definido')}")

# Verificar si estamos en Streamlit Cloud
if 'STREAMLIT_SHARING_MODE' in os.environ:
    st.success("✅ Ejecutándose en Streamlit Cloud")
    is_cloud = True
else:
    st.warning("⚠️ Ejecutándose localmente")
    is_cloud = False

st.divider()

# Verificar secrets
st.subheader("🔐 Verificación de Secrets")

try:
    # Verificar si existe la sección google_sheets
    if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
        st.success("✅ Sección 'google_sheets' encontrada en secrets")
        
        # Verificar cada campo individualmente
        fields_to_check = {
            'spreadsheet_id': 'ID de la hoja de cálculo',
            'sheet_name': 'Nombre de la hoja',
            'client_email': 'Email del Service Account',
            'private_key': 'Clave privada',
            'project_id': 'ID del proyecto',
            'token_uri': 'URI del token'
        }
        
        for field, description in fields_to_check.items():
            try:
                if field in st.secrets.google_sheets:
                    value = st.secrets.google_sheets[field]
                    if value and value.strip():
                        st.success(f"✅ {field} ({description}): Configurado")
                        # Mostrar solo los primeros y últimos caracteres para seguridad
                        if field == 'private_key':
                            display_value = f"{value[:20]}...{value[-20:]}" if len(value) > 40 else "***"
                        else:
                            display_value = f"{value[:10]}...{value[-10:]}" if len(str(value)) > 20 else str(value)
                        st.code(f"{field}: {display_value}")
                    else:
                        st.error(f"❌ {field} ({description}): Vacío o nulo")
                else:
                    st.error(f"❌ {field} ({description}): NO encontrado")
            except Exception as e:
                st.error(f"❌ Error verificando {field}: {str(e)}")
                
    else:
        st.error("❌ Sección 'google_sheets' NO encontrada en secrets")
        st.write("**Secrets disponibles:**")
        try:
            if hasattr(st, 'secrets'):
                for key in st.secrets.keys():
                    st.write(f"- {key}")
            else:
                st.write("No se pudo acceder a st.secrets")
        except Exception as e:
            st.write(f"Error accediendo a secrets: {str(e)}")
            
except Exception as e:
    st.error(f"❌ Error general accediendo a secrets: {str(e)}")
    st.code(traceback.format_exc())

st.divider()

# Verificar archivo del modelo
st.subheader("🤖 Verificación del Modelo")
if os.path.exists("modelo_perfeccionado.pkl"):
    st.success("✅ Archivo modelo_perfeccionado.pkl encontrado")
    size = os.path.getsize("modelo_perfeccionado.pkl")
    st.info(f"📏 Tamaño del archivo: {size:,} bytes")
else:
    st.error("❌ Archivo modelo_perfeccionado.pkl NO encontrado")

# Listar archivos en el directorio
st.subheader("📁 Archivos en el directorio")
try:
    files = os.listdir(".")
    st.write(f"**Total de archivos:** {len(files)}")
    
    # Mostrar archivos relevantes
    relevant_files = [f for f in files if any(keyword in f.lower() for keyword in ['modelo', 'streamlit', 'requirements', 'gitignore'])]
    if relevant_files:
        st.write("**Archivos relevantes:**")
        for file in relevant_files:
            st.write(f"- {file}")
    
    # Mostrar todos los archivos (limitado)
    if len(files) <= 20:
        st.write("**Todos los archivos:**")
        for file in sorted(files):
            st.write(f"- {file}")
    else:
        st.write("**Primeros 20 archivos:**")
        for file in sorted(files)[:20]:
            st.write(f"- {file}")
        st.write(f"... y {len(files) - 20} archivos más")
        
except Exception as e:
    st.error(f"Error listando archivos: {str(e)}")

st.divider()

# Test de autenticación básica
st.subheader("🧪 Test de Autenticación Básica")
if st.button("🔍 Probar Autenticación"):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        # Obtener credenciales de secrets
        if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
            secrets = st.secrets.google_sheets
            
            # Crear credenciales
            credentials = service_account.Credentials.from_service_account_info({
                "type": "service_account",
                "project_id": secrets.get('project_id'),
                "private_key_id": "test",
                "private_key": secrets.get('private_key'),
                "client_email": secrets.get('client_email'),
                "client_id": "test",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": secrets.get('token_uri'),
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "test"
            })
            
            # Crear servicio
            service = build('sheets', 'v4', credentials=credentials)
            
            # Probar acceso
            spreadsheet_id = secrets.get('spreadsheet_id')
            if spreadsheet_id:
                result = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
                st.success("✅ Autenticación exitosa con Google Sheets")
                st.write(f"**Título de la hoja:** {result.get('properties', {}).get('title', 'Sin título')}")
            else:
                st.error("❌ No se encontró spreadsheet_id en secrets")
                
        else:
            st.error("❌ No se pudieron obtener los secrets")
            
    except Exception as e:
        st.error(f"❌ Error en autenticación: {str(e)}")
        st.code(traceback.format_exc())
