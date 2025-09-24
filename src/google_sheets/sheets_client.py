#!/usr/bin/env python3
"""
Google Sheets Client
Integración con Google Sheets para almacenar datos de procesamiento de imágenes
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

# Scopes necesarios para Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetsClient:
    """Cliente para interactuar con Google Sheets"""
    
    def __init__(self, credentials_file: str = 'config/credentials.json', token_file: str = 'config/token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.creds = None
        self.use_streamlit_secrets = False
        
        # Intentar cargar desde Streamlit secrets primero (para producción)
        try:
            if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
                self.spreadsheet_id = st.secrets.google_sheets.spreadsheet_id
                self.use_streamlit_secrets = True
                print("✅ Usando secrets de Streamlit Cloud")
            else:
                raise Exception("No hay secrets de Streamlit")
        except Exception as e:
            print(f"⚠️ No se encontraron secrets de Streamlit: {e}")
            # Fallback a configuración local
            try:
                with open('config/google_sheets_config.json', 'r') as f:
                    config = json.load(f)
                    self.spreadsheet_id = config.get('spreadsheet_id')
                print("✅ Usando configuración local")
            except Exception as e2:
                print(f"⚠️ Error cargando configuración local: {e2}")
                self.spreadsheet_id = None
        
    def authenticate(self) -> bool:
        """
        Autentica con Google Sheets API
        
        Returns:
            bool: True si la autenticación fue exitosa
        """
        try:
            if self.use_streamlit_secrets:
                # Usar Service Account desde Streamlit secrets
                return self._authenticate_with_service_account()
            else:
                # Usar OAuth2 local
                return self._authenticate_with_oauth2()
                
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
            return False
    
    def _authenticate_with_service_account(self) -> bool:
        """Autenticación usando Service Account desde Streamlit secrets"""
        try:
            # Crear credenciales desde secrets
            service_account_info = {
                "type": "service_account",
                "project_id": st.secrets.google_sheets.project_id,
                "private_key_id": "dummy",  # No necesario para autenticación
                "private_key": st.secrets.google_sheets.private_key,
                "client_email": st.secrets.google_sheets.client_email,
                "client_id": "dummy",  # No necesario para autenticación
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": st.secrets.google_sheets.token_uri,
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{st.secrets.google_sheets.client_email}",
                "universe_domain": "googleapis.com"
            }
            
            # Crear credenciales
            self.creds = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=SCOPES)
            
            # Construir el servicio
            self.service = build('sheets', 'v4', credentials=self.creds)
            print("✅ Autenticación con Service Account exitosa")
            return True
            
        except Exception as e:
            print(f"❌ Error en autenticación con Service Account: {e}")
            return False
    
    def _authenticate_with_oauth2(self) -> bool:
        """Autenticación usando OAuth2 local"""
        try:
            # Cargar credenciales existentes
            if os.path.exists(self.token_file):
                self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            
            # Si no hay credenciales válidas, solicitar autorización
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        print(f"❌ No se encontró el archivo de credenciales: {self.credentials_file}")
                        print("📋 Necesitas descargar las credenciales desde Google Cloud Console")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                # Guardar credenciales para la próxima vez
                with open(self.token_file, 'w') as token:
                    token.write(self.creds.to_json())
            
            # Construir el servicio
            self.service = build('sheets', 'v4', credentials=self.creds)
            print("✅ Autenticación con OAuth2 exitosa")
            return True
            
        except Exception as e:
            print(f"❌ Error en autenticación OAuth2: {e}")
            return False
    
    def create_spreadsheet(self, title: str = "Agricola Luz-Sombra") -> Optional[str]:
        """
        Crea una nueva hoja de cálculo
        
        Args:
            title: Título de la hoja de cálculo
            
        Returns:
            str: ID de la hoja de cálculo creada o None si hay error
        """
        try:
            spreadsheet = {
                'properties': {
                    'title': title
                },
                'sheets': [{
                    'properties': {
                        'title': 'Procesamientos',
                        'gridProperties': {
                            'rowCount': 1000,
                            'columnCount': 15
                        }
                    }
                }]
            }
            
            spreadsheet = self.service.spreadsheets().create(
                body=spreadsheet,
                fields='spreadsheetId'
            ).execute()
            
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            print(f"✅ Hoja de cálculo creada: {spreadsheet_id}")
            
            # Configurar encabezados
            self._setup_headers(spreadsheet_id)
            
            return spreadsheet_id
            
        except HttpError as e:
            print(f"❌ Error creando hoja de cálculo: {e}")
            return None
    
    def _setup_headers(self, spreadsheet_id: str, sheet_name: str = None) -> bool:
        """
        Configura los encabezados de la hoja de cálculo
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            sheet_name: Nombre de la hoja (opcional)
            
        Returns:
            bool: True si se configuraron correctamente
        """
        try:
            headers = [
                'ID', 'Fecha', 'Hora', 'Imagen', 'Nombre Archivo', 'Empresa', 'Fundo', 'Sector', 'Lote', 'Hilera', 'N° Planta',
                'Latitud', 'Longitud', 'Porcentaje Luz', 'Porcentaje Sombra',
                'Dispositivo', 'Software', 'Dirección', 'Timestamp'
            ]
            
            body = {
                'values': [headers]
            }
            
            # Usar el nombre de la hoja especificado o el por defecto
            range_name = f"'{sheet_name}'!A1:S1" if sheet_name else 'A1:S1'
            
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print("✅ Encabezados configurados correctamente")
            return True
            
        except HttpError as e:
            print(f"❌ Error configurando encabezados: {e}")
            return False
    
    def ensure_headers_updated(self, spreadsheet_id: str, sheet_name: str = None) -> bool:
        """
        Verifica y actualiza los encabezados de una hoja existente si es necesario
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            sheet_name: Nombre de la hoja (opcional)
            
        Returns:
            bool: True si los encabezados están correctos
        """
        try:
            # Obtener encabezados actuales
            range_name = f"'{sheet_name}'!A1:S1" if sheet_name else 'A1:S1'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            current_headers = result.get('values', [[]])[0] if result.get('values') else []
            
            # Encabezados esperados
            expected_headers = [
                'ID', 'Fecha', 'Hora', 'Imagen', 'Nombre Archivo', 'Empresa', 'Fundo', 'Sector', 'Lote', 'Hilera', 'N° Planta',
                'Latitud', 'Longitud', 'Porcentaje Luz', 'Porcentaje Sombra',
                'Dispositivo', 'Software', 'Dirección', 'Timestamp'
            ]
            
            # Verificar si los encabezados son exactamente correctos
            print(f"📋 Encabezados actuales ({len(current_headers)}): {current_headers}")
            print(f"📋 Encabezados esperados ({len(expected_headers)}): {expected_headers}")
            
            # Si el número de columnas no coincide, actualizar
            if len(current_headers) != len(expected_headers):
                print(f"🔄 Número de columnas diferente: {len(current_headers)} vs {len(expected_headers)}")
                print("🔄 Actualizando encabezados de la hoja...")
                return self._setup_headers(spreadsheet_id, sheet_name)
            
            # Si el número de columnas coincide, verificar si todos los encabezados coinciden exactamente
            matches = sum(1 for i, header in enumerate(expected_headers) 
                        if i < len(current_headers) and current_headers[i] == header)
            
            if matches == len(expected_headers):  # 100% de coincidencia exacta
                print("✅ Encabezados ya están actualizados")
                return True
            else:
                print(f"🔄 Solo {matches}/{len(expected_headers)} encabezados coinciden")
                print("🔄 Actualizando encabezados de la hoja...")
                return self._setup_headers(spreadsheet_id, sheet_name)
            
        except HttpError as e:
            print(f"❌ Error verificando encabezados: {e}")
            return False
    
    def force_update_headers(self, spreadsheet_id: str, sheet_name: str = None) -> bool:
        """
        Fuerza la actualización de los encabezados de la hoja
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            sheet_name: Nombre de la hoja (opcional)
            
        Returns:
            bool: True si se actualizaron correctamente
        """
        print("🔄 Forzando actualización de encabezados...")
        return self._setup_headers(spreadsheet_id, sheet_name)
    
    def _get_next_id(self, spreadsheet_id: str, sheet_name: str = None) -> int:
        """
        Obtiene el siguiente ID secuencial
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            sheet_name: Nombre de la hoja
            
        Returns:
            int: Siguiente ID disponible
        """
        try:
            # Obtener registros existentes
            records = self.get_processing_records(spreadsheet_id, limit=1000, sheet_name=sheet_name)
            
            if not records:
                return 1
            
            # Encontrar el ID más alto
            max_id = 0
            for record in records:
                try:
                    record_id = int(record.get('id', 0))
                    if record_id > max_id:
                        max_id = record_id
                except (ValueError, TypeError):
                    continue
            
            return max_id + 1
            
        except Exception as e:
            print(f"⚠️ Error obteniendo siguiente ID: {e}")
            return 1

    def add_processing_record(self, spreadsheet_id: str, record: Dict[str, Any], sheet_name: str = None) -> bool:
        """
        Agrega un registro de procesamiento a la hoja de cálculo
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            record: Diccionario con los datos del procesamiento
            sheet_name: Nombre de la hoja (opcional, por defecto usa 'Procesamientos')
            
        Returns:
            bool: True si se agregó correctamente
        """
        try:
            # Verificar y actualizar encabezados si es necesario
            self.ensure_headers_updated(spreadsheet_id, sheet_name)
            
            # Generar ID automáticamente si no se proporciona
            if not record.get('id') or record.get('id') == '':
                next_id = self._get_next_id(spreadsheet_id, sheet_name)
                record['id'] = str(next_id)
                print(f"🆔 ID generado automáticamente: {next_id}")
            
            # Preparar datos para la fila (18 columnas, sin "Nombre Archivo")
            row_data = [
                record.get('id', ''),
                record.get('fecha', ''),
                record.get('hora', ''),
                record.get('imagen', ''),
                record.get('empresa', ''),
                record.get('fundo', ''),
                record.get('sector', ''),
                record.get('lote', ''),
                record.get('hilera') if record.get('hilera') is not None else '',  # Hilera puede ser null
                record.get('numero_planta') if record.get('numero_planta') is not None else '',  # N° Planta puede ser null
                record.get('latitud', ''),
                record.get('longitud', ''),
                record.get('porcentaje_luz', ''),
                record.get('porcentaje_sombra', ''),
                record.get('dispositivo', ''),
                record.get('software', ''),
                record.get('direccion', ''),
                record.get('timestamp', '')
            ]
            
            print(f"📋 Datos de fila a insertar: {row_data}")
            print(f"📊 Número de columnas: {len(row_data)}")
            
            body = {
                'values': [row_data]
            }
            
            # Usar el nombre de la hoja especificado o el por defecto
            range_name = f"'{sheet_name}'!A:R" if sheet_name else 'A:R'
            
            self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            print(f"✅ Registro agregado: {record.get('imagen', 'N/A')}")
            return True
            
        except HttpError as e:
            print(f"❌ Error agregando registro: {e}")
            return False
    
    def get_sheet_data(self, sheet_name: str) -> List[List[str]]:
        """
        Obtiene todos los datos de una hoja
        
        Args:
            sheet_name: Nombre de la hoja
            
        Returns:
            List[List[str]]: Lista de filas con datos
        """
        try:
            if not self.authenticate():
                return []
            
            # Construir rango de toda la hoja
            range_name = f"{sheet_name}!A:Z"  # A hasta Z columnas
            
            # Obtener datos
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            return values
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de hoja {sheet_name}: {e}")
            return []

    def get_column_data(self, sheet_name: str, column: str) -> List[str]:
        """
        Obtiene todos los datos de una columna específica
        
        Args:
            sheet_name: Nombre de la hoja
            column: Columna (ej: 'A', 'B', 'C', etc.)
            
        Returns:
            List[str]: Lista de valores de la columna
        """
        try:
            if not self.authenticate():
                return []
            
            # Construir rango de la columna
            range_name = f"{sheet_name}!{column}:{column}"
            
            # Obtener datos
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            # Flatten la lista (cada fila es una lista con un elemento)
            column_data = [row[0] if row else '' for row in values]
            
            return column_data
            
        except Exception as e:
            print(f"❌ Error obteniendo datos de columna {column}: {e}")
            return []

    def get_processing_records(self, spreadsheet_id: str, limit: int = 100, sheet_name: str = None) -> List[Dict[str, Any]]:
        """
        Obtiene los registros de procesamiento de la hoja de cálculo
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            limit: Número máximo de registros a obtener
            sheet_name: Nombre de la hoja (opcional, por defecto usa 'Procesamientos')
            
        Returns:
            List[Dict]: Lista de registros de procesamiento
        """
        try:
            # Usar el nombre de la hoja especificado o el por defecto
            range_name = f"'{sheet_name}'!A2:R{limit + 1}" if sheet_name else f'A2:R{limit + 1}'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            records = []
            
            for row in values:
                if len(row) >= 18:  # Ajustar para 18 columnas (sin "Nombre Archivo")
                    record = {
                        'id': row[0] if len(row) > 0 else '',
                        'fecha': row[1] if len(row) > 1 else '',
                        'hora': row[2] if len(row) > 2 else '',
                        'imagen': row[3] if len(row) > 3 else '',
                        'empresa': row[4] if len(row) > 4 else '',
                        'fundo': row[5] if len(row) > 5 else '',
                        'sector': row[6] if len(row) > 6 else '',
                        'lote': row[7] if len(row) > 7 else '',
                        'hilera': row[8] if len(row) > 8 else '',
                        'numero_planta': row[9] if len(row) > 9 else '',
                        'latitud': row[10] if len(row) > 10 else '',
                        'longitud': row[11] if len(row) > 11 else '',
                        'porcentaje_luz': row[12] if len(row) > 12 else '',
                        'porcentaje_sombra': row[13] if len(row) > 13 else '',
                        'dispositivo': row[14] if len(row) > 14 else '',
                        'software': row[15] if len(row) > 15 else '',
                        'direccion': row[16] if len(row) > 16 else '',
                        'timestamp': row[17] if len(row) > 17 else ''
                    }
                    
                    # Debug: imprimir los primeros registros para verificar el mapeo
                    if len(records) < 2:
                        print(f"🔍 Debug registro {len(records) + 1}:")
                        print(f"  Row length: {len(row)}")
                        print(f"  Empresa (row[4]): '{row[4] if len(row) > 4 else 'N/A'}'")
                        print(f"  Lote (row[7]): '{row[7] if len(row) > 7 else 'N/A'}'")
                        print(f"  N° Planta (row[9]): '{row[9] if len(row) > 9 else 'N/A'}'")
                        print(f"  Record empresa: '{record['empresa']}'")
                        print(f"  Record lote: '{record['lote']}'")
                        print(f"  Record numero_planta: '{record['numero_planta']}'")
                    
                    records.append(record)
            
            print(f"✅ Obtenidos {len(records)} registros")
            return records
            
        except HttpError as e:
            print(f"❌ Error obteniendo registros: {e}")
            return []
    
    def get_spreadsheet_url(self, spreadsheet_id: str) -> str:
        """
        Obtiene la URL de la hoja de cálculo
        
        Args:
            spreadsheet_id: ID de la hoja de cálculo
            
        Returns:
            str: URL de la hoja de cálculo
        """
        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"


def test_sheets_client():
    """Función de prueba para el cliente de Google Sheets"""
    client = GoogleSheetsClient()
    
    if client.authenticate():
        print("🔍 Probando Google Sheets...")
        
        # Crear hoja de cálculo de prueba
        spreadsheet_id = client.create_spreadsheet("Test Agricola")
        
        if spreadsheet_id:
            print(f"📊 Hoja creada: {client.get_spreadsheet_url(spreadsheet_id)}")
            
            # Agregar registro de prueba
            test_record = {
                'id': '1',
                'fecha': '2025-01-15',
                'hora': '10:30:00',
                'imagen': 'test.jpg',
                'empresa': 'Empresa Test',
                'fundo': 'Fundo A',
                'sector': 'Sector 1',
                'lote': 'Lote 1',
                'hilera': 'Hilera 1',
                'numero_planta': 'Planta 1',
                'latitud': '-33.4489',
                'longitud': '-70.6693',
                'porcentaje_luz': '65.5',
                'porcentaje_sombra': '34.5',
                'dispositivo': 'Xiaomi',
                'software': 'Open Camera',
                'direccion': 'Santiago, Chile',
                'timestamp': datetime.now().isoformat()
            }
            
            if client.add_processing_record(spreadsheet_id, test_record):
                print("✅ Registro de prueba agregado")
                
                # Obtener registros
                records = client.get_processing_records(spreadsheet_id)
                print(f"📋 Registros obtenidos: {len(records)}")
            else:
                print("❌ Error agregando registro de prueba")
        else:
            print("❌ Error creando hoja de cálculo")
    else:
        print("❌ Error en autenticación")


if __name__ == "__main__":
    test_sheets_client()
