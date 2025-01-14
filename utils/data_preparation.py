import pandas as pd
import os

class DataPreparer:
    def calculate_indicators(self, data):
        """
        Calculate technical indicators and add them to the dataset.
        """
        try:
            # RSI
            delta = data["close"].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
            rs = gain / loss
            data["RSI"] = 100 - (100 / (1 + rs))

            # EMA
            data["EMA"] = data["close"].ewm(span=14, adjust=False).mean()

            # ATR
            high_low = data["high"] - data["low"]
            high_close = abs(data["high"] - data["close"].shift())
            low_close = abs(data["low"] - data["close"].shift())
            tr = high_low.combine(high_close, max).combine(low_close, max)
            data["ATR"] = tr.rolling(window=14).mean()

            # Bollinger Bands
            data["Bollinger_Mid"] = data["close"].rolling(window=20).mean()
            data["Bollinger_Upper"] = data["Bollinger_Mid"] + 2 * data["close"].rolling(window=20).std()
            data["Bollinger_Lower"] = data["Bollinger_Mid"] - 2 * data["close"].rolling(window=20).std()

        except Exception as e:
            print(f"Error calculating indicators: {e}")
        return data

    def prepare_all(self):
        """
        Prepare all datasets in the input directory.
        """
        for file in os.listdir(self.input_dir):
            if file.endswith(".csv"):
                filepath = os.path.join(self.input_dir, file)
                try:
                    data = pd.read_csv(filepath)

                    # Ensure columns exist and convert types
                    if "Datetime" in data.columns:
                        data.rename(columns={"Datetime": "date"}, inplace=True)
                    if "Date" in data.columns:
                        data.rename(columns={"Date": "date"}, inplace=True)

                    # Ensure numeric conversion
                    for col in ["open", "high", "low", "close"]:
                        data[col] = pd.to_numeric(data[col], errors="coerce")

                    # Convert 'date' column to datetime
                    data["date"] = pd.to_datetime(data["date"])

                    # Calculate indicators and drop rows with NaN
                    data = self.calculate_indicators(data)
                    data.dropna(inplace=True)

                    # Save prepared data
                    output_path = os.path.join(self.output_dir, file)
                    data.to_csv(output_path, index=False)
                    print(f"Prepared data saved to {output_path}")
                except Exception as e:
                    print(f"Error preparing {file}: {e}")

