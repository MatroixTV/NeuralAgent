from indicators.rsi import RSI
from indicators.ema import EMA
from indicators.atr import ATR
from indicators.sar import SAR

# Mock data for testing
prices = [100, 102, 101, 103, 105, 104, 106, 107, 108, 107, 106, 105, 104, 102, 101]
highs = [101, 103, 102, 104, 106, 105, 107, 108, 109, 108, 107, 106, 105, 103, 102]
lows = [99, 101, 100, 102, 104, 103, 105, 106, 107, 106, 105, 104, 103, 101, 100]
closes = prices

def test_rsi():
    rsi = RSI.calculate(prices, period=14)
    print("RSI:", rsi)
    assert isinstance(rsi, float), "RSI should return a float value"

def test_ema():
    ema = EMA.calculate(prices, period=14)
    print("EMA:", ema)
    assert isinstance(ema, float), "EMA should return a float value"

def test_atr():
    atr = ATR.calculate(highs, lows, closes, period=14)
    print("ATR:", atr)
    assert isinstance(atr, float), "ATR should return a float value"

def test_sar():
    sar = SAR.calculate(highs, lows)
    print("SAR:", sar)
    assert isinstance(sar, float), "SAR should return a float value"
