# indicators/ema.py
import numpy as np

class EMA:
    @staticmethod
    def calculate(prices, period):
        """
        Calculate the Exponential Moving Average (EMA).

        :param prices: List or numpy array of prices
        :param period: The period for calculating EMA
        :return: EMA value
        """
        prices = np.array(prices)
        if len(prices) < period:
            raise ValueError("Not enough data to calculate EMA")

        multiplier = 2 / (period + 1)
        ema = prices[0]

        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema

        return ema
