import numpy as np


class ATR:
    @staticmethod
    def calculate(highs, lows, closes, period=14):
        """
        Calculate the Average True Range (ATR).

        :param highs: List or numpy array of high prices
        :param lows: List or numpy array of low prices
        :param closes: List or numpy array of close prices
        :param period: The period for calculating ATR (default: 14)
        :return: ATR value
        """
        if len(highs) != len(lows) or len(lows) != len(closes):
            raise ValueError("Highs, Lows, and Closes must have the same length")
        if len(highs) < period:
            raise ValueError("Not enough data to calculate ATR")

        highs, lows, closes = np.array(highs), np.array(lows), np.array(closes)

        # Compute True Range
        true_ranges = []
        for i in range(1, len(highs)):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i - 1])
            low_close = abs(lows[i] - closes[i - 1])
            true_range = max(high_low, high_close, low_close)
            true_ranges.append(true_range)

        # Calculate ATR
        true_ranges = np.array(true_ranges)
        atr = np.mean(true_ranges[:period])

        for i in range(period, len(true_ranges)):
            atr = (atr * (period - 1) + true_ranges[i]) / period

        return atr
