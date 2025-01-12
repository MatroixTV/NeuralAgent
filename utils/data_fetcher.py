import MetaTrader5 as mt5
import pandas as pd


class DataFetcher:
    """
    Fetches market data from MetaTrader 5.
    """

    @staticmethod
    def fetch_data(symbol, num_candles=100, timeframe=mt5.TIMEFRAME_M1):
        """
        Fetch historical data from MetaTrader 5.
        :param symbol: Trading symbol (e.g., "EURUSD")
        :param num_candles: Number of candles to fetch
        :param timeframe: Timeframe for historical data (default: M1)
        :return: DataFrame with market data
        """
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
        if rates is None or len(rates) == 0:
            raise ValueError(f"Failed to fetch data for {symbol}")

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        return df
