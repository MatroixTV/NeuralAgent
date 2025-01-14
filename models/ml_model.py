import pickle
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

class MLModel:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "ml_model.pkl")
        self.model = None
        self.feature_names = None  # To track feature names during training

    def train(self, data):
        """
        Train the ML model using the provided data.
        """
        print("Training the model...")
        # Prepare features and target
        features = data.drop(columns=["target", "Date"])  # Exclude target and Date
        self.feature_names = features.columns.tolist()  # Save feature names
        target = data["target"]

        # Check dataset size
        if len(features) < 2:
            raise ValueError("Insufficient data for training. Provide a dataset with at least 2 samples.")

        # Train-test split
        if len(features) > 5:  # Split if enough samples are available
            X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        else:  # Use the entire dataset if it's small
            print("Dataset is small; using entire data for training.")
            X_train, X_test, y_train, y_test = features, features, target, target

        # Train the RandomForest model
        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, predictions)}")
        print(f"Classification Report:\n{classification_report(y_test, predictions)}")

    def save_model(self, model_path=None):
        """
        Save the trained model to a file.
        """
        path = model_path or self.model_path
        with open(path, "wb") as file:
            pickle.dump(self.model, file)
        print(f"Model saved to {path}")

    def load_model(self, model_path=None):
        """
        Load the trained model from a file.
        """
        path = model_path or self.model_path
        with open(path, "rb") as file:
            self.model = pickle.load(file)
        print("Model loaded successfully.")

        # Check if feature names are available
        if hasattr(self.model, "feature_names_in_"):
            self.feature_names = self.model.feature_names_in_
        else:
            raise ValueError(
                "The loaded model does not have feature names. Ensure the model was trained with proper feature tracking."
            )

    def get_feature_names(self):
        """
        Get the feature names used during training.
        """
        if not self.feature_names:
            raise ValueError("Feature names are not available. Train the model first.")
        return self.feature_names

    def predict(self, features):
        """
        Make predictions using the trained model.
        """
        if self.model is None:
            raise ValueError("Model is not loaded. Load or train the model first.")
        return self.model.predict(features)

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
