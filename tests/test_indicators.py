import unittest
from indicators.sar import SAR

class TestIndicators(unittest.TestCase):
    def test_sar(self):
        highs = [101, 103, 102, 104, 106, 105, 107, 108, 109]
        lows = [99, 101, 100, 102, 104, 103, 105, 106, 107]
        sar = SAR.calculate(highs, lows)
        self.assertIsNotNone(sar)
        # Add more assertions as needed

if __name__ == '__main__':
    unittest.main()
