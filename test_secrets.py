#!/usr/bin/env python3
"""
Script de prueba para verificar que los secrets de Streamlit Cloud funcionan
"""

import streamlit as st
import os

st.title("🔍 Test de Secrets - Streamlit Cloud")

st.write("### Verificando configuración de secrets...")

# Verificar si estamos en Streamlit Cloud
if 'STREAMLIT_SHARING_MODE' in os.environ:
    st.success("✅ Ejecutándose en Streamlit Cloud")
else:
    st.warning("⚠️ Ejecutándose localmente")

# Verificar secrets
try:
    if 'google_sheets' in st.secrets:
        st.success("✅ Sección 'google_sheets' encontrada en secrets")
        
        # Verificar cada campo
        fields = ['spreadsheet_id', 'sheet_name', 'client_email', 'private_key', 'project_id', 'token_uri']
        for field in fields:
            if field in st.secrets.google_sheets:
                st.success(f"✅ {field}: {'*' * 20} (configurado)")
            else:
                st.error(f"❌ {field}: NO encontrado")
    else:
        st.error("❌ Sección 'google_sheets' NO encontrada en secrets")
        
except Exception as e:
    st.error(f"❌ Error accediendo a secrets: {str(e)}")

# Verificar archivo del modelo
st.write("### Verificando modelo...")
if os.path.exists("modelo_perfeccionado.pkl"):
    st.success("✅ Archivo modelo_perfeccionado.pkl encontrado")
    size = os.path.getsize("modelo_perfeccionado.pkl")
    st.info(f"📏 Tamaño del archivo: {size:,} bytes")
else:
    st.error("❌ Archivo modelo_perfeccionado.pkl NO encontrado")

# Mostrar estructura de directorios
st.write("### Estructura de archivos:")
import subprocess
try:
    result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
    st.code(result.stdout)
except:
    try:
        result = subprocess.run(['dir'], capture_output=True, text=True, shell=True)
        st.code(result.stdout)
    except:
        st.write("No se pudo listar archivos")
