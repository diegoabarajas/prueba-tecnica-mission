from logger import get_logger
from datetime import datetime

logger = get_logger()

class DataProcessor:
    def __init__(self):
        self.logger = get_logger()
    
    def evaluate_alerts(self, ciudad, clima_data):
        """Evalúa y genera alertas basadas en los datos climáticos"""
        alertas = []
        current = clima_data['current']
        
        # 1. Alerta por temperatura crítica
        if current['temperature_2m'] > 35 or current['temperature_2m'] < 0:
            alertas.append({
                'tipo': 'CLIMA',
                'severidad': 'ALTA',
                'mensaje': f"Temperatura crítica: {current['temperature_2m']}°C"
            })
        
        # 2. Alerta por probabilidad de lluvia alta
        if current['precipitation'] > 5:
            alertas.append({
                'tipo': 'CLIMA', 
                'severidad': 'MEDIA',
                'mensaje': f"Precipitación alta: {current['precipitation']}mm"
            })
        
        # 3. Alerta por viento fuerte
        if current['wind_speed_10m'] > 50:
            alertas.append({
                'tipo': 'CLIMA',
                'severidad': 'ALTA', 
                'mensaje': f"Viento fuerte: {current['wind_speed_10m']} km/h"
            })
        
        # 4. Alerta por UV alto
        if current['uv_index'] > 8:
            alertas.append({
                'tipo': 'CLIMA',
                'severidad': 'MEDIA',
                'mensaje': f"Índice UV muy alto: {current['uv_index']}"
            })
            
        return alertas
    
    def calculate_ivv(self, alertas, uv_index, cambio_estable=True):
        """Calcula el Índice de Viabilidad de Viaje (IVV)"""
        # Clima_Score: 100 - (alertas_climaticas * 25)
        clima_score = 100 - (len(alertas) * 25)
        clima_score = max(0, clima_score)
        
        # Cambio_Score: 100 si estable, 50 si volátil
        cambio_score = 100 if cambio_estable else 50
        
        # UV_Score: 100 si UV < 6, 75 si UV 6-8, 50 si UV > 8
        if uv_index < 6:
            uv_score = 100
        elif uv_index <= 8:
            uv_score = 75
        else:
            uv_score = 50
        
        # IVV = (Clima_Score * 0.4) + (Cambio_Score * 0.3) + (UV_Score * 0.3)
        ivv = (clima_score * 0.4) + (cambio_score * 0.3) + (uv_score * 0.3)
        
        # Determinar nivel de riesgo
        if ivv >= 80:
            nivel_riesgo = "BAJO"
        elif ivv >= 60:
            nivel_riesgo = "MEDIO" 
        elif ivv >= 40:
            nivel_riesgo = "ALTO"
        else:
            nivel_riesgo = "CRÍTICO"
            
        return {
            'ivv_score': round(ivv, 1),
            'nivel_riesgo': nivel_riesgo,
            'componentes_ivv': {
                'clima_score': clima_score,
                'cambio_score': cambio_score,
                'uv_score': uv_score
            }
        }