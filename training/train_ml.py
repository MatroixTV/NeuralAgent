from models.ml_model import MLModel
import pandas as pd

def main():
    # Load historical data
    try:
        data = pd.read_csv("training_data.csv")  # Replace with your data file
        if len(data) < 50:  # Minimum threshold
            raise ValueError("Insufficient data for training. Please collect more data.")
        ml_model = MLModel()
        ml_model.train(data)

        # Save the model
        ml_model.model.feature_names_in_ = ml_model.feature_names  # Attach feature names to the model
        ml_model.save_model("models/ml_model.pkl")
        print("Model training and saving completed successfully.")
    except Exception as e:
        print("Error during training:", str(e))

if __name__ == "__main__":
    main()
