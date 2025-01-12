from strategies.base_strategy import BaseStrategy

class TrendFollowingStrategy(BaseStrategy):
    """
    Implements a Trend Following Strategy using RSI and EMA.
    """

    def __init__(self, symbol, lot_size, stop_loss, take_profit, atr_multiplier=1.5, rsi_threshold=30, ema_period=14):
        """
        Initialize the trend-following strategy.

        :param symbol: The trading symbol (e.g., "EURUSD")
        :param lot_size: Lot size for trades
        :param stop_loss: Stop-loss in pips
        :param take_profit: Take-profit in pips
        :param atr_multiplier: Multiplier for ATR-based stop-loss (default: 1.5)
        :param rsi_threshold: RSI threshold for buy/sell signals
        :param ema_period: EMA period for trend identification
        """
        super().__init__(symbol, lot_size, stop_loss, take_profit, atr_multiplier)
        self.rsi_threshold = rsi_threshold
        self.ema_period = ema_period

    def generate_signal(self):
        """
        Generate a trading signal based on trend-following logic.
        :return: 'buy', 'sell', or 'hold'
        """
        rsi = self.indicators['rsi']
        ema = self.indicators['ema']
        current_price = self.indicators['current_price']

        # Buy signal: Oversold RSI and price above EMA
        if rsi < self.rsi_threshold and current_price > ema:
            return 'buy'

        # Sell signal: Overbought RSI and price below EMA
        elif rsi > (100 - self.rsi_threshold) and current_price < ema:
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
