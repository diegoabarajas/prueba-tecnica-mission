# Sistema RPA TravelCorp - Mission SAS

Sistema de automatización para monitoreo de condiciones de viaje corporativo.

## Características

- Monitoreo de 5 ciudades: Nueva York, Londres, Tokio, São Paulo, Sídney
- 3 APIs integradas: Clima (Open-Meteo), Tipos de Cambio (ExchangeRate), Zonas Horarias (WorldTimeAPI)
- Dashboard interactivo: Streamlit con visualizaciones en tiempo real
- Ejecución automática: Scheduler cada 30 minutos
- Sistema de alertas: Temperatura, viento, precipitación, UV
- Índice de Viabilidad (IVV): Cálculo automático con niveles de riesgo
- Reportes automáticos: Generación de JSON/CSV

## Instalación

```bash
# Clonar repositorio
git clone <url-repositorio>
cd prueba-tecnica-rpa-travelcorp

# Entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## Uso
Ejecusion manual
```bash
python src/main.py
```

## Ejecusion autoamtica
scheduler
```bash
python src/scheduler.py
```

## Dashboard web

```bash
streamlit run src/dashboard/app.py
```

## APIs Integradas
-> Open-Meteo: Datos climáticos en tiempo real
-> ExchangeRate-API: Tipos de cambio y tendencias
-> WorldTimeAPI: Zonas horarias y diferencias

## Estructura del Proyecto

src/
├── api_clients/          # Clientes de APIs
├── dashboard/            # Visualización Streamlit
├── data_collector.py     # Recolector de datos
├── processor.py          # Lógica de negocio y alertas
├── output_generator.py   # Generador de reportes
├── scheduler.py          # Automatización
├── logger.py             # Sistema de logging
├── config.py             # Configuración
└── main.py              # Punto de entrada

## Salidas del Sistema

-> JSON estructurado: Datos completos de todas las ciudades
-> CSV resumido: Métricas clave para análisis
-> Logs detallados: Trazabilidad completa del sistema
-> Dashboard web: Visualización interactiva

## Sistema de Alertas

-> Temperatura >35°C o <0°C
-> Viento >50 km/h
-> Precipitación alta
-> Índice UV >8

## Cálculo del IVV

IVV = (Clima_Score * 0.4) + (Cambio_Score * 0.3) + (UV_Score * 0.3)

Donde:
-> Clima_Score: 100 - (alertas_climaticas * 25)
-> Cambio_Score: 100 si estable, 50 si volátil
-> UV_Score: 100 si UV <6, 75 si UV 6-8, 50 si UV >8

## Niveles de Riesgo

->> 80-100: BAJO (Verde) - Condiciones óptimas
->> 60-79: MEDIO (Amarillo) - Precaución recomendada
->> 40-59: ALTO (Naranja) - Considerar postergar
->> 0-39: CRÍTICO (Rojo) - No recomendado viajar