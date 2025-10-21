import requests
from logger import get_logger
import random
from datetime import datetime, timedelta

logger = get_logger()

class ExchangeClient:
    def __init__(self):
        self.base_url = "https://api.exchangerate-api.com/v4/latest/USD"
    
    def get_exchange_rates(self):
        """Obtiene tipos de cambio actuales USD a otras monedas"""
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            logger.info("API Exchange Rates respondio exitosamente")
            return data['rates']
            
        except Exception as e:
            logger.error(f"Error API Exchange Rates: {e}")
            logger.info("Usando datos simulados...")
            return self._get_mock_rates()
    
    def _get_mock_rates(self):
        """Datos simulados cuando la API falla"""
        return {
            'USD': 1.0,
            'GBP': 0.78,
            'JPY': 149.50,
            'BRL': 5.45,
            'AUD': 1.55
        }
    
    def get_exchange_history(self, days=5):
        """Simula historico de 5 dias con variacion ±2%"""
        history = {}
        today_rates = self.get_exchange_rates()
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            day_rates = {}
            
            for currency, rate in today_rates.items():
                variation = random.uniform(-0.02, 0.02)
                day_rates[currency] = round(rate * (1 + variation), 4)
            
            history[date] = day_rates
        
        return history
    
    def analyze_trend(self, history):
        """Analiza tendencia de los ultimos 5 dias"""
        currencies = list(history.values())[0].keys()
        trends = {}
        
        for currency in currencies:
            rates = [day_rates[currency] for day_rates in history.values()]
            
            daily_changes = []
            for i in range(1, len(rates)):
                change = ((rates[i] - rates[i-1]) / rates[i-1]) * 100
                daily_changes.append(change)
            
            if len(daily_changes) >= 3 and all(change < 0 for change in daily_changes[-3:]):
                trend = "negativa"
            elif len(daily_changes) >= 3 and all(change > 0 for change in daily_changes[-3:]):
                trend = "positiva" 
            else:
                trend = "estable"
            
            last_change = daily_changes[-1] if daily_changes else 0
            
            trends[currency] = {
                'tendencia': trend,
                'variacion_diaria': round(last_change, 2),
                'volatil': abs(last_change) > 3
            }
        
        return trends