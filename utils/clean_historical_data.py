import pandas as pd

def clean_data(input_file, output_file):
    """
    Cleans historical Forex data to ensure compatibility with backtesting.

    :param input_file: Path to the raw CSV file
    :param output_file: Path to save the cleaned CSV file
    """
    try:
        # Load the raw data
        data = pd.read_csv(input_file)

        # Display original column names for debugging
        print("Original Columns:", data.columns)

        # Rename columns to standard format
        data = data.rename(columns={
            "date": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close"
        })

        # Ensure the Date column is properly formatted
        if "Date" in data.columns:
            data["Date"] = pd.to_datetime(data["Date"])
        else:
            raise ValueError("The input file is missing the 'Date' column.")

        # Sort data by date (ascending)
        data = data.sort_values(by="Date")

        # Remove any rows with missing or invalid data
        data = data.dropna()

        # Save the cleaned data to a new file
        data.to_csv(output_file, index=False)
        print(f"Cleaned data saved to {output_file}")
    except Exception as e:
        print(f"Error during cleaning: {e}")

if __name__ == "__main__":
    # Specify input and output file paths
    input_file = "EURUSD_daily.csv"
    output_file = "EURUSD_daily_cleaned.csv"

    # Run the cleaning function
    clean_data(input_file, output_file)
