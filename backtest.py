import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from models.ml_model import MLModel

class Backtest:
    def __init__(self, initial_balance):
        self.initial_balance = initial_balance
        self.equity = initial_balance
        self.trades = []
        self.equity_curve = [initial_balance]
        self.max_drawdown = 0
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.current_streak = 0
        self.current_streak_type = None  # 'win' or 'loss'

    def calculate_performance_metrics(self):
        profits = [trade["profit"] for trade in self.trades]
        win_trades = [p for p in profits if p > 0]
        loss_trades = [p for p in profits if p <= 0]

        # Win Rate
        win_rate = len(win_trades) / len(profits) * 100 if profits else 0

        # Profit Factor
        gross_profit = sum(win_trades)
        gross_loss = abs(sum(loss_trades))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else "N/A"

        # Maximum Drawdown
        peak = -np.inf
        for eq in self.equity_curve:
            peak = max(peak, eq)
            self.max_drawdown = max(self.max_drawdown, peak - eq)

        # Maximum Consecutive Wins and Losses
        for profit in profits:
            if profit > 0:
                if self.current_streak_type == "win":
                    self.current_streak += 1
                else:
                    self.current_streak = 1
                    self.current_streak_type = "win"
                self.consecutive_wins = max(self.consecutive_wins, self.current_streak)
            else:
                if self.current_streak_type == "loss":
                    self.current_streak += 1
                else:
                    self.current_streak = 1
                    self.current_streak_type = "loss"
                self.consecutive_losses = max(self.consecutive_losses, self.current_streak)

        return {
            "Win Rate": win_rate,
            "Profit Factor": profit_factor,
            "Max Drawdown": self.max_drawdown,
            "Max Consecutive Wins": self.consecutive_wins,
            "Max Consecutive Losses": self.consecutive_losses,
        }

    def run(self, data):
        for i, row in data.iterrows():
            signal = row["ML_Signal"]
            if signal == "buy":
                entry_price = row["Close"]
                self.trades.append({"type": "buy", "price": entry_price})
            elif signal == "sell" and self.trades:
                last_trade = self.trades.pop()
                if last_trade["type"] == "buy":
                    exit_price = row["Close"]
                    profit = exit_price - last_trade["price"]
                    self.equity += profit
                    self.trades.append({"type": "sell", "profit": profit})
                    self.equity_curve.append(self.equity)

    def plot_results(self, data):
        # Plot price with buy/sell signals
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.plot(data["Date"], data["Close"], label="Close Price", color="blue")
        plt.scatter(data[data["ML_Signal"] == "buy"].index, data[data["ML_Signal"] == "buy"]["Close"], marker="^", color="green", label="Buy Signal")
        plt.scatter(data[data["ML_Signal"] == "sell"].index, data[data["ML_Signal"] == "sell"]["Close"], marker="v", color="red", label="Sell Signal")
        plt.legend()
        plt.title("Price and Signals")

        # Plot equity curve
        plt.subplot(2, 1, 2)
        plt.plot(self.equity_curve, label="Equity Curve", color="orange")
        plt.legend()
        plt.title("Equity Curve")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Load data
    data = pd.read_csv("training/training_data.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    model = MLModel()
    model.load_model()

    # Generate ML signals
    features = data.drop(columns=["Date", "Close"])
    data["ML_Signal"] = model.predict(features)
    data["ML_Signal"] = np.where(data["ML_Signal"] > 0.5, "buy", "sell")

    # Backtest
    bot = Backtest(initial_balance=200)
    bot.run(data)

    # Calculate and display performance metrics
    metrics = bot.calculate_performance_metrics()
    print("\nDetailed Performance Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")

    # Plot results
    bot.plot_results(data)
