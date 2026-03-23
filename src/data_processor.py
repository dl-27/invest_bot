"""
src/data_processor.py
---------------------
The ETL Engine: Calculates Sector-Normalized Value and FCF-Weighted Growth
"""

import pandas as pd
import logging
from data_loader import DataLoader
import config

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MASTER_FILE = "data/master_metrics.csv"

def build_master_table(progress_callback=None):
    """
    Loops through local csv, calculates sector-relative metrics,
    and incorporates Free Cash Flow into the growth engine.
    """
    logger.info("Starting Offline Batch Processing (Sector Normalization Enabled)...")
    loader = DataLoader()
    results = []

    total_tasks = sum(len(tickers) for sector in config.SECTOR_UNIVERSE.values() for tickers in sector.values())
    completed = 0

    for sector in config.SECTOR_UNIVERSE.keys():
        for region in config.REGIONS:

            fund_df = loader.get_market_data(sector, region)
            if fund_df.empty:
                continue

            for _, row in fund_df.iterrows():
                ticker = row['Ticker']
                name = row.get('Company Name', ticker)

                # Extract Fundamentals
                pe_ratio = row.get('Trailing_PE', None)
                pb_ratio = row.get('Price_to_Book', row.get('PriceToBook', None))
                ps_ratio = row.get('Price_to_Sales', row.get('PriceToSalesTrailing12Months', None))

                rev_growth = row.get('Revenue_Growth', 0)
                earn_growth = row.get('Earnings_Growth', 0)
                prof_margin = row.get('Profit_Margin', 0)
                fcf = row.get('Free_Cash_Flow', 0) # New field from updated data_store

                # Extract Momentum
                hist = loader.fetch_price_history(ticker, local_only=True)
                momentum_6m, momentum_12m = 0, 0

                if not hist.empty and 'Close' in hist.columns:
                    try:
                        closes = hist['Close']
                        if isinstance(closes, pd.DataFrame):
                            closes = closes.iloc[:, 0]

                        current_price = float(closes.values[-1])
                        if len(closes) >= 126:
                            p_6m = float(closes.values[-126])
                            momentum_6m = ((current_price - p_6m) / p_6m) * 100
                        if len(closes) >= 2:
                            p_12m = float(closes.values[0])
                            momentum_12m = ((current_price - p_12m) / p_12m) * 100
                    except Exception as e:
                        logger.warning(f"Momentum error for {ticker}: {e}")

                results.append({
                    "Ticker": ticker,
                    "Name": name,
                    "Sector": sector,
                    "Region": region,
                    "P/E Ratio": pe_ratio,
                    "P/B Ratio": pb_ratio,
                    "P/S Ratio": ps_ratio,
                    "Revenue Growth (%)": float(rev_growth) * 100 if pd.notnull(rev_growth) else 0,
                    "Earnings Growth (%)": float(earn_growth) * 100 if pd.notnull(earn_growth) else 0,
                    "Profit Margin (%)": float(prof_margin) * 100 if pd.notnull(prof_margin) else 0,
                    "Free Cash Flow": float(fcf) if pd.notnull(fcf) else 0,
                    "Div_2025": float(row.get('Div_2025', 0)),
                    "Momentum 6M (%)": momentum_6m,
                    "Momentum 12M (%)": momentum_12m
                })

                completed += 1
                if progress_callback and completed % 15 == 0:
                    prog = min(completed / total_tasks, 1.0)
                    progress_callback(prog, f"Normalizing Sector Data... ({completed}/{total_tasks})")

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)

    # SECTOR NORMALIZED VALUE SCORING
    # Ranks stocks against peers in the same industry
    def calculate_sector_value(group):
        # Fill missing with 2x median to penalize reasonably
        pe_s = group['P/E Ratio'].fillna(group['P/E Ratio'].median() * 2).rank(pct=True, ascending=False)
        pb_s = group['P/B Ratio'].fillna(group['P/B Ratio'].median() * 2).rank(pct=True, ascending=False)
        ps_s = group['P/S Ratio'].fillna(group['P/S Ratio'].median() * 2).rank(pct=True, ascending=False)
        return (pe_s + pb_s + ps_s) / 3

    df['Value Score'] = df.groupby('Sector', group_keys=False).apply(calculate_sector_value) * 100

    # FCF-WEIGHTED GROWTH SCORING
    # Rewards high revenue/earnings growth + positive cash generation
    df['Rev_Rank'] = df['Revenue Growth (%)'].rank(pct=True)
    df['Earn_Rank'] = df['Earnings Growth (%)'].rank(pct=True)
    df['FCF_Rank'] = df['Free Cash Flow'].apply(lambda x: 1.0 if x > 0 else 0.5).rank(pct=True)

    df['Growth Score'] = ((df['Rev_Rank'] + df['Earn_Rank'] + df['FCF_Rank']) / 3) * 100

    # MOMENTUM SCORING
    df['Mom6_Rank'] = df['Momentum 6M (%)'].rank(pct=True)
    df['Mom12_Rank'] = df['Momentum 12M (%)'].rank(pct=True)
    df['Momentum Score'] = ((df['Mom6_Rank'] + df['Mom12_Rank']) / 2) * 100

    # OVERALL SCORE & SCALING
    df['Overall AI Score'] = (df['Value Score'] + df['Growth Score'] + df['Momentum Score']) / 3

    def scale_1_5(series):
        return pd.cut(series, bins=[-1, 20, 40, 60, 80, 101], labels=[5, 4, 3, 2, 1]).astype(int)

    for col in ['Value Score', 'Growth Score', 'Momentum Score', 'Overall AI Score']:
        df[col] = scale_1_5(df[col])

    # Cleanup and Save
    cols_to_drop = ['Rev_Rank', 'Earn_Rank', 'FCF_Rank', 'Mom6_Rank', 'Mom12_Rank']
    df = df.drop(columns=cols_to_drop).round(2).sort_values(by='Overall AI Score')
    df.to_csv(MASTER_FILE, index=False)

    if progress_callback:
        progress_callback(1.0, "Master Database (Normalized) Generated.")
    return df
