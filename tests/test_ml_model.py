import pytest
from models.ml_model import MLModel
import pandas as pd

@pytest.fixture
def test_data():
    # Load test data
    return pd.read_csv("C:/Users/ismac/PycharmProjects/NeuralAgent/training/training_data.csv")

def test_ml_model_predictions(test_data):
    """
    Test the predictions of the trained ML model.
    """
    # Exclude target column
    features = test_data.drop(columns=["target", "Date"])

    # Load the trained model
    ml_model = MLModel()
    ml_model.load_model()

    # Make predictions
    predictions = ml_model.predict(features)

    # Assert that predictions are made
    assert predictions is not None, "Predictions should not be None"
    assert len(predictions) > 0, "Predictions should not be empty"

    # Print a sample of predictions
    print("Sample Predictions:", predictions[:10])
