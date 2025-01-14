# from strategies.base_strategy import BaseStrategy
#
# class TrendFollowingStrategy(BaseStrategy):
#     """
#     Implements a Trend Following Strategy using RSI and EMA.
#     """
#
#     def __init__(self, symbol, lot_size, stop_loss, take_profit, atr_multiplier=1.5, rsi_threshold=30, ema_period=14):
#         """
#         Initialize the trend-following strategy.
#
#         :param symbol: The trading symbol (e.g., "EURUSD")
#         :param lot_size: Lot size for trades
#         :param stop_loss: Stop-loss in pips
#         :param take_profit: Take-profit in pips
#         :param atr_multiplier: Multiplier for ATR-based stop-loss (default: 1.5)
#         :param rsi_threshold: RSI threshold for buy/sell signals
#         :param ema_period: EMA period for trend identification
#         """
#         super().__init__(symbol, lot_size, stop_loss, take_profit, atr_multiplier)
#         self.rsi_threshold = rsi_threshold
#         self.ema_period = ema_period
#
#     def generate_signal(self):
#         """
#         Generate a trading signal based on strategy logic.
#         :return: 'buy', 'sell', or 'hold'
#         """
#         # Retrieve indicator values
#         rsi = self.indicators.get('rsi')
#         ema = self.indicators.get('ema')
#         current_price = self.indicators.get('current_price')
#
#         # Debug: Log indicator values
#         print(f"Debug - RSI: {rsi}, EMA: {ema}, Current Price: {current_price}")
#
#         # Example: Adjust conditions based on strategy type
#         if hasattr(self, 'bollinger_upper') and hasattr(self, 'bollinger_lower'):  # For mean reversion
#             bollinger_upper = self.indicators.get('upper_band')
#             bollinger_lower = self.indicators.get('lower_band')
#             print(f"Debug - Bollinger Upper: {bollinger_upper}, Lower: {bollinger_lower}")
#
#         # Example Buy/Sell conditions
#         if rsi < self.rsi_threshold and current_price > ema:
#             print("Signal: Buy")
#             return 'buy'
#         elif rsi > (100 - self.rsi_threshold) and current_price < ema:
#             print("Signal: Sell")
#             return 'sell'
#
#         print("Signal: Hold")
#         return 'hold'
#
#     def setup(self, market_data):
#         """
#         Calculate indicators required for the strategy.
#         :param market_data: A dictionary with price data (e.g., highs, lows, closes)
#         """
#         super().setup(market_data)
#         # Store the most recent price as 'current_price'
#         self.indicators['current_price'] = market_data['closes'][-1]

from models.ml_model import MLModel
import pandas as pd


class MLStrategy:
    def __init__(self, symbol="EURUSD"):
        self.symbol = symbol
        self.ml_model = MLModel()
        self.ml_model.load_model()  # Load the trained model

    def generate_signal(self, market_data):
        """
        Generate a signal using the ML model.

        :param market_data: DataFrame containing market features
        :return: 'buy', 'sell', or 'hold'
        """
        # Prepare data for prediction
        features = market_data.drop(columns=["Date"])  # Exclude Date
        predictions = self.ml_model.predict(features)

        # Translate predictions into signals
        signal_map = {0: "hold", 1: "buy"}
        signal = signal_map.get(predictions[-1], "hold")  # Take the last prediction
        print(f"ML Signal: {signal}")
        return signal
