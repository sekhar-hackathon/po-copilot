from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import os


class RULModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train(self, X_train, y_train):
        """
        Train the RUL prediction model.
        :param X_train: Training features.
        :param y_train: Training target.
        """
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test) -> float:
        """
        Evaluate the model and return the mean squared error.
        :param X_test: Test features.
        :param y_test: Test target.
        :return: Mean squared error of the model.
        """
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        return mse

    def save_model(self, file_path: str):
        """
        Save the trained model to a file.
        :param file_path: Path where the model will be saved.
        """
        joblib.dump(self.model, file_path)

    def load_model(self, file_path: str):
        """
        Load a model from a file.
        :param file_path: Path to the model file.
        """
        if os.path.exists(file_path):
            self.model = joblib.load(file_path)
        else:
            raise FileNotFoundError(f"Model file not found at {file_path}")
