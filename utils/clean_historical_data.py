import os
import pandas as pd

class HistoricalDataCleaner:
    def __init__(self, input_dir="data", output_dir="cleaned_data"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def clean_file(self, file_path):
        try:
            print(f"Cleaning file: {file_path}...")
            df = pd.read_csv(file_path)

            # Ensure proper column names
            expected_columns = {"time": "date", "open": "open", "high": "high", "low": "low", "close": "close"}
            df.rename(columns=expected_columns, inplace=True)

            # Parse the date column
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

            # Drop rows with missing dates or prices
            df.dropna(subset=["date", "open", "high", "low", "close"], inplace=True)

            # Sort by date
            df.sort_values(by="date", inplace=True)

            # Save the cleaned file
            output_file = os.path.join(self.output_dir, os.path.basename(file_path))
            df.to_csv(output_file, index=False)
            print(f"Cleaned data saved to {output_file}")
        except Exception as e:
            print(f"Error cleaning {file_path}: {e}")

    def clean_all_files(self):
        for file_name in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, file_name)
            if os.path.isfile(file_path):
                self.clean_file(file_path)

if __name__ == "__main__":
    cleaner = HistoricalDataCleaner(input_dir="data", output_dir="cleaned_data")
    cleaner.clean_all_files()
