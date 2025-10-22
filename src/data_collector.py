from logger import get_logger
from api_clients.weather_client import WeatherClient
from api_clients.exchange_client import ExchangeClient
from datetime import datetime, timezone
from api_clients.time_client import TimeClient

logger = get_logger()

CIUDADES = [
    {"nombre": "Nueva York", "lat": 40.7128, "lon": -74.0060, "moneda": "USD", "timezone": "America/New_York"},
    {"nombre": "Londres", "lat": 51.5074, "lon": -0.1278, "moneda": "GBP", "timezone": "Europe/London"},
    {"nombre": "Tokio", "lat": 35.6762, "lon": 139.6503, "moneda": "JPY", "timezone": "Asia/Tokyo"},
    {"nombre": "São Paulo", "lat": -23.5505, "lon": -46.6333, "moneda": "BRL", "timezone": "America/Sao_Paulo"},
    {"nombre": "Sídney", "lat": -33.8688, "lon": 151.2093, "moneda": "AUD", "timezone": "Australia/Sydney"}
]

class DataCollector:
    def __init__(self):
        self.weather_client = WeatherClient()
        self.exchange_client = ExchangeClient()
        self.time_client = TimeClient()
    
    def collect_city_data(self, ciudad):
        """Recolecta datos para una ciudad especifica"""
        logger.info(f"Recolectando datos para {ciudad['nombre']}")
        
        weather_data = self.weather_client.get_weather_data(ciudad['lat'], ciudad['lon'])
        
        if weather_data:
            timestamp_actual = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
            
            return {
                'ciudad': ciudad['nombre'],
                'clima': weather_data,
                'timestamp': timestamp_actual
            }
        return None

    def collect_exchange_data(self, moneda):
        """Recolecta datos de tipo de cambio para una moneda"""
        try:
            rates = self.exchange_client.get_exchange_rates()
            history = self.exchange_client.get_exchange_history()
            trends = self.exchange_client.analyze_trend(history)
            
            return {
                'tipo_cambio_actual': rates.get(moneda, 1.0),
                'variacion_diaria': trends.get(moneda, {}).get('variacion_diaria', 0),
                'tendencia_5_dias': trends.get(moneda, {}).get('tendencia', 'estable'),
                'es_volatil': trends.get(moneda, {}).get('volatil', False)
            }
        except Exception as e:
            logger.error(f"Error recolectando datos de cambio para {moneda}: {e}")
            return None
    
    def collect_time_data(self, timezone):
        """Recolecta datos de zona horaria"""
        try:
            return self.time_client.get_time_data(timezone)
        except Exception as e:
            logger.error(f"Error recolectando datos de tiempo para {timezone}: {e}")
            return None