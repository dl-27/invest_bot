"""
src/data_loader.py
------------------
Handles loading saved CSV data for fundamentals and
fetching/loading price history for charts and momentum calculations
"""

import os
import pandas as pd
import yfinance as yf
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.history_dir = os.path.join(data_dir, "history")

    def get_market_data(self, sector, region):
        """Loads fundamental data from saved sector/region CSVs"""
        filename = f"{sector}_{region}.csv".replace(" & ", "_").replace(" ", "_")
        filepath = os.path.join(self.data_dir, filename)

        if os.path.exists(filepath):
            try:
                return pd.read_csv(filepath)
            except Exception as e:
                logger.error(f"Error reading {filepath}: {e}")

        return pd.DataFrame()

    def fetch_price_history(self, ticker, period="1y", local_only=False):
        """
        Fetches price history for 1 year to save time and space
        If local_only=True, it reads from the hard drive
        If local_only=False, it fetches from Yahoo and saves it locally
        """
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)

        file_path = os.path.join(self.history_dir, f"{ticker}_history.csv")

        # OFFLINE MODE
        if local_only:
            if os.path.exists(file_path):
                try:
                    hist = pd.read_csv(file_path, index_col="Date", parse_dates=True)
                    return hist
                except Exception as e:
                    logger.warning(f"Could not read local history for {ticker}: {e}")
            return pd.DataFrame()

        # ONLINE MODE
        try:
            hist = yf.download(ticker, period=period, interval="1d", auto_adjust=True, progress=False)

            # Clean up Yahoo formatting
            if isinstance(hist.columns, pd.MultiIndex):
                hist.columns = hist.columns.droplevel('Ticker')

            if not hist.empty:
                hist.to_csv(file_path)
            return hist
        except Exception as e:
            logger.error(f"Failed to fetch live history for {ticker}: {e}")
            return pd.DataFrame()
