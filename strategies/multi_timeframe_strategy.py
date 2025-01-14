import pandas as pd
from models.ml_model import MLModel


class MultiTimeframeStrategy:
    def __init__(self, symbol, model_path="models/ml_model.pkl"):
        self.symbol = symbol
        self.model = MLModel()
        self.model.load_model(model_path)

    def generate_signal(self, data_dict):
        """
        Generate a signal by analyzing multiple timeframes.
        :param data_dict: Dictionary of DataFrames for each timeframe
        :return: Aggregated signal ('buy', 'sell', 'hold')
        """
        signals = {}
        for timeframe, data in data_dict.items():
            print(f"Analyzing {self.symbol} ({timeframe})...")

            if not isinstance(data, pd.DataFrame) or data.empty:
                print(f"No valid data for {timeframe}. Skipping.")
                signals[timeframe] = "hold"
                continue

            # Prepare features
            features = data.drop(columns=["date", "target"], errors="ignore")
            try:
                signal = self.model.predict(features.tail(1))[0]  # Use last row for prediction
                signals[timeframe] = signal
            except Exception as e:
                print(f"Error generating signal for {timeframe}: {e}")
                signals[timeframe] = "hold"

        return self.aggregate_signals(signals)

    def aggregate_signals(self, signals):
        """
        Combine signals from multiple timeframes.
        :param signals: Dictionary of signals (e.g., {'1h': 'buy', '1d': 'sell'})
        :return: Aggregated signal ('buy', 'sell', 'hold')
        """
        buy_count = sum(1 for signal in signals.values() if signal == "buy")
        sell_count = sum(1 for signal in signals.values() if signal == "sell")

        if buy_count > sell_count:
            return "buy"
        elif sell_count > buy_count:
            return "sell"
        else:
            return "hold"
