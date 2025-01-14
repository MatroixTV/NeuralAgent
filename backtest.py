import os
import pandas as pd
from strategies.multi_timeframe_strategy import MultiTimeframeStrategy
import matplotlib.pyplot as plt

class Backtest:
    def __init__(self, symbol, timeframes, initial_balance=1000):
        self.symbol = symbol
        self.timeframes = timeframes
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.equity_curve = [initial_balance]
        self.trades = []

    def load_data(self, data_dir):
        """
        Load prepared data for all timeframes.
        :param data_dir: Directory containing prepared data
        :return: Dictionary of DataFrames for each timeframe
        """
        print("Checking prepared data files...")  # Debugging statement
        data_dict = {}

        for timeframe in self.timeframes:
            file_path = os.path.join(data_dir, f"{self.symbol}_{timeframe}.csv")

            # Debugging: Check if the file exists
            if os.path.exists(file_path):
                print(f"File found: {file_path}")
                try:
                    data = pd.read_csv(file_path)
                    data["date"] = pd.to_datetime(data["date"])  # Ensure correct datetime format
                    data_dict[timeframe] = data
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
            else:
                print(f"File missing: {file_path}")
                data_dict[timeframe] = None

        # Debugging output
        print(f"Data Dictionary Keys: {list(data_dict.keys())}")
        if not data_dict or all(value is None for value in data_dict.values()):
            raise ValueError(
                "Data dictionary is empty or contains only None. Ensure prepared data files are correct and exist."
            )
        return data_dict

    def run(self, strategy, data_dict):
        """
        Run backtest using the given strategy and data.
        :param strategy: Strategy object (e.g., MultiTimeframeStrategy)
        :param data_dict: Dictionary of DataFrames for each timeframe
        """
        print(f"Running backtest for {self.symbol}...")

        # Simulate trades
        for i in range(len(list(data_dict.values())[0])):  # Iterate over the shortest timeframe
            current_data = {tf: df.iloc[i:i + 1] for tf, df in data_dict.items() if df is not None}

            signal = strategy.generate_signal(current_data)  # Pass the current_data dictionary
            print(f"Generated Signal: {signal}")
            # Add trade execution logic here

            if signal == "buy":
                self.trades.append({"type": "buy", "price": current_data["1h"]["close"].iloc[-1]})
                print(f"Buy Signal at {current_data['1h']['date'].iloc[-1]}")
            elif signal == "sell" and self.trades:
                last_trade = self.trades.pop()
                if last_trade["type"] == "buy":
                    sell_price = current_data["1h"]["close"].iloc[-1]
                    profit = sell_price - last_trade["price"]
                    self.balance += profit
                    print(f"Sell Signal at {current_data['1h']['date'].iloc[-1]} (Profit: {profit:.2f})")
            self.equity_curve.append(self.balance)

        self.display_performance()

    def display_performance(self):
        """
        Display performance metrics and equity curve.
        """
        total_trades = len(self.trades)
        net_profit = self.balance - self.initial_balance
        print("\nPerformance Metrics:")
        print(f"Total Trades: {total_trades}")
        print(f"Final Balance: ${self.balance:.2f}")
        print(f"Net Profit: ${net_profit:.2f}")
        self.plot_equity_curve()

    def plot_equity_curve(self):
        """
        Plot the equity curve.
        """
        plt.figure(figsize=(12, 6))
        plt.plot(self.equity_curve, label="Equity Curve", color="blue")
        plt.title("Equity Curve")
        plt.xlabel("Trades")
        plt.ylabel("Balance")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    # Define symbol, timeframes, and data directory
    symbol = "EURUSD=X"
    timeframes = ["1h", "90m", "1d"]
    data_dir = "utils/utils/prepared_data"

    # Initialize backtest
    backtest = Backtest(symbol=symbol, timeframes=timeframes, initial_balance=1000)

    # Load data for the symbol and timeframes
    data_dict = backtest.load_data(data_dir)

    # Initialize multi-timeframe strategy
    strategy = MultiTimeframeStrategy(symbol=symbol)

    # Run the backtest
    backtest.run(strategy=strategy, data_dict=data_dict)
