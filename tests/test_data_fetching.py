import MetaTrader5 as mt5
import pandas as pd

# Initialize MetaTrader 5
if not mt5.initialize():
    print("MetaTrader5 initialization failed")
else:
    print("MetaTrader5 connected")

# Fetch historical data
symbol = "EURUSD"  # Update if suffixes are required
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)

if rates is None or len(rates) == 0:
    print(f"Failed to fetch data for {symbol}")
else:
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    print(df.head())

# Shutdown MetaTrader 5
mt5.shutdown()
