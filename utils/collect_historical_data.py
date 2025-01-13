import yfinance as yf
import pandas as pd

class YahooFinanceDataCollector:
    """
    Collects historical Forex data for EUR/USD using Yahoo Finance.
    """

    def __init__(self, symbol="EURUSD=X"):
        self.symbol = symbol

    def fetch_data(self, start_date, end_date, interval="1d"):
        """
        Fetch historical data for a given date range and interval.

        :param start_date: Start date (YYYY-MM-DD)
        :param end_date: End date (YYYY-MM-DD)
        :param interval: Interval (e.g., '1d', '1wk', '1mo', '1h')
        :return: DataFrame with historical data
        """
        print(f"Fetching data for {self.symbol} from {start_date} to {end_date} at {interval} interval...")
        data = yf.download(
            tickers=self.symbol,
            start=start_date,
            end=end_date,
            interval=interval
        )

        if data.empty:
            raise Exception(f"No data fetched for {self.symbol} with interval {interval}.")

        # Format DataFrame
        data.reset_index(inplace=True)

        # Handle 'Datetime' for intraday data
        date_column = "Datetime" if "Datetime" in data.columns else "Date"
        data = data.rename(columns={
            date_column: "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adjusted_close",
            "Volume": "volume"
        })
        return data[["date", "open", "high", "low", "close"]]

    def save_to_csv(self, data, filename):
        """
        Save DataFrame to a CSV file.

        :param data: DataFrame to save
        :param filename: File path for saving the data
        """
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


if __name__ == "__main__":
    collector = YahooFinanceDataCollector(symbol="EURUSD=X")

    # Define date range and intervals
    start_date = "2025-01-01"
    end_date = "2025-01-13"
    interval = "1h"  # '1d' for daily data, '1h' for hourly

    try:
        data = collector.fetch_data(start_date=start_date, end_date=end_date, interval=interval)
        collector.save_to_csv(data, "EURUSD_hourly.csv")
    except Exception as e:
        print(f"Error: {e}")
