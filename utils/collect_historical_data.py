import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

def initialize_mt5():
    """
    Initialize the MetaTrader 5 connection.
    """
    if not mt5.initialize():
        print(f"Failed to initialize MT5: {mt5.last_error()}")
        return False
    print("MT5 initialized successfully.")
    return True

def fetch_mt5_data(symbol, timeframe, start_date, end_date):
    """
    Fetch historical data from MT5.

    Args:
        symbol (str): Trading symbol (e.g., 'EURUSD').
        timeframe (int): MT5 timeframe constant (e.g., mt5.TIMEFRAME_H1).
        start_date (datetime): Start date for historical data.
        end_date (datetime): End date for historical data.

    Returns:
        pd.DataFrame: Historical data as a Pandas DataFrame.
    """
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    if rates is None:
        print(f"Failed to fetch data for {symbol}: {mt5.last_error()}")
        return None

    # Convert to DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert UNIX time to datetime
    return df

def save_data_to_csv(data, symbol, timeframe_label, output_dir="data"):
    """
    Save historical data to CSV.

    Args:
        data (pd.DataFrame): Historical data.
        symbol (str): Trading symbol.
        timeframe_label (str): Timeframe label (e.g., '1h', '4h').
        output_dir (str): Directory to save CSV files.
    """
    file_path = f"{output_dir}/{symbol}_{timeframe_label}.csv"
    data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def main():
    # Initialize MT5
    if not initialize_mt5():
        return

    # Define symbols, timeframes, and date range
    symbols = ["EURUSD", "GBPUSD", "USDJPY"]
    timeframes = {
        "1h": mt5.TIMEFRAME_H1,
        "4h": mt5.TIMEFRAME_H4,
        "1d": mt5.TIMEFRAME_D1
    }
    start_date = datetime.now() - timedelta(days=3650)  # 1 year of data
    end_date = datetime.now()

    # Fetch and save data
    for symbol in symbols:
        for timeframe_label, timeframe_const in timeframes.items():
            print(f"Fetching {symbol} ({timeframe_label})...")
            data = fetch_mt5_data(symbol, timeframe_const, start_date, end_date)
            if data is not None:
                save_data_to_csv(data, symbol, timeframe_label)

    # Shutdown MT5
    mt5.shutdown()

if __name__ == "__main__":
    main()
