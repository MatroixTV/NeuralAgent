# indicators/rsi.py
import numpy as np

class RSI:
    @staticmethod
    def calculate(prices, period=14):
        """
        Calculate the Relative Strength Index (RSI).

        :param prices: List or numpy array of closing prices
        :param period: The period for calculating RSI (default: 14)
        :return: RSI value
        """
        prices = np.array(prices)
        if len(prices) < period:
            raise ValueError("Not enough data to calculate RSI")

        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])

        for i in range(period, len(prices) - 1):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        rsi = 100 - (100 / (1 + rs))
        return rsi
