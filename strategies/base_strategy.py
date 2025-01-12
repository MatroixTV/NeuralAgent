from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    """
    Abstract Base Class for trading strategies.
    Provides the structure and common functionality for derived strategies.
    """

    def __init__(self, symbol, lot_size, stop_loss, take_profit, atr_multiplier=1.5):
        """
        Initialize the base strategy.

        :param symbol: The trading symbol (e.g., "EURUSD")
        :param lot_size: Lot size for trades
        :param stop_loss: Stop-loss in pips
        :param take_profit: Take-profit in pips
        :param atr_multiplier: Multiplier for ATR-based stop-loss (default: 1.5)
        """
        self.symbol = symbol
        self.lot_size = lot_size
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.atr_multiplier = atr_multiplier
        self.indicators = {}  # Dictionary to store indicator values

    def setup(self, market_data):
        """
        Setup the strategy by calculating required indicators.

        :param market_data: A dictionary with price data (e.g., highs, lows, closes)
        """
        self.indicators['rsi'] = self.calculate_rsi(market_data['closes'])
        self.indicators['ema'] = self.calculate_ema(market_data['closes'])
        self.indicators['atr'] = self.calculate_atr(market_data['highs'], market_data['lows'], market_data['closes'])

    @abstractmethod
    def generate_signal(self):
        """
        Abstract method for generating trading signals.
        Must be implemented by derived strategies.
        """
        pass

    def execute_trade(self, signal, trade_executor):
        """
        Execute a trade based on the generated signal.

        :param signal: The signal ('buy', 'sell', or 'hold')
        :param trade_executor: An instance of the TradeExecutor class
        """
        if signal == 'buy':
            trade_executor.open_buy(self.symbol, self.lot_size, self.stop_loss, self.take_profit)
        elif signal == 'sell':
            trade_executor.open_sell(self.symbol, self.lot_size, self.stop_loss, self.take_profit)

    # Indicator calculations
    def calculate_rsi(self, prices, period=14):
        from indicators.rsi import RSI
        return RSI.calculate(prices, period)

    def calculate_ema(self, prices, period=14):
        from indicators.ema import EMA
        return EMA.calculate(prices, period)

    def calculate_atr(self, highs, lows, closes, period=14):
        from indicators.atr import ATR
        return ATR.calculate(highs, lows, closes, period)
