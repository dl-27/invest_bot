"""
src/data_loader.py
------------------
Static Data Loader.
Fetches data for the hardcoded tickers in config.py.
"""

import yfinance as yf
import pandas as pd
import config

class DataLoader:
    def __init__(self):
        self.universe = config.SECTOR_UNIVERSE

    def fetch_fundamentals(self, ticker):
        """
        Fetches single stock data using yfinance.
        """
        try:
            # Optimize: 'fast_info' is faster, but 'info' has the fields we need.
            stock = yf.Ticker(ticker)
            info = stock.info

            # Basic validation: ensure we got data
            if not info or 'regularMarketPrice' not in info:
                # Sometimes yfinance returns empty info but doesn't raise error
                pass

            data = {
                "Ticker": ticker,
                "Company Name": info.get("longName", info.get("shortName", ticker)),
                "Current_Price": info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
                "Market_Cap": info.get("marketCap", 0),
                "Trailing_PE": info.get("trailingPE", None),
                "Revenue_Growth": info.get("revenueGrowth", None),
                "Profit_Margins": info.get("profitMargins", None)
            }
            return data
        except Exception:
            # print(f"Error: {e}") # keep silent for UI cleanliness
            return None

    def get_stocks_by_region(self, sector_name, region_name):
        """
        Gets the hardcoded list from config and fetches data.
        """
        # 1. Get List
        sector_data = self.universe.get(sector_name, {})
        tickers = sector_data.get(region_name, [])

        results = []
        if tickers:
            print(f"Fetching {len(tickers)} stocks for {region_name} - {sector_name}...")

            # 2. Loop and Fetch
            for ticker in tickers:
                data = self.fetch_fundamentals(ticker)
                if data:
                    results.append(data)

        return pd.DataFrame(results)