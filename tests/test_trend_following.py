import unittest
from strategies.trend_following import TrendFollowingStrategy

class TestTrendFollowingStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = TrendFollowingStrategy(
            symbol="EURUSD",
            lot_size=0.1,
            stop_loss=50,
            take_profit=100,
            rsi_threshold=30,
            ema_period=14
        )

    def test_generate_signal_buy(self):
        """
        Test that the strategy generates a 'buy' signal under the correct conditions.
        """
        market_data = {
            "highs": [1.1 + i * 0.01 for i in range(14)],
            "lows": [1.0 + i * 0.01 for i in range(14)],
            "closes": [1.05 + i * 0.02 for i in range(14)]  # Adjusted closes for buy condition
        }
        self.strategy.setup(market_data)
        signal = self.strategy.generate_signal()
        self.assertEqual(signal, "buy", "Expected 'buy' signal")

    def test_generate_signal_sell(self):
        """
        Test that the strategy generates a 'sell' signal under the correct conditions.
        """
        market_data = {
            "highs": [1.3 - i * 0.01 for i in range(14)],
            "lows": [1.2 - i * 0.01 for i in range(14)],
            "closes": [1.25 - i * 0.02 for i in range(14)]  # Adjusted closes for sell condition
        }
        self.strategy.setup(market_data)
        signal = self.strategy.generate_signal()
        self.assertEqual(signal, "sell", "Expected 'sell' signal")

    def test_generate_signal_hold(self):
        """
        Test that the strategy generates a 'hold' signal when conditions are neutral.
        """
        market_data = {
            "highs": [1.1 + i * 0.01 for i in range(14)],
            "lows": [1.0 + i * 0.01 for i in range(14)],
            "closes": [1.05 + (i % 2) * 0.005 for i in range(14)]  # Neutral closes
        }
        self.strategy.setup(market_data)
        signal = self.strategy.generate_signal()
        self.assertEqual(signal, "hold", "Expected 'hold' signal")


if __name__ == "__main__":
    unittest.main()
