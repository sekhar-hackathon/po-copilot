import unittest
from src.rul_prediction.model import RULModel
from src.rul_prediction.data_preprocessing import load_and_preprocess_data


class TestRULModel(unittest.TestCase):
    def setUp(self):
        # Load sample data
        self.X_train, self.X_test, self.y_train, self.y_test = load_and_preprocess_data('data/sample_rul_data.csv')
        self.model = RULModel()

    def test_train_and_evaluate(self):
        # Train the model
        self.model.train(self.X_train, self.y_train)
        # Evaluate the model
        mse = self.model.evaluate(self.X_test, self.y_test)
        self.assertIsInstance(mse, float)

    def test_save_and_load_model(self):
        # Train and save the model
        self.model.train(self.X_train, self.y_train)
        self.model.save_model('models/test_rul_model.pkl')
        # Load the model
        loaded_model = RULModel()
        loaded_model.load_model('models/test_rul_model.pkl')
        # Evaluate loaded model
        mse = loaded_model.evaluate(self.X_test, self.y_test)
        self.assertIsInstance(mse, float)


if __name__ == '__main__':
    unittest.main()
