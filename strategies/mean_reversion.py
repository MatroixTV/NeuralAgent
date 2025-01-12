from strategies.base_strategy import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    """
    Implements a Mean Reversion Strategy using RSI and Bollinger Bands.
    """

    def __init__(self, symbol, lot_size, stop_loss, take_profit, rsi_threshold=30, ema_period=14, bollinger_period=20, bollinger_std_dev=2):
        """
        Initialize the mean reversion strategy.

        :param symbol: The trading symbol (e.g., "EURUSD")
        :param lot_size: Lot size for trades
        :param stop_loss: Stop-loss in pips
        :param take_profit: Take-profit in pips
        :param rsi_threshold: RSI threshold for buy/sell signals
        :param ema_period: EMA period for trend confirmation
        :param bollinger_period: Bollinger Band period
        :param bollinger_std_dev: Standard deviation for Bollinger Bands
        """
        super().__init__(symbol, lot_size, stop_loss, take_profit)
        self.rsi_threshold = rsi_threshold
        self.ema_period = ema_period
        self.bollinger_period = bollinger_period
        self.bollinger_std_dev = bollinger_std_dev

    def generate_signal(self):
        """
        Generate a trading signal based on mean reversion logic.
        :return: 'buy', 'sell', or 'hold'
        """
        rsi = self.indicators['rsi']
        lower_band = self.indicators['lower_band']
        upper_band = self.indicators['upper_band']
        current_price = self.indicators['current_price']

        # Buy signal: Oversold RSI and price below lower Bollinger Band
        if rsi < self.rsi_threshold and current_price < lower_band:
            return 'buy'

        # Sell signal: Overbought RSI and price above upper Bollinger Band
        elif rsi > (100 - self.rsi_threshold) and current_price > upper_band:
            return 'sell'

        # Otherwise, hold
        return 'hold'

    def setup(self, market_data):
        """
        Calculate indicators required for the strategy.
        :param market_data: A dictionary with price data (e.g., highs, lows, closes)
        """
        super().setup(market_data)
        # Store the most recent price as 'current_price'
        self.indicators['current_price'] = market_data['closes'][-1]

        # Calculate Bollinger Bands
        self.indicators['lower_band'], self.indicators['upper_band'] = self.calculate_bollinger_bands(market_data['closes'])

    def calculate_bollinger_bands(self, closes):
        """
        Calculate Bollinger Bands.

        :param closes: List or numpy array of closing prices
        :return: (lower_band, upper_band)
        """
        import numpy as np

        closes = np.array(closes)
        if len(closes) < self.bollinger_period:
            raise ValueError("Not enough data to calculate Bollinger Bands")

        sma = np.mean(closes[-self.bollinger_period:])
        std_dev = np.std(closes[-self.bollinger_period:])
        lower_band = sma - (self.bollinger_std_dev * std_dev)
        upper_band = sma + (self.bollinger_std_dev * std_dev)

        return lower_band, upper_band
