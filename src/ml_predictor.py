# src/ml_predictor.py
import pandas as pd
import numpy as np
import os
import glob
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from logger import get_logger

logger = get_logger()

class IVVPredictor:
    """
    Predice el IVV futuro y detecta anomalías usando datos históricos generados por el sistema.
    """

    def __init__(self, data_path="data/outputs"):
        self.data_path = data_path

    def _load_data(self):
        """Carga los archivos CSV históricos generados por el sistema."""
        try:
            csv_files = glob.glob(os.path.join(self.data_path, "resumen_ciudades_*.csv"))
            if not csv_files:
                logger.warning("No se encontraron archivos CSV históricos en data/outputs.")
                return None

            df_list = [pd.read_csv(f) for f in csv_files]
            df = pd.concat(df_list, ignore_index=True)
            logger.info(f"Datos históricos cargados correctamente: {len(df)} registros totales.")
            return df
        except Exception as e:
            logger.error(f"Error cargando datos históricos: {e}")
            return None

    def predict_ivv(self):
        """
        Predice el IVV futuro simple para cada ciudad usando regresión lineal.
        Retorna un diccionario {ciudad: IVV_predicho}.
        """
        df = self._load_data()
        if df is None:
            return {}

        preds = {}
        for city in df["Ciudad"].unique():
            sub = df[df["Ciudad"] == city].reset_index(drop=True)
            if len(sub) < 2:
                continue  # No hay suficientes datos históricos

            X = np.arange(len(sub)).reshape(-1, 1)
            y = sub["IVV_Score"]

            model = LinearRegression()
            model.fit(X, y)
            future_ivv = model.predict([[len(sub)]])[0]
            # Limitar los valores predichos al rango 0–100
            future_ivv = max(0, min(future_ivv, 100))
            preds[city] = round(float(future_ivv), 2)


        logger.info(f"Predicciones generadas para {len(preds)} ciudades.")
        return preds

    def detect_anomalies(self):
        """
        Detecta ciudades con valores anómalos de IVV usando Isolation Forest.
        """
        df = self._load_data()
        if df is None:
            return pd.DataFrame()

        model = IsolationForest(contamination=0.2, random_state=42)
        df["anomaly_flag"] = model.fit_predict(df[["IVV_Score"]])
        anomalies = df[df["anomaly_flag"] == -1][["Ciudad", "IVV_Score", "Nivel_Riesgo"]]

        if anomalies.empty:
            logger.info("No se detectaron anomalías en el IVV.")
        else:
            logger.warning(f"Se detectaron {len(anomalies)} anomalías en el IVV.")

        return anomalies


if __name__ == "__main__":
    print("=== PREDICTOR DE IVV ===")
    predictor = IVVPredictor()

    preds = predictor.predict_ivv()
    print("\n Predicción de IVV futuro por ciudad:")
    for city, ivv in preds.items():
        print(f"{city}: {ivv}")

    anomalias = predictor.detect_anomalies()
    print("\n Ciudades con comportamiento anómalo:")
    print(anomalias if not anomalias.empty else "Ninguna detectada")
