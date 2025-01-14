import os
import pandas as pd
from utils.clean_historical_data import HistoricalDataCleaner

class DataPreparer:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def clean_and_prepare(self, file_path):
        try:
            # Step 1: Clean the data
            cleaner = HistoricalDataCleaner(input_dir=self.input_dir, output_dir="cleaned_temp")
            cleaner.clean_file(file_path)
            cleaned_file = os.path.join("cleaned_temp", os.path.basename(file_path))
            cleaned_data = pd.read_csv(cleaned_file)

            # Step 2: Calculate indicators
            print(f"Calculating indicators for {file_path}...")
            cleaned_data["RSI"] = self.calculate_rsi(cleaned_data["close"], period=14)
            cleaned_data["EMA"] = cleaned_data["close"].ewm(span=14, adjust=False).mean()

            # Save the prepared data
            output_file = os.path.join(self.output_dir, os.path.basename(file_path))
            cleaned_data.to_csv(output_file, index=False)
            print(f"Prepared data saved to {output_file}")
        except Exception as e:
            print(f"Error preparing {file_path}: {e}")

    def calculate_rsi(self, prices, period):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def prepare_all(self):
        for file_name in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, file_name)
            print(f"Preparing {file_path}...")
            self.clean_and_prepare(file_path)

if __name__ == "__main__":
    input_dir = "data"
    output_dir = "prepared_data"
    preparer = DataPreparer(input_dir=input_dir, output_dir=output_dir)
    preparer.prepare_all()
