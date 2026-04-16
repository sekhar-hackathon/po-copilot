import schedule
import time
from datetime import datetime
from .data_preprocessing import load_and_preprocess_data
from .model import RULModel
from .ab_testing import ab_test


def retrain_model():
    """
    Retrain the RUL prediction model monthly.
    """
    # Load and preprocess data
    X_train, X_test, y_train, y_test = load_and_preprocess_data('data/rul_data.csv')
    
    # Load current model
    model = RULModel()
    try:
        model.load_model('models/current_rul_model.pkl')
    except FileNotFoundError:
        print("No existing model found. Training a new model.")

    # Train new model
    new_model = RULModel()
    new_model.train(X_train, y_train)
    new_mse = new_model.evaluate(X_test, y_test)

    # Evaluate current model
    current_mse = model.evaluate(X_test, y_test)

    # A/B test
    if ab_test(current_mse, new_mse):
        print("New model is better. Updating the current model.")
        new_model.save_model('models/current_rul_model.pkl')
    else:
        print("Current model is still better.")


def schedule_monthly_retraining():
    """
    Schedule the retraining of the model every month.
    """
    schedule.every().month.do(retrain_model)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    print(f"Starting model retraining scheduler at {datetime.now()}")
    schedule_monthly_retraining()
