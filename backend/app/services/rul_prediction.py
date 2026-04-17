import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

class RULPredictionModel:
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)

    def train(self, data: pd.DataFrame, target_column: str) -> None:
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f"Model trained. Mean Squared Error: {mse}")

    def predict(self, input_data: np.ndarray) -> np.ndarray:
        return self.model.predict(input_data)
