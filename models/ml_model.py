import pandas as pd
import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

class MLModel:
    def __init__(self):
        # Save models in the same directory as this script
        self.model_path = os.path.join(os.path.dirname(__file__), "ml_model.pkl")
        self.model = None

    def prepare_data(self, data):
        """
        Prepares data for training and testing.

        :param data: DataFrame containing features and target
        :return: X_train, X_test, y_train, y_test
        """
        # Exclude the 'Date' column from features
        features = data.drop(columns=["target", "Date"])  # Exclude 'Date'
        target = data["target"]
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train(self, data):
        """
        Train the machine learning model.

        :param data: DataFrame containing features and target
        """
        X_train, X_test, y_train, y_test = self.prepare_data(data)

        print("Training the model...")
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, predictions))
        print("Classification Report:\n", classification_report(y_test, predictions))

        # Save the trained model
        self.save_model()
        print("Model training completed and saved.")

    def save_model(self):
        """
        Save the trained model to disk.
        """
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)  # Ensure directory exists
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        """
        Load the trained model from disk.
        """
        try:
            self.model = joblib.load(self.model_path)
            print("Model loaded successfully.")
        except FileNotFoundError:
            print(f"No trained model found at {self.model_path}. Please train the model first.")

    def predict(self, features):
        """
        Make predictions with the trained model.

        :param features: DataFrame or array of features
        :return: Predictions
        """
        if self.model is None:
            print("Model not loaded. Please load or train the model first.")
            return None

        predictions = self.model.predict(features)
        return predictions

if __name__ == "__main__":
    # Example usage
    # Assuming data.csv has features and a 'target' column
    try:
        data = pd.read_csv("C:/Users/ismac/PycharmProjects/NeuralAgent/training/training_data.csv")
        ml_model = MLModel()
        ml_model.train(data)

        # Example prediction
        sample_features = data.drop(columns=["target"]).iloc[:5]
        predictions = ml_model.predict(sample_features)
        print("Sample Predictions:", predictions)
    except Exception as e:
        print("Error:", str(e))
