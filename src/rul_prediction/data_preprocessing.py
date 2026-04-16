import pandas as pd
from sklearn.model_selection import train_test_split


def load_and_preprocess_data(file_path: str) -> tuple:
    """
    Load and preprocess the data for RUL prediction.
    :param file_path: Path to the CSV file containing the data.
    :return: Tuple of train and test data.
    """
    data = pd.read_csv(file_path)
    # Assuming the data has a 'RUL' column for the target
    X = data.drop(columns=['RUL'])
    y = data['RUL']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
