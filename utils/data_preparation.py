import pandas as pd
import numpy as np

def calculate_indicators(data):
    """
    Calculate technical indicators and add them to the dataset.

    :param data: DataFrame containing historical data with 'Close' column
    :return: DataFrame with added features
    """
    # Calculate RSI
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data.loc[:, "RSI"] = 100 - (100 / (1 + rs))

    # Calculate EMA
    data.loc[:, "EMA"] = data["Close"].ewm(span=14, adjust=False).mean()

    # Calculate ATR
    high_low = data["High"] - data["Low"]
    high_close = np.abs(data["High"] - data["Close"].shift())
    low_close = np.abs(data["Low"] - data["Close"].shift())
    tr = high_low.combine(high_close, max).combine(low_close, max)
    data.loc[:, "ATR"] = tr.rolling(window=14).mean()

    # Calculate Bollinger Bands
    data.loc[:, "Bollinger_Mid"] = data["Close"].rolling(window=20).mean()
    data.loc[:, "Bollinger_Upper"] = data["Bollinger_Mid"] + 2 * data["Close"].rolling(window=20).std()
    data.loc[:, "Bollinger_Lower"] = data["Bollinger_Mid"] - 2 * data["Close"].rolling(window=20).std()

    return data

def generate_target(data):
    """
    Generate target column based on future price movement.

    :param data: DataFrame containing historical data with 'Close' column
    :return: DataFrame with a target column
    """
    data["Future_Close"] = data["Close"].shift(-1)  # Next period close
    data["target"] = np.where(data["Future_Close"] > data["Close"], 1, 0)  # Binary classification
    data.drop(columns=["Future_Close"], inplace=True)
    return data

def prepare_dataset(input_file, output_file):
    """
    Prepare dataset with features and target column.

    :param input_file: Path to input CSV file containing historical data
    :param output_file: Path to save the prepared dataset
    """
    try:
        # Load historical data
        data = pd.read_csv(input_file, parse_dates=["Date"])
        data.sort_values(by="Date", inplace=True)
        data.reset_index(drop=True, inplace=True)

        # Calculate indicators and generate target
        print("Calculating indicators...")
        data = calculate_indicators(data)
        print("Indicators calculated:", data.columns.tolist())

        print("Generating target column...")
        data = generate_target(data)
        print("Target column generated. Sample data:")
        print(data.head())

        # Drop rows with NaN values (from rolling calculations)
        data.dropna(inplace=True)

        # Save the prepared dataset
        data.to_csv(output_file, index=False)
        print(f"Prepared dataset saved to {output_file}")
    except Exception as e:
        print(f"Error preparing dataset: {str(e)}")

if __name__ == "__main__":
    # Example usage
    prepare_dataset(input_file="EURUSD_hourly_cleaned.csv", output_file="../training/training_data.csv")
