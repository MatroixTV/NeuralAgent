import pandas as pd
import matplotlib.pyplot as plt
from strategies.trend_following import TrendFollowingStrategy
from strategies.mean_reversion import MeanReversionStrategy

class BacktestBot:
    """
    Simulates the trading bot's performance using historical data.
    """

    def __init__(self, strategy_type="trend_following"):
        self.strategy_type = strategy_type

        # Initialize strategy
        if strategy_type == "trend_following":
            self.strategy = TrendFollowingStrategy(
                symbol="EURUSD",
                lot_size=0.1,
                stop_loss=50,
                take_profit=100,
                rsi_threshold=30,
                ema_period=14
            )
        elif strategy_type == "mean_reversion":
            self.strategy = MeanReversionStrategy(
                symbol="EURUSD",
                lot_size=0.1,
                stop_loss=50,
                take_profit=100,
                rsi_threshold=30,
                ema_period=14,
                bollinger_period=20,
                bollinger_std_dev=2
            )
        else:
            raise ValueError(f"Unsupported strategy type: {strategy_type}")

    def visualize_indicators(self, data, indicators):
        """
        Visualize price data and indicators.

        :param data: Historical price data (DataFrame)
        :param indicators: Calculated indicators (dict)
        """
        plt.figure(figsize=(14, 8))

        # Plot price data
        plt.plot(data['Date'], data['Close'], label="Close Price", color="blue")

        # Plot EMA (only if available)
        if "ema" in indicators and any(indicators["ema"]):
            plt.plot(data['Date'][:len(indicators["ema"])], indicators["ema"], label="EMA", color="orange")

        # Plot Bollinger Bands (if available)
        if "upper_band" in indicators and "lower_band" in indicators:
            if any(indicators["upper_band"]) and any(indicators["lower_band"]):
                plt.plot(data['Date'][:len(indicators["upper_band"])], indicators["upper_band"], label="Bollinger Upper", color="green", linestyle="--")
                plt.plot(data['Date'][:len(indicators["lower_band"])], indicators["lower_band"], label="Bollinger Lower", color="red", linestyle="--")

        plt.title("Price and Indicators")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()

    def run_backtest(self, data):
        """
        Run the backtest on the provided historical data.
        :param data: DataFrame containing historical price data
        """
        indicators_log = {"ema": [], "upper_band": [], "lower_band": []}  # To store indicator values
        trades = 0
        wins = 0
        losses = 0
        profit = 0
        equity = 10000  # Starting equity

        print(f"Running backtest with {self.strategy_type} strategy...")

        # Loop through each row
        for i in range(max(self.strategy.ema_period, self.strategy.rsi_threshold), len(data)):
            market_data = {
                "highs": data["High"][:i].values,
                "lows": data["Low"][:i].values,
                "closes": data["Close"][:i].values
            }
            self.strategy.setup(market_data)

            # Collect indicator values
            indicators_log["ema"].append(self.strategy.indicators.get("ema"))
            indicators_log["upper_band"].append(self.strategy.indicators.get("upper_band"))
            indicators_log["lower_band"].append(self.strategy.indicators.get("lower_band"))

            # Generate signal
            signal = self.strategy.generate_signal()
            print(f"Date: {data['Date'].iloc[i]}, Signal: {signal}")

            # Simulate trade
            if signal in ["buy", "sell"]:
                trades += 1
                result = self.simulate_trade(signal, data.iloc[i])
                equity += result
                profit += result
                if result > 0:
                    wins += 1
                else:
                    losses += 1

        # Visualize indicators
        try:
            self.visualize_indicators(data, indicators_log)
        except Exception as e:
            print(f"Error during visualization: {e}")

        print(
            f"Backtest completed: Trades={trades}, Wins={wins}, Losses={losses}, Profit={profit:.2f}, Final Equity={equity:.2f}"
        )

    def simulate_trade(self, signal, row):
        """
        Simulates the outcome of a trade based on the signal and current row of data.

        :param signal: 'buy' or 'sell'
        :param row: Current row of historical data
        :return: Simulated profit/loss
        """
        entry_price = row["Close"]
        sl_pips = self.strategy.stop_loss / 10000
        tp_pips = self.strategy.take_profit / 10000

        if signal == "buy":
            stop_loss = entry_price - sl_pips
            take_profit = entry_price + tp_pips
            if row["Low"] <= stop_loss:
                return -sl_pips * 10000
            elif row["High"] >= take_profit:
                return tp_pips * 10000
        elif signal == "sell":
            stop_loss = entry_price + sl_pips
            take_profit = entry_price - tp_pips
            if row["High"] >= stop_loss:
                return -sl_pips * 10000
            elif row["Low"] <= take_profit:
                return tp_pips * 10000
        return 0


if __name__ == "__main__":
    # Load historical data
    data = pd.read_csv("utils/EURUSD_daily_cleaned.csv")
    data["Date"] = pd.to_datetime(data["Date"])

    # Run backtest for each strategy
    for strategy in ["trend_following", "mean_reversion"]:
        bot = BacktestBot(strategy_type=strategy)
        bot.run_backtest(data)
