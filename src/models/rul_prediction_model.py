import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

class RULPredictionModel:
    def __init__(self, alert_thresholds: dict):
        self.alert_thresholds = alert_thresholds
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train(self, data: pd.DataFrame, target_column: str):
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Model trained with MSE: {mse}")

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        return self.model.predict(data)

    def save_model(self, file_path: str):
        joblib.dump(self.model, file_path)

    def load_model(self, file_path: str):
        self.model = joblib.load(file_path)

    def check_alerts(self, predictions: np.ndarray, machine_type: str) -> list:
        threshold = self.alert_thresholds.get(machine_type, float('inf'))
        alerts = [i for i, pred in enumerate(predictions) if pred < threshold]
        return alerts
