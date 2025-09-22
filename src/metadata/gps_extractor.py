#!/usr/bin/env python3
"""
GPS Metadata Extractor
Basado en: https://github.com/ozgecinko/image-metadata-extractor

Extrae coordenadas GPS y metadatos de imágenes usando EXIF.
Incluye conversión de formato DMS a decimal y geocodificación inversa.
"""

import io
import os
import tempfile
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class GPSMetadataExtractor:
    """Extractor de metadatos GPS y EXIF de imágenes"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="agricola-luz-sombra-app")
    
    def extract_metadata(self, image_bytes: bytes, filename: str = None) -> Dict[str, Any]:
        """
        Extrae todos los metadatos de una imagen
        
        Args:
            image_bytes: Bytes de la imagen
            filename: Nombre del archivo (opcional)
            
        Returns:
            Dict con todos los metadatos extraídos
        """
        metadata = {
            'fecha_tomada': None,
            'gps_latitud': None,
            'gps_longitud': None,
            'gps_altitud': None,
            'direccion': None,
            'dispositivo': {},
            'exif_tags': {},
            'errores': []
        }
        
        try:
            # Abrir imagen
            img = Image.open(io.BytesIO(image_bytes))
            exifdata = img.getexif()
            
            # Extraer fecha
            metadata['fecha_tomada'] = self._extract_date(exifdata)
            
            # Extraer información del dispositivo
            metadata['dispositivo'] = self._extract_device_info(exifdata)
            
            # Extraer GPS
            gps_data = self._extract_gps_data(exifdata, image_bytes)
            metadata.update(gps_data)
            
            # Extraer todos los tags EXIF
            metadata['exif_tags'] = self._extract_all_exif_tags(exifdata)
            
            # Geocodificación inversa si hay coordenadas
            if metadata['gps_latitud'] and metadata['gps_longitud']:
                metadata['direccion'] = self._reverse_geocode(
                    metadata['gps_latitud'], 
                    metadata['gps_longitud']
                )
            
        except Exception as e:
            metadata['errores'].append(f"Error general: {str(e)}")
        
        return metadata
    
    def _extract_date(self, exifdata) -> Optional[datetime]:
        """Extrae fecha de captura del EXIF"""
        date_tags = ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']
        
        for tag_name in date_tags:
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                if tag == tag_name:
                    date_str = exifdata[tag_id]
                    if date_str:
                        try:
                            # Intentar diferentes formatos de fecha
                            for fmt in ["%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"]:
                                try:
                                    return datetime.strptime(date_str, fmt)
                                except ValueError:
                                    continue
                        except Exception as e:
                            print(f"Error parseando fecha {date_str}: {e}")
                            continue
        
        return None
    
    def _extract_device_info(self, exifdata) -> Dict[str, str]:
        """Extrae información del dispositivo"""
        device_info = {}
        
        device_tags = {
            'Make': 'fabricante',
            'Model': 'modelo',
            'Software': 'software',
            'ImageWidth': 'ancho',
            'ImageLength': 'alto'
        }
        
        for tag_name, key in device_tags.items():
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                if tag == tag_name:
                    device_info[key] = str(exifdata[tag_id])
                    break
        
        return device_info
    
    def _extract_gps_data(self, exifdata, image_bytes: bytes = None) -> Dict[str, Any]:
        """Extrae datos GPS del EXIF"""
        gps_data = {
            'gps_latitud': None,
            'gps_longitud': None,
            'gps_altitud': None,
            'gps_errores': []
        }
        
        try:
            print("🔍 Buscando datos GPS en EXIF...")
            
            # Buscar información GPS usando exifread
            try:
                import exifread
                if image_bytes:
                    # Usar los bytes de la imagen actual
                    tags = exifread.process_file(io.BytesIO(image_bytes), details=True)
                else:
                    # Fallback al archivo hardcodeado solo para pruebas
                    with open("dataset/imagenes/foto-fv5-gps.jpg", 'rb') as f:
                        tags = exifread.process_file(f, details=True)
                
                # Extraer latitud
                if 'GPS GPSLatitude' in tags and 'GPS GPSLatitudeRef' in tags:
                    lat_dms = str(tags['GPS GPSLatitude'])
                    lat_ref = str(tags['GPS GPSLatitudeRef'])
                    
                    # Convertir DMS a decimal
                    lat = self._convert_dms_to_decimal(lat_dms)
                    
                    if lat_ref == 'S':
                        lat = -lat
                    
                    gps_data['gps_latitud'] = lat
                    print(f"✅ Latitud GPS extraída: {lat} ({lat_ref})")
                
                # Extraer longitud
                if 'GPS GPSLongitude' in tags and 'GPS GPSLongitudeRef' in tags:
                    lon_dms = str(tags['GPS GPSLongitude'])
                    lon_ref = str(tags['GPS GPSLongitudeRef'])
                    
                    # Convertir DMS a decimal
                    lon = self._convert_dms_to_decimal(lon_dms)
                    
                    if lon_ref == 'W':
                        lon = -lon
                    
                    gps_data['gps_longitud'] = lon
                    print(f"✅ Longitud GPS extraída: {lon} ({lon_ref})")
                
                # Extraer altitud
                if 'GPS GPSAltitude' in tags:
                    gps_data['gps_altitud'] = float(str(tags['GPS GPSAltitude']))
                    print(f"✅ Altitud GPS extraída: {gps_data['gps_altitud']} m")
                
                # Extraer fecha GPS
                if 'GPS GPSDateStamp' in tags:
                    gps_date = str(tags['GPS GPSDateStamp'])
                    print(f"✅ Fecha GPS: {gps_date}")
                
                # Extraer hora GPS
                if 'GPS GPSTimeStamp' in tags:
                    gps_time = str(tags['GPS GPSTimeStamp'])
                    print(f"✅ Hora GPS: {gps_time}")
                
                if gps_data['gps_latitud'] and gps_data['gps_longitud']:
                    print(f"🎉 Coordenadas GPS completas: {gps_data['gps_latitud']}, {gps_data['gps_longitud']}")
                else:
                    gps_data['gps_errores'].append("No se pudieron extraer coordenadas GPS completas")
                
            except ImportError:
                gps_data['gps_errores'].append("exifread no está instalado")
            except Exception as e:
                gps_data['gps_errores'].append(f"Error con exifread: {str(e)}")
            
        except Exception as e:
            gps_data['gps_errores'].append(f"Error extrayendo GPS: {str(e)}")
        
        return gps_data
    
    def _search_custom_gps_format(self, exifdata) -> Dict[str, Any]:
        """
        Busca coordenadas GPS en formato personalizado (como Camera FV-5)
        
        Args:
            exifdata: Datos EXIF de la imagen
            
        Returns:
            Dict con coordenadas encontradas o None
        """
        coordinates = {
            'gps_latitud': None,
            'gps_longitud': None,
            'gps_errores': []
        }
        
        try:
            print("🔍 Buscando coordenadas GPS en todos los tags EXIF...")
            
            # Buscar en todos los tags EXIF por patrones de coordenadas
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                tag_value = exifdata[tag_id]
                
                # Mostrar todos los tags para debugging
                print(f"📍 Tag {tag} ({tag_id}): {tag_value} (tipo: {type(tag_value)})")
                
                # Buscar strings que contengan coordenadas en formato DMS
                if isinstance(tag_value, str) and ';' in tag_value:
                    print(f"🎯 Encontrado formato DMS en {tag}: {tag_value}")
                    
                    # Intentar parsear como coordenadas DMS
                    dms_coords = self._parse_dms_string(tag_value)
                    if dms_coords:
                        # Determinar si es latitud o longitud basado en el rango
                        if 0 <= dms_coords <= 90:
                            coordinates['gps_latitud'] = dms_coords
                            print(f"✅ Latitud detectada: {dms_coords}")
                        elif 0 <= dms_coords <= 180:
                            coordinates['gps_longitud'] = dms_coords
                            print(f"✅ Longitud detectada: {dms_coords}")
                
                # También buscar en tuplas/listas que puedan contener coordenadas
                elif isinstance(tag_value, (tuple, list)) and len(tag_value) >= 2:
                    print(f"🎯 Encontrado formato tupla en {tag}: {tag_value}")
                    
                    # Intentar convertir tupla a DMS string
                    if len(tag_value) == 3:
                        dms_string = f"{tag_value[0]}; {tag_value[1]}; {tag_value[2]}"
                        dms_coords = self._parse_dms_string(dms_string)
                        if dms_coords:
                            if 0 <= dms_coords <= 90:
                                coordinates['gps_latitud'] = dms_coords
                                print(f"✅ Latitud detectada desde tupla: {dms_coords}")
                            elif 0 <= dms_coords <= 180:
                                coordinates['gps_longitud'] = dms_coords
                                print(f"✅ Longitud detectada desde tupla: {dms_coords}")
            
            # Si no se encontraron coordenadas, mostrar mensaje informativo
            if not coordinates['gps_latitud'] and not coordinates['gps_longitud']:
                coordinates['gps_errores'].append("No se encontraron coordenadas en formato personalizado")
                print("📍 INFO: Las coordenadas GPS pueden estar en un formato personalizado")
                print("📍 Puedes ingresar las coordenadas manualmente en los campos del formulario")
            else:
                print(f"🎉 Coordenadas encontradas: Lat={coordinates['gps_latitud']}, Lon={coordinates['gps_longitud']}")
            
        except Exception as e:
            coordinates['gps_errores'].append(f"Error buscando formato personalizado: {str(e)}")
            print(f"❌ Error: {e}")
        
        return coordinates
    
    def _parse_dms_string(self, dms_string: str) -> Optional[float]:
        """
        Parsea string en formato 'grados; minutos; segundos' a decimal
        
        Args:
            dms_string: String en formato "12; 5; 56.0221999999994438"
            
        Returns:
            Coordenada en grados decimales o None si hay error
        """
        try:
            parts = dms_string.split(';')
            if len(parts) == 3:
                degrees = float(parts[0].strip())
                minutes = float(parts[1].strip())
                seconds = float(parts[2].strip())
                
                # Aplicar fórmula: Decimal = grados + (minutos / 60) + (segundos / 3600)
                decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
                
                print(f"    Conversión DMS: {degrees}° {minutes}' {seconds}\" = {decimal}°")
                return decimal
        except Exception as e:
            print(f"    Error parseando DMS string '{dms_string}': {e}")
        
        return None
    
    def _convert_dms_to_decimal(self, dms_string: str) -> Optional[float]:
        """
        Convierte string DMS a decimal
        Ejemplo: '[12, 5, 563861/10000]' -> 12.09899613888889
        """
        try:
            # Limpiar el string y extraer los valores
            dms_string = dms_string.strip('[]')
            parts = dms_string.split(', ')
            
            if len(parts) == 3:
                degrees = float(parts[0])
                minutes = float(parts[1])
                
                # Manejar fracciones en segundos
                seconds_str = parts[2]
                if '/' in seconds_str:
                    num, den = seconds_str.split('/')
                    seconds = float(num) / float(den)
                else:
                    seconds = float(seconds_str)
                
                # Aplicar fórmula: Decimal = grados + (minutos / 60) + (segundos / 3600)
                decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
                
                print(f"    Conversión DMS: {degrees}° {minutes}' {seconds}\" = {decimal}°")
                return decimal
        except Exception as e:
            print(f"Error convirtiendo DMS '{dms_string}': {e}")
        
        return None

    def _convert_to_decimal(self, value) -> Optional[float]:
        """
        Convierte coordenadas GPS EXIF a grados decimales
        
        Args:
            value: Valor de coordenada en formato EXIF (tupla de 3 elementos)
            
        Returns:
            Coordenada en grados decimales o None si hay error
        """
        try:
            if isinstance(value, (list, tuple)) and len(value) == 3:
                degrees, minutes, seconds = value
                
                # Manejar fracciones
                if hasattr(degrees, 'numerator') and hasattr(degrees, 'denominator'):
                    degrees = float(degrees.numerator) / float(degrees.denominator)
                if hasattr(minutes, 'numerator') and hasattr(minutes, 'denominator'):
                    minutes = float(minutes.numerator) / float(minutes.denominator)
                if hasattr(seconds, 'numerator') and hasattr(seconds, 'denominator'):
                    seconds = float(seconds.numerator) / float(seconds.denominator)
                
                return degrees + (minutes / 60.0) + (seconds / 3600.0)
        except Exception as e:
            print(f"Error convirtiendo coordenada {value}: {e}")
        
        return None
    
    def _extract_all_exif_tags(self, exifdata) -> Dict[str, Any]:
        """Extrae todos los tags EXIF disponibles"""
        tags = {}
        
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            value = exifdata[tag_id]
            
            # Convertir valores complejos a string
            if hasattr(value, 'numerator') and hasattr(value, 'denominator'):
                value = float(value.numerator) / float(value.denominator)
            elif isinstance(value, bytes):
                try:
                    value = value.decode('utf-8')
                except:
                    value = str(value)
            
            tags[tag] = value
        
        return tags
    
    def _reverse_geocode(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Convierte coordenadas GPS a dirección usando geocodificación inversa
        
        Args:
            latitude: Latitud en grados decimales
            longitude: Longitud en grados decimales
            
        Returns:
            Dirección como string o None si hay error
        """
        try:
            location = self.geolocator.reverse(f"{latitude}, {longitude}", timeout=10)
            if location:
                return location.address
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Error en geocodificación: {e}")
        except Exception as e:
            print(f"Error inesperado en geocodificación: {e}")
        
        return None
    
    def parse_dms_to_decimal(self, dms_string: str) -> Optional[float]:
        """
        Parsea string en formato 'grados; minutos; segundos' a decimal
        
        Args:
            dms_string: String en formato "12; 5; 56.0221999999994438"
            
        Returns:
            Coordenada en grados decimales o None si hay error
        """
        try:
            parts = dms_string.split(';')
            if len(parts) == 3:
                degrees = float(parts[0].strip())
                minutes = float(parts[1].strip())
                seconds = float(parts[2].strip())
                return degrees + (minutes / 60.0) + (seconds / 3600.0)
        except Exception as e:
            print(f"Error parseando DMS string '{dms_string}': {e}")
        
        return None


def test_extractor():
    """Función de prueba para el extractor"""
    extractor = GPSMetadataExtractor()
    
    # Probar con imagen de prueba
    test_image_path = "dataset/imagenes/foto-fv5-gps.jpg"
    
    if os.path.exists(test_image_path):
        with open(test_image_path, 'rb') as f:
            image_bytes = f.read()
        
        metadata = extractor.extract_metadata(image_bytes, test_image_path)
        
        print("🔍 METADATOS EXTRAÍDOS:")
        print("=" * 50)
        print(f"📅 Fecha: {metadata['fecha_tomada']}")
        print(f"📍 GPS: {metadata['gps_latitud']}, {metadata['gps_longitud']}")
        print(f"🏠 Dirección: {metadata['direccion']}")
        print(f"📱 Dispositivo: {metadata['dispositivo']}")
        
        if metadata['gps_errores']:
            print(f"❌ Errores GPS: {metadata['gps_errores']}")
        
        if metadata['errores']:
            print(f"❌ Errores generales: {metadata['errores']}")
    else:
        print(f"❌ No se encontró la imagen de prueba: {test_image_path}")


if __name__ == "__main__":
    test_extractor()
