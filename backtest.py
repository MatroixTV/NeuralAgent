import MetaTrader5 as mt5
import pandas as pd
from utils.logger import Logger
from utils.config_loader import ConfigLoader
from utils.data_fetcher import DataFetcher
from strategies.trend_following import TrendFollowingStrategy
from strategies.mean_reversion import MeanReversionStrategy
from trade_management.trade_executor import TradeExecutor
from trade_management.risk_manager import RiskManager

class BacktestBot:
    """
    Simulates the trading bot's behavior using historical data for backtesting.
    """

    def __init__(self, config_file="config.json"):
        self.logger = Logger()
        self.logger.info("Loading configuration...")
        self.config = ConfigLoader.load_config(config_file)
        if not self.config:
            raise ValueError("Failed to load configuration file")

        self.symbol = self.config["symbol"]
        self.account_balance = self.config["account_balance"]
        self.risk_per_trade = self.config["risk_per_trade"]
        self.initial_balance = self.account_balance
        self.trade_executor = TradeExecutor(self.symbol)
        self.risk_manager = RiskManager(self.account_balance, self.risk_per_trade)

        # Select strategy
        strategy_type = self.config.get("strategy_type", "trend_following")
        if strategy_type == "trend_following":
            self.strategy = TrendFollowingStrategy(
                symbol=self.symbol,
                lot_size=0.1,
                stop_loss=self.config["stop_loss"],
                take_profit=self.config["take_profit"],
                rsi_threshold=self.config["rsi_threshold"],
                ema_period=self.config["ema_period"]
            )
        elif strategy_type == "mean_reversion":
            self.strategy = MeanReversionStrategy(
                symbol=self.symbol,
                lot_size=0.1,
                stop_loss=self.config["stop_loss"],
                take_profit=self.config["take_profit"],
                rsi_threshold=self.config["rsi_threshold"],
                ema_period=self.config["ema_period"],
                bollinger_period=self.config["bollinger_period"],
                bollinger_std_dev=self.config["bollinger_std_dev"]
            )
        else:
            raise ValueError(f"Unsupported strategy type: {strategy_type}")

        self.logger.info(f"Selected strategy: {strategy_type}")

    def fetch_historical_data(self, num_candles=5000):
        """
        Fetch a large amount of historical data for backtesting.
        :param num_candles: Number of historical candles to fetch
        :return: DataFrame with market data
        """
        self.logger.info(f"Fetching {num_candles} historical candles for {self.symbol}...")
        try:
            df = DataFetcher.fetch_data(self.symbol, num_candles=num_candles)
            self.logger.info("Historical market data fetched successfully")
            return df
        except Exception as e:
            self.logger.error(f"Failed to fetch historical data: {e}")
            return None

    def run_backtest(self, num_candles=5000):
        """
        Run the backtest simulation.
        :param num_candles: Number of historical candles to use for backtesting
        """
        # Fetch historical data
        df = self.fetch_historical_data(num_candles)
        if df is None:
            self.logger.error("No historical data available. Exiting backtest.")
            return

        trades = 0
        wins = 0
        losses = 0
        profit = 0
        max_drawdown = 0
        peak_balance = self.account_balance

        # Loop through each candle
        for i in range(self.config["ema_period"], len(df)):
            market_data = {
                "highs": df["high"][:i].values,
                "lows": df["low"][:i].values,
                "closes": df["close"][:i].values
            }

            # Setup strategy with partial data
            self.strategy.setup(market_data)

            # Generate signal
            signal = self.strategy.generate_signal()
            if signal in ["buy", "sell"]:
                trades += 1
                lot_size = self.risk_manager.calculate_lot_size(
                    stop_loss_pips=self.config["stop_loss"],
                    pip_value=10
                )
                self.strategy.lot_size = lot_size

                # Simulate trade outcome
                trade_result = self.simulate_trade(signal, market_data, i, df)
                profit += trade_result
                if trade_result > 0:
                    wins += 1
                else:
                    losses += 1

                # Track drawdown
                self.account_balance += trade_result
                if self.account_balance > peak_balance:
                    peak_balance = self.account_balance
                drawdown = peak_balance - self.account_balance
                max_drawdown = max(max_drawdown, drawdown)

        win_rate = (wins / trades) * 100 if trades > 0 else 0

        # Log results
        self.logger.info(f"Backtest completed: {trades} trades executed")
        self.logger.info(f"Total Profit: {profit:.2f}")
        self.logger.info(f"Win Rate: {win_rate:.2f}%")
        self.logger.info(f"Max Drawdown: {max_drawdown:.2f}")
        self.logger.info(f"Final Balance: {self.account_balance:.2f}")

    def simulate_trade(self, signal, market_data, current_index, df):
        """
        Simulate the outcome of a trade.
        :param signal: 'buy' or 'sell'
        :param market_data: Market data up to the current index
        :param current_index: Current index in the historical data
        :param df: Full historical data
        :return: Simulated trade profit/loss
        """
        entry_price = market_data["closes"][-1]
        sl_pips = self.config["stop_loss"] / 10000
        tp_pips = self.config["take_profit"] / 10000

        if signal == "buy":
            stop_loss = entry_price - sl_pips
            take_profit = entry_price + tp_pips
            for j in range(current_index + 1, len(df)):
                if df["low"].iloc[j] <= stop_loss:
                    return -sl_pips * 100
                if df["high"].iloc[j] >= take_profit:
                    return tp_pips * 100
        elif signal == "sell":
            stop_loss = entry_price + sl_pips
            take_profit = entry_price - tp_pips
            for j in range(current_index + 1, len(df)):
                if df["high"].iloc[j] >= stop_loss:
                    return -sl_pips * 100
                if df["low"].iloc[j] <= take_profit:
                    return tp_pips * 100
        return 0


if __name__ == "__main__":
    backtester = BacktestBot(config_file="config.json")
    backtester.run_backtest(num_candles=500)
