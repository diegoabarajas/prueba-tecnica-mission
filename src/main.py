from logger import get_logger
from data_collector import DataCollector, CIUDADES
from processor import DataProcessor
from output_generator import OutputGenerator

logger = get_logger()

def main():
    logger.info("Iniciando sistema RPA TravelCorp - Procesando 5 ciudades")
    
    collector = DataCollector()
    processor = DataProcessor()
    
    resultados = []
    
    for ciudad in CIUDADES:
        logger.info(f"Procesando ciudad: {ciudad['nombre']}")
        
        datos = collector.collect_city_data(ciudad)
        
        if datos:
            exchange_data = collector.collect_exchange_data(ciudad['moneda'])
            
            alertas = processor.evaluate_alerts(ciudad, datos['clima'])
            
            # Usar datos reales de exchange para el calculo de IVV
            cambio_estable = exchange_data['tendencia_5_dias'] == 'estable' if exchange_data else True
            
            ivv_data = processor.calculate_ivv(
                alertas, 
                datos['clima']['current']['uv_index'],
                cambio_estable=cambio_estable
            )
            
            resultado_ciudad = {
                'ciudad': ciudad['nombre'],
                'datos': datos,
                'exchange_data': exchange_data,
                'alertas': alertas,
                'ivv_data': ivv_data
            }
            
            resultados.append(resultado_ciudad)
            
            # Mostrar resultados por ciudad
            current = datos['clima']['current']
            print(f"\n--- {ciudad['nombre']} ---")
            print(f"Temperatura: {current['temperature_2m']}C")
            print(f"Viento: {current['wind_speed_10m']} km/h")
            print(f"Precipitacion: {current['precipitation']} mm")
            print(f"UV: {current['uv_index']}")
            
            if exchange_data:
                print(f"Tipo cambio: 1 USD = {exchange_data['tipo_cambio_actual']} {ciudad['moneda']}")
                print(f"Variacion: {exchange_data['variacion_diaria']}%")
                print(f"Tendencia: {exchange_data['tendencia_5_dias']}")
            
            print(f"Alertas: {len(alertas)}")
            for alerta in alertas:
                print(f"  - {alerta['severidad']}: {alerta['mensaje']}")
                
            print(f"IVV: {ivv_data['ivv_score']} ({ivv_data['nivel_riesgo']})")
            
        else:
            logger.error(f"Fallo la recoleccion para {ciudad['nombre']}")
    
    # Resumen final
    print(f"\n=== RESUMEN EJECUCION ===")
    print(f"Ciudades procesadas: {len(resultados)}/{len(CIUDADES)}")
    
    for resultado in resultados:
        print(f"{resultado['ciudad']}: IVV {resultado['ivv_data']['ivv_score']} ({resultado['ivv_data']['nivel_riesgo']}) - Alertas: {len(resultado['alertas'])}")

    # Generar archivos de output
    output_gen = OutputGenerator()
    json_file = output_gen.generate_json(resultados)
    csv_file = output_gen.generate_csv(resultados)

    if json_file and csv_file:
        print(f"Archivos generados exitosamente:")
        print(f"JSON: {json_file}")
        print(f"CSV: {csv_file}")

if __name__ == "__main__":
    main()