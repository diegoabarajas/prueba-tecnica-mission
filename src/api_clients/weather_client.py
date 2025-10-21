import requests
from logger import get_logger

logger = get_logger()

class WeatherClient:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather_data(self, lat, lon):
        """Obtiene datos climáticos para una ubicación"""
        try:
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,wind_speed_10m,precipitation,uv_index',
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
                'timezone': 'auto'
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            logger.info(f"API Clima respondió exitosamente")
            return response.json()
        except Exception as e:
            logger.error(f"Error API Clima: {e}")
            return None