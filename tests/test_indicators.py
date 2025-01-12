import unittest
import numpy as np
from indicators.rsi import RSI
from indicators.ema import EMA
from indicators.atr import ATR
from indicators.sar import SAR


class TestIndicators(unittest.TestCase):
    """
    Unit tests for all indicators implemented in the NeuralAgent bot.
    """

    def test_rsi_calculation(self):
        """
        Test RSI calculation.
        """
        prices = np.array([44.3389, 44.0902, 44.1497, 43.6124, 44.3278,
                           44.8264, 45.0955, 45.4245, 45.8433, 46.0826,
                           45.8931, 46.0328, 45.6140, 46.2820, 46.2820,
                           46.0028, 46.0328, 46.4116, 46.2222, 45.6439,
                           46.2122, 46.2521, 45.7137, 46.4515, 45.7835,
                           45.3548, 44.0288, 44.1783, 44.2181, 44.5672])
        period = 14
        rsi_value = RSI.calculate(prices, period)
        self.assertIsInstance(rsi_value, float, "RSI should return a float value")
        print(f"RSI Value: {rsi_value}")

    def test_ema_calculation(self):
        """
        Test EMA calculation.
        """
        prices = np.array([44.3389, 44.0902, 44.1497, 43.6124, 44.3278,
                           44.8264, 45.0955, 45.4245, 45.8433, 46.0826])
        period = 5
        ema_value = EMA.calculate(prices, period)
        self.assertIsInstance(ema_value, float, "EMA should return a float value")
        print(f"EMA Value: {ema_value}")

    def test_atr_calculation(self):
        """
        Test ATR calculation.
        """
        highs = np.array([1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55])
        lows = np.array([1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45])
        closes = np.array([1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5])
        period = 5
        atr_value = ATR.calculate(highs, lows, closes, period)
        self.assertIsInstance(atr_value, float, "ATR should return a float value")
        print(f"ATR Value: {atr_value}")

    def test_sar_calculation(self):
        """
        Test SAR calculation.
        """
        highs = [101, 103, 102, 104, 106, 105, 107, 108, 109]
        lows = [99, 101, 100, 102, 104, 103, 105, 106, 107]
        sar_value = SAR.calculate(highs, lows)
        self.assertIsInstance(sar_value, float, "SAR should return a float value")
        print(f"SAR Value: {sar_value}")


if __name__ == "__main__":
    unittest.main()
