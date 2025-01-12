# Test the Mean Reversion Strategy

from strategies.mean_reversion import MeanReversionStrategy

class MockTradeExecutor:
    """
    Mock Trade Executor for testing trade execution functionality.
    """
    def open_buy(self, symbol, lot_size, stop_loss, take_profit):
        print(f"BUY Order: Symbol={symbol}, LotSize={lot_size}, SL={stop_loss}, TP={take_profit}")

    def open_sell(self, symbol, lot_size, stop_loss, take_profit):
        print(f"SELL Order: Symbol={symbol}, LotSize={lot_size}, SL={stop_loss}, TP={take_profit}")

def test_mean_reversion_strategy():
    """
    Test the Mean Reversion Strategy with mock data and a mock trade executor.
    """
    # Mock market data for testing
    market_data = {
        'closes': [100, 102, 101, 103, 105, 104, 106, 107, 108, 107, 106, 105, 104, 102, 101],
        'highs': [101, 103, 102, 104, 106, 105, 107, 108, 109, 108, 107, 106, 105, 103, 102],
        'lows': [99, 101, 100, 102, 104, 103, 105, 106, 107, 106, 105, 104, 103, 101, 100]
    }

    # Initialize the strategy and mock trade executor
    strategy = MeanReversionStrategy(
        symbol="EURUSD",
        lot_size=0.1,
        stop_loss=50,
        take_profit=100,
        rsi_threshold=30,
        ema_period=14,
        bollinger_period=14,
        bollinger_std_dev=2
    )
    trade_executor = MockTradeExecutor()

    # Run the test
    strategy.setup(market_data)
    signal = strategy.generate_signal()
    print(f"Generated Signal: {signal}")
    strategy.execute_trade(signal, trade_executor)