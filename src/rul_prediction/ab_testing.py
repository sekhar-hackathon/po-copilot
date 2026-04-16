import numpy as np


def ab_test(current_model_mse: float, new_model_mse: float, threshold: float = 0.05) -> bool:
    """
    Perform A/B testing to compare the current and new model.
    :param current_model_mse: Mean squared error of the current model.
    :param new_model_mse: Mean squared error of the new model.
    :param threshold: Improvement threshold to consider the new model better.
    :return: True if the new model is better, False otherwise.
    """
    improvement = current_model_mse - new_model_mse
    relative_improvement = improvement / current_model_mse
    return relative_improvement > threshold
