import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class RULModelPrototype:
    def __init__(self):
        self.model_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', LinearRegression())
        ])

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model_pipeline.fit(X_train, y_train)
        predictions = self.model_pipeline.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print(f'Model trained. Test MSE: {mse}')

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model_pipeline.predict(X)
