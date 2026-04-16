import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

class RULPredictiveModel:
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_val)
        mse = mean_squared_error(y_val, predictions)
        print(f"Validation MSE: {mse}")

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

    def save_model(self, file_path: str) -> None:
        joblib.dump(self.model, file_path)

    def load_model(self, file_path: str) -> None:
        self.model = joblib.load(file_path)
