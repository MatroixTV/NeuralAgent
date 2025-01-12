import MetaTrader5 as mt5
import pandas as pd
from utils.logger import Logger
from utils.config_loader import ConfigLoader
from utils.data_fetcher import DataFetcher
from strategies.trend_following import TrendFollowingStrategy
from strategies.mean_reversion import MeanReversionStrategy
from trade_management.trade_executor import TradeExecutor
from trade_management.risk_manager import RiskManager
from trade_management.trailing_stop import TrailingStopManager


class NeuralAgentBot:
    """
    The main trading bot integrating strategies, trade management, and execution using MetaTrader 5.
    """

    def __init__(self, config_file="config.json"):
        """
        Initialize the trading bot.

        :param config_file: Path to the JSON configuration file
        """
        # Load configuration
        self.logger = Logger()
        self.logger.info("Loading configuration...")
        self.config = ConfigLoader.load_config(config_file)
        if not self.config:
            self.logger.error("Failed to load configuration file")
            raise ValueError("Failed to load configuration file")

        self.symbol = self.config["symbol"]
        self.account_balance = self.config["account_balance"]
        self.risk_per_trade = self.config["risk_per_trade"]

        # Initialize components
        self.trade_executor = TradeExecutor(self.symbol)
        self.risk_manager = RiskManager(self.account_balance, self.risk_per_trade)
        self.trailing_stop_manager = TrailingStopManager(atr_multiplier=1.5)

        # Select a strategy
        strategy_type = self.config.get("strategy_type", "trend_following")
        self.logger.info(f"Selected strategy type: {strategy_type}")
        if strategy_type == "trend_following":
            self.strategy = TrendFollowingStrategy(
                symbol=self.symbol,
                lot_size=0.1,  # Placeholder; calculated dynamically later
                stop_loss=self.config["stop_loss"],
                take_profit=self.config["take_profit"],
                rsi_threshold=self.config["rsi_threshold"],
                ema_period=self.config["ema_period"]
            )
        elif strategy_type == "mean_reversion":
            self.strategy = MeanReversionStrategy(
                symbol=self.symbol,
                lot_size=0.1,  # Placeholder; calculated dynamically later
                stop_loss=self.config["stop_loss"],
                take_profit=self.config["take_profit"],
                rsi_threshold=self.config["rsi_threshold"],
                ema_period=self.config["ema_period"],
                bollinger_period=self.config["bollinger_period"],
                bollinger_std_dev=self.config["bollinger_std_dev"]
            )
        else:
            self.logger.error(f"Unsupported strategy type: {strategy_type}")
            raise ValueError(f"Unsupported strategy type: {strategy_type}")

    def connect_to_mt5(self):
        """
        Connect to MetaTrader 5.
        """
        if not mt5.initialize():
            self.logger.error("MetaTrader5 initialization failed")
            return False

        self.logger.info("MetaTrader5 connected successfully")
        return True

    def fetch_market_data(self, num_candles=100):
        """
        Fetch historical Forex market data using MetaTrader 5.
        :param num_candles: Number of historical candles to fetch
        :return: Market data dictionary
        """
        try:
            self.logger.info(f"Fetching {num_candles} historical candles for {self.symbol}...")
            df = DataFetcher.fetch_data(self.symbol, num_candles=num_candles)
            self.logger.info("Historical market data fetched successfully")
            return {
                "highs": df["high"].values,
                "lows": df["low"].values,
                "closes": df["close"].values
            }
        except Exception as e:
            self.logger.error(f"Error fetching historical market data: {e}")
            return None

    def run(self, use_historical=True, num_candles=100):
        """
        Main loop of the trading bot.
        :param use_historical: Whether to use historical data for testing
        :param num_candles: Number of historical candles to fetch
        """
        self.logger.info("Starting NeuralAgentBot...")

        # Connect to MetaTrader 5
        if not self.connect_to_mt5():
            self.logger.error("Failed to connect to MetaTrader 5. Exiting.")
            return

        # Fetch market data
        market_data = self.fetch_market_data(num_candles=num_candles if use_historical else 1)
        if not market_data:
            self.logger.error("Failed to fetch market data. Exiting.")
            mt5.shutdown()
            return

        # Setup strategy with market data
        self.strategy.setup(market_data)

        # Log indicator values (for debugging)
        self.logger.info(f"Indicator Values: {self.strategy.indicators}")

        # Calculate position size dynamically
        lot_size = self.risk_manager.calculate_lot_size(
            stop_loss_pips=self.strategy.stop_loss,
            pip_value=10  # Placeholder pip value
        )
        self.strategy.lot_size = lot_size
        self.logger.info(f"Calculated Lot Size: {lot_size}")

        # Generate a trading signal
        signal = self.strategy.generate_signal()
        self.logger.info(f"Generated Signal: {signal}")

        # Execute trade based on the signal
        self.strategy.execute_trade(signal, self.trade_executor)

        # Disconnect from MetaTrader 5
        mt5.shutdown()
        self.logger.info("NeuralAgentBot finished.")


# Run the bot
if __name__ == "__main__":
    bot = NeuralAgentBot(config_file="config.json")
    bot.run(use_historical=True, num_candles=500)  # Fetch last 500 candles
