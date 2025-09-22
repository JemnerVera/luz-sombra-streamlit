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
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes necesarios para Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetsClient:
    """Cliente para interactuar con Google Sheets"""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.creds = None
        
    def authenticate(self) -> bool:
        """
        Autentica con Google Sheets API
        
        Returns:
            bool: True si la autenticación fue exitosa
        """
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
            print("✅ Autenticación con Google Sheets exitosa")
            return True
            
        except Exception as e:
            print(f"❌ Error en autenticación: {e}")
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
            
            # Preparar datos para la fila
            row_data = [
                record.get('id', ''),
                record.get('fecha', ''),
                record.get('hora', ''),
                record.get('imagen', ''),
                record.get('nombre_archivo', ''),  # Nueva columna: Nombre Archivo
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
            range_name = f"'{sheet_name}'!A:S" if sheet_name else 'A:S'
            
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
            range_name = f"'{sheet_name}'!A2:S{limit + 1}" if sheet_name else f'A2:S{limit + 1}'
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            records = []
            
            for row in values:
                if len(row) >= 19:  # Asegurar que tenemos todas las columnas (ahora 19)
                    record = {
                        'id': row[0] if len(row) > 0 else '',
                        'fecha': row[1] if len(row) > 1 else '',
                        'hora': row[2] if len(row) > 2 else '',
                        'imagen': row[3] if len(row) > 3 else '',
                        'nombre_archivo': row[4] if len(row) > 4 else '',  # Nueva columna
                        'empresa': row[5] if len(row) > 5 else '',
                        'fundo': row[6] if len(row) > 6 else '',
                        'sector': row[7] if len(row) > 7 else '',
                        'lote': row[8] if len(row) > 8 else '',
                        'hilera': row[9] if len(row) > 9 else '',
                        'numero_planta': row[10] if len(row) > 10 else '',
                        'latitud': row[11] if len(row) > 11 else '',
                        'longitud': row[12] if len(row) > 12 else '',
                        'porcentaje_luz': row[13] if len(row) > 13 else '',
                        'porcentaje_sombra': row[14] if len(row) > 14 else '',
                        'dispositivo': row[15] if len(row) > 15 else '',
                        'software': row[16] if len(row) > 16 else '',
                        'direccion': row[17] if len(row) > 17 else '',
                        'timestamp': row[18] if len(row) > 18 else ''
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
