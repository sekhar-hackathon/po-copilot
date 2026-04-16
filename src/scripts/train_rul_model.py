import pandas as pd
from models.rul_predictive_model import RULPredictiveModel

# Load your dataset
# For demonstration, we assume a CSV file with features and RUL as the target
DATA_PATH = 'data/bearing_data.csv'
MODEL_PATH = 'models/rul_model.pkl'

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def main():
    data = load_data(DATA_PATH)
    X = data.drop(columns=['RUL'])
    y = data['RUL']

    model = RULPredictiveModel()
    model.train(X, y)
    model.save_model(MODEL_PATH)

if __name__ == '__main__':
    main()
