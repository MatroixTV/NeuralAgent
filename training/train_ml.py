from models.ml_model import MLModel
import pandas as pd

def main():
    # Load historical data
    try:
        data = pd.read_csv("training_data.csv")  # Replace with your data file
        ml_model = MLModel()
        ml_model.train(data)
    except Exception as e:
        print("Error during training:", str(e))

if __name__ == "__main__":
    main()
