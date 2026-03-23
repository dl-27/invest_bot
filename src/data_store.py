"""
src/data_store.py
-----------------
Downloads fundamental data (including Free Cash Flow) and price histories
Saves to local CSVs for offline processing later
"""

import os
import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import logging
import config
from data_loader import DataLoader

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = "data"
UPDATE_FILE = os.path.join(DATA_DIR, "last_update.txt")

def ensure_directories():
    """Creates necessary folders if they don't exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(os.path.join(DATA_DIR, "history")):
        os.makedirs(os.path.join(DATA_DIR, "history"))


def fetch_all_data(progress_callback=None):
    ensure_directories()
    loader = DataLoader()

    total_tickers = sum(len(tickers) for sector in config.SECTOR_UNIVERSE.values() for tickers in sector.values())
    processed = 0

    for sector, regions in config.SECTOR_UNIVERSE.items():
        for region, tickers in regions.items():
            data_list = []
            for ticker in tickers:
                processed += 1
                if progress_callback:
                    progress_callback(processed / total_tickers, f"Downloading: {ticker}")

                try:
                    # FUNDAMENTALS
                    stock = yf.Ticker(ticker)
                    info = stock.info

                    data_list.append({
                        "Ticker": ticker,
                        "Company Name": info.get('shortName', ticker),
                        "Current_Price": info.get('currentPrice') or info.get('regularMarketPrice'),
                        "Market_Cap": info.get('marketCap'),
                        "Trailing_PE": info.get('trailingPE'),
                        "Price_to_Book": info.get('priceToBook'),
                        "Price_to_Sales": info.get('priceToSalesTrailing12Months'),
                        "Revenue_Growth": info.get('revenueGrowth'),
                        "Earnings_Growth": info.get('earningsGrowth'),
                        "Profit_Margin": info.get('profitMargins'),
                        "Free_Cash_Flow": info.get('freeCashflow'),
                        "Div_2025": info.get('trailingAnnualDividendRate', 0)  # Pulled directly from info
                    })

                    # HISTORY 1 year
                    loader.fetch_price_history(ticker, period="1y", local_only=False)

                    time.sleep(0.1)
                except Exception as e:
                    logger.warning(f"Error {ticker}: {e}")

            if data_list:
                df = pd.DataFrame(data_list)
                filename = f"{sector}_{region}.csv".replace(" & ", "_").replace(" ", "_")
                df.to_csv(os.path.join(DATA_DIR, filename), index=False)

    with open(UPDATE_FILE, "w") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if progress_callback:
        progress_callback(1.0, "Database Update Complete!")

def get_last_update():
    """Returns the timestamp of the last successful database update."""
    if os.path.exists(UPDATE_FILE):
        with open(UPDATE_FILE, "r") as f:
            return f.read().strip()
    return "Never"
