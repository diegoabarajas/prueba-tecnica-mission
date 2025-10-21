import json
import csv
import os
from datetime import datetime
from logger import get_logger

logger = get_logger()

class OutputGenerator:
    def __init__(self):
        self.output_dir = "data/outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_json(self, datos_ciudades):
        """Genera archivo JSON con estructura requerida"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/reporte_ciudades_{timestamp}.json"
            
            output_data = []
            
            for ciudad_data in datos_ciudades:
                ciudad_output = {
                    "timestamp": ciudad_data['datos']['timestamp'],
                    "ciudad": ciudad_data['ciudad'],
                    "clima": {
                        "temperatura_actual": ciudad_data['datos']['clima']['current']['temperature_2m'],
                        "pronostico_7_dias": self._get_7day_forecast(ciudad_data['datos']['clima']),
                        "precipitacion": ciudad_data['datos']['clima']['current']['precipitation'],
                        "viento": ciudad_data['datos']['clima']['current']['wind_speed_10m'],
                        "uv": ciudad_data['datos']['clima']['current']['uv_index']
                    },
                    "finanzas": {
                        "tipo_cambio_actual": ciudad_data['exchange_data']['tipo_cambio_actual'],
                        "variacion_diaria": ciudad_data['exchange_data']['variacion_diaria'],
                        "tendencia_5_dias": ciudad_data['exchange_data']['tendencia_5_dias']
                    },
                    "alertas": ciudad_data['alertas'],
                    "ivv_score": ciudad_data['ivv_data']['ivv_score'],
                    "nivel_riesgo": ciudad_data['ivv_data']['nivel_riesgo'],
                    "componentes_ivv": ciudad_data['ivv_data']['componentes_ivv']
                }
                output_data.append(ciudad_output)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"JSON generado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error generando JSON: {e}")
            return None
    
    def _get_7day_forecast(self, clima_data):
        """Extrae pronostico de 7 dias de los datos de la API"""
        try:
            forecast = []
            daily = clima_data.get('daily', {})
            
            if daily and 'time' in daily:
                for i in range(min(7, len(daily['time']))):
                    day_forecast = {
                        "fecha": daily['time'][i],
                        "temp_max": daily['temperature_2m_max'][i] if 'temperature_2m_max' in daily else 0,
                        "temp_min": daily['temperature_2m_min'][i] if 'temperature_2m_min' in daily else 0,
                        "precipitacion": daily['precipitation_probability_max'][i] if 'precipitation_probability_max' in daily else 0
                    }
                    forecast.append(day_forecast)
            
            return forecast
        except Exception as e:
            logger.error(f"Error procesando pronostico: {e}")
            return []
    
    def generate_csv(self, datos_ciudades):
        """Genera archivo CSV resumen"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.output_dir}/resumen_ciudades_{timestamp}.csv"
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Ciudad', 'Timestamp', 'Temperatura', 'Viento', 'Precipitacion', 
                    'UV', 'Tipo_Cambio', 'Variacion', 'Tendencia', 
                    'IVV_Score', 'Nivel_Riesgo', 'Alertas_Count'
                ])
                
                for ciudad_data in datos_ciudades:
                    writer.writerow([
                        ciudad_data['ciudad'],
                        ciudad_data['datos']['timestamp'],
                        ciudad_data['datos']['clima']['current']['temperature_2m'],
                        ciudad_data['datos']['clima']['current']['wind_speed_10m'],
                        ciudad_data['datos']['clima']['current']['precipitation'],
                        ciudad_data['datos']['clima']['current']['uv_index'],
                        ciudad_data['exchange_data']['tipo_cambio_actual'],
                        ciudad_data['exchange_data']['variacion_diaria'],
                        ciudad_data['exchange_data']['tendencia_5_dias'],
                        ciudad_data['ivv_data']['ivv_score'],
                        ciudad_data['ivv_data']['nivel_riesgo'],
                        len(ciudad_data['alertas'])
                    ])
            
            logger.info(f"CSV generado: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error generando CSV: {e}")
            return None