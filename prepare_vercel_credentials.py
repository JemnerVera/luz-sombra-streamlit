#!/usr/bin/env python3
"""
Script para preparar credenciales de Google Sheets para Vercel
Convierte los archivos JSON a Base64 para usar como variables de entorno
"""

import base64
import json
import os

def encode_file_to_base64(file_path):
    """Convierte un archivo a Base64"""
    if not os.path.exists(file_path):
        print(f"❌ Archivo no encontrado: {file_path}")
        return None
    
    with open(file_path, 'rb') as f:
        content = f.read()
        encoded = base64.b64encode(content).decode('utf-8')
        return encoded

def main():
    print("🔐 Preparando credenciales para Vercel...")
    print("=" * 50)
    
    # Verificar archivos necesarios
    required_files = ['credentials.json', 'token.json', 'google_sheets_config.json']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        print("Asegúrate de tener estos archivos en el directorio raíz")
        return
    
    # Leer configuración
    with open('google_sheets_config.json', 'r') as f:
        config = json.load(f)
    
    # Convertir archivos a Base64
    print("📄 Convirtiendo archivos a Base64...")
    
    credentials_b64 = encode_file_to_base64('credentials.json')
    token_b64 = encode_file_to_base64('token.json')
    
    if not credentials_b64 or not token_b64:
        print("❌ Error al convertir archivos a Base64")
        return
    
    print("✅ Archivos convertidos exitosamente")
    print()
    
    # Mostrar variables de entorno para Vercel
    print("🌐 Variables de entorno para Vercel:")
    print("=" * 50)
    print()
    
    print("# Google Sheets Configuration")
    print(f"GOOGLE_SHEETS_SPREADSHEET_ID={config['spreadsheet_id']}")
    print(f"GOOGLE_SHEETS_SHEET_NAME={config['sheet_name']}")
    print()
    
    print("# Google Sheets Credentials (Base64)")
    print(f"GOOGLE_SHEETS_CREDENTIALS_BASE64={credentials_b64}")
    print(f"GOOGLE_SHEETS_TOKEN_BASE64={token_b64}")
    print()
    
    print("# API Configuration")
    print("REACT_APP_API_URL=https://tu-backend.railway.app")
    print()
    
    print("📋 Instrucciones:")
    print("1. Copia las variables de entorno mostradas arriba")
    print("2. Ve a tu proyecto en Vercel Dashboard")
    print("3. Ve a Settings > Environment Variables")
    print("4. Agrega cada variable de entorno")
    print("5. Asegúrate de que estén disponibles en Production")
    print()
    
    # Guardar en archivo para referencia
    with open('vercel_env_vars.txt', 'w') as f:
        f.write("# Variables de entorno para Vercel\n")
        f.write("# Google Sheets Configuration\n")
        f.write(f"GOOGLE_SHEETS_SPREADSHEET_ID={config['spreadsheet_id']}\n")
        f.write(f"GOOGLE_SHEETS_SHEET_NAME={config['sheet_name']}\n")
        f.write("\n")
        f.write("# Google Sheets Credentials (Base64)\n")
        f.write(f"GOOGLE_SHEETS_CREDENTIALS_BASE64={credentials_b64}\n")
        f.write(f"GOOGLE_SHEETS_TOKEN_BASE64={token_b64}\n")
        f.write("\n")
        f.write("# API Configuration\n")
        f.write("REACT_APP_API_URL=https://tu-backend.railway.app\n")
    
    print("💾 Variables guardadas en 'vercel_env_vars.txt'")
    print("⚠️  IMPORTANTE: No subas este archivo al repositorio!")

if __name__ == "__main__":
    main()
