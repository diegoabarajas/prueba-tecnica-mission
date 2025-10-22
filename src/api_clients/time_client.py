import requests
from logger import get_logger

logger = get_logger()

class TimeClient:
    def __init__(self):
        self.base_url = "http://worldtimeapi.org/api/timezone"
    
    def get_time_data(self, timezone):
        """Obtiene datos de zona horaria"""
        try:
            url = f"{self.base_url}/{timezone}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"API Zona Horaria respondio para {timezone}")
            
            return {
                'hora_local': data['datetime'],
                'zona_horaria': data['timezone'],
                'utc_offset': data['utc_offset'],
                'diferencia_bogota': self._calculate_bogota_offset(data['utc_offset'])
            }
            
        except Exception as e:
            logger.error(f"Error API Zona Horaria {timezone}: {e}")
            return self._get_mock_time_data(timezone)
    
    def _calculate_bogota_offset(self, utc_offset):
        """Calcula diferencia horaria con Bogotá (-05:00)"""
        try:
            # Bogotá es UTC-5
            bogota_offset = -5
            
            # Convertir offset like "+01:00" to hours
            target_offset = int(utc_offset.split(':')[0])
            
            difference = target_offset - bogota_offset
            return f"{difference:+d} horas"
            
        except:
            return "N/A"
    
    def _get_mock_time_data(self, timezone):
        """Datos simulados cuando la API falla"""
        mock_data = {
            "America/New_York": {"utc_offset": "-04:00", "diferencia": "-1 horas"},
            "Europe/London": {"utc_offset": "+01:00", "diferencia": "+6 horas"},
            "Asia/Tokyo": {"utc_offset": "+09:00", "diferencia": "+14 horas"},
            "America/Sao_Paulo": {"utc_offset": "-03:00", "diferencia": "+2 horas"},
            "Australia/Sydney": {"utc_offset": "+11:00", "diferencia": "+16 horas"}
        }
        
        data = mock_data.get(timezone, {"utc_offset": "+00:00", "diferencia": "+5 horas"})
        return {
            'hora_local': '2024-12-10T10:30:00',
            'zona_horaria': timezone,
            'utc_offset': data['utc_offset'],
            'diferencia_bogota': data['diferencia']
        }