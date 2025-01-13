import pandas as pd
from strategies.trend_following import MLStrategy
from utils.data_preparation import calculate_indicators
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class BacktestBot:
    def __init__(self):
        self.strategy = MLStrategy(symbol="EURUSD")

    def run_backtest(self, data):
        """
        Run the backtest using the ML strategy.

        :param data: DataFrame with historical market data
        """
        print("Running backtest with ML-based strategy...")
        trades = 0
        equity = 200  # Starting equity
        signals = []

        # Calculate required features
        data = calculate_indicators(data).copy()

        for i in range(len(data) - 1):
            # Prepare market data slice
            market_data = data.iloc[: i + 1]

            # Generate signal using ML model
            signal = self.strategy.generate_signal(market_data)
            signals.append(signal)

            # Simulate trade (example logic)
            if signal == "buy":
                trades += 1
                equity += 50  # Example profit
            elif signal == "sell":
                trades += 1
                equity -= 50  # Example loss

        # Add signals to the data for visualization
        data = data.iloc[:-1].copy()
        data["Signal"] = signals

        print(f"Backtest completed: Trades={trades}, Final Equity={equity:.2f}")
        self.visualize(data)

        # Calculate metrics
        initial_balance = 200
        total_profit = equity - initial_balance
        max_drawdown = initial_balance - min(equity, initial_balance)
        buy_signals = sum([1 for s in signals if s == "buy"])
        sell_signals = sum([1 for s in signals if s == "sell"])
        win_rate = (buy_signals / trades) * 100 if trades > 0 else 0
        sharpe_ratio = (total_profit / len(data)) / data["Close"].std() if data["Close"].std() != 0 else 0

        # Print detailed results
        print("\nDetailed Performance Metrics:")
        print(f"Initial Balance: ${initial_balance:.2f}")
        print(f"Final Equity: ${equity:.2f}")
        print(f"Total Profit: ${total_profit:.2f}")
        print(f"Max Drawdown: ${max_drawdown:.2f}")
        print(f"Win Rate: {win_rate:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

    def visualize(self, data):
        """
        Visualize price data and ML-generated signals.
        """
        plt.figure(figsize=(14, 8))

        # Plot close prices
        plt.plot(data["Date"], data["Close"], label="Close Price", color="blue")

        # Plot buy/sell signals
        buy_signals = data[data["Signal"] == "buy"]
        sell_signals = data[data["Signal"] == "sell"]

        plt.scatter(buy_signals["Date"], buy_signals["Close"], label="Buy Signal", marker="^", color="green", alpha=0.8)
        plt.scatter(sell_signals["Date"], sell_signals["Close"], label="Sell Signal", marker="v", color="red", alpha=0.8)

        plt.title("Price and ML Signals with Performance Metrics")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()

        # Annotate cumulative profit
        total_profit = (data["Signal"] == "buy").sum() * 50  # Example
        plt.figtext(0.15, 0.8, f"Cumulative Profit: ${total_profit:.2f}", fontsize=12, color="green")

        plt.show()


if __name__ == "__main__":
    # Load historical data
    data = pd.read_csv("utils/EURUSD_daily_cleaned.csv")
    data["Date"] = pd.to_datetime(data["Date"])

    # Filter data for the last 30 days
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.Timedelta(days=30)
    recent_data = data[(data["Date"] >= start_date) & (data["Date"] <= end_date)]

    # Run backtest
    bot = BacktestBot()
    bot.run_backtest(recent_data)
