class SAR:
    """
    Implements the Parabolic SAR indicator.
    """

    @staticmethod
    def calculate(highs, lows, af=0.02, max_af=0.2):
        """
        Calculate Parabolic SAR.

        :param highs: List or numpy array of high prices
        :param lows: List or numpy array of low prices
        :param af: Acceleration factor (default: 0.02)
        :param max_af: Maximum acceleration factor (default: 0.2)
        :return: SAR value as a float
        """
        if len(highs) < 2 or len(lows) < 2:
            raise ValueError("Not enough data to calculate SAR")

        sar = lows[0] - af * (highs[0] - lows[0])
        trend_up = True  # Assuming the initial trend is upward

        for i in range(1, len(highs)):
            if trend_up:
                sar = sar + af * (highs[i - 1] - sar)
                if sar > lows[i]:
                    sar = highs[i]
                    af = min(af + 0.02, max_af)
                    trend_up = False
            else:
                sar = sar + af * (lows[i - 1] - sar)
                if sar < highs[i]:
                    sar = lows[i]
                    af = min(af + 0.02, max_af)
                    trend_up = True

        return sar
