"""
src/momentum.py
---------------
Technical analysis module using pandas_ta
Features: Leaderboard with Local Filters (Region/Sector), Momentum Heatmaps,
and Expandable Plotly Technical Charts.
"""

import streamlit as st
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config

def calculate_indicators(df):
    """
    Calculates technical indicators for the provided price history
    Includes SMA 20/50, RSI, and MACD
    """
    if df is None or df.empty:
        return df

    # Standardize column names to lowercase for pandas_ta compatibility
    df.columns = [c.lower() for c in df.columns]

    # Moving Averages
    df['sma_20'] = ta.sma(df['close'], length=20)
    df['sma_50'] = ta.sma(df['close'], length=50)

    # RSI
    df['rsi'] = ta.rsi(df['close'], length=14)

    # MACD
    macd = ta.macd(df['close'])
    if macd is not None:
        df = pd.concat([df, macd], axis=1)

    return df

def plot_charts(df, ticker):
    """
    Generates a Plotly chart for technical info
    1: Price + SMAs
    2: RSI
    3: MACD
    """
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.2, 0.3],
        subplot_titles=(f"{ticker} Price & Trends", "Relative Strength Index (RSI)", "MACD Histogram")
    )

    # Price and SMAs
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], name="Price", line=dict(color='white')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['sma_20'], name="SMA 20", line=dict(color='orange', width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['sma_50'], name="SMA 50", line=dict(color='cyan', width=1)), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['rsi'], name="RSI", line=dict(color='purple')), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # MACD
    macd_col = [c for c in df.columns if 'macd_' in c.lower() and 's' not in c.lower() and 'h' not in c.lower()]
    sig_col = [c for c in df.columns if 'macds' in c.lower()]
    hist_col = [c for c in df.columns if 'macdh' in c.lower()]

    if macd_col and sig_col:
        fig.add_trace(go.Scatter(x=df.index, y=df[macd_col[0]], name="MACD", line=dict(color='blue')), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df[sig_col[0]], name="Signal", line=dict(color='orange')), row=3, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df[hist_col[0]], name="Hist"), row=3, col=1)

    fig.update_layout(height=800, template="plotly_dark", showlegend=False)
    return fig

def render_momentum_tab(master_df, loader):
    """
    Renders the Momentum tab with local filters for Region and Sector
    """
    st.header("Momentum Leaderboard")
    st.caption("Score 1 = High Momentum (Bullish), Score 5 = Low Momentum (Bearish).")

    # Local Filters (Aligning with Value/Growth tabs)
    col1, col2 = st.columns(2)
    with col1:
        sel_reg = st.selectbox("Filter by Region:", config.REGIONS, key="mom_reg_filter")
    with col2:
        sel_sec = st.selectbox("Filter by Sector:", config.SECTORS, key="mom_sec_filter")

    # Filter data from Master Table
    df = master_df[(master_df['Sector'] == sel_sec) & (master_df['Region'] == sel_reg)].copy()

    if df.empty:
        st.info(f"No local indicators found for {sel_reg} {sel_sec}. Ensure you have updated the database.")
        return

    # Summary Table: Momentum Score only
    # Sorted by Momentum Score (Best to Worst)
    display_df = df[["Ticker", "Name", "Momentum Score"]].sort_values("Momentum Score")

    st.dataframe(
        display_df.style.background_gradient(
            subset=['Momentum Score'],
            cmap='RdYlGn_r', # Green for 1, Red for 5
            vmin=1,
            vmax=5
        ),
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    st.subheader("Technical charts")
    st.info("Click on a stock to expand its technical charts.")

    # Expandable Rows (Dropdown effect)
    for _, row in display_df.iterrows():
        ticker = row['Ticker']
        name = row['Name']
        score = row['Momentum Score']

        expander_label = f"{ticker} — {name} (Momentum Score: {score})"

        with st.expander(expander_label):
            # Only generate chart on button click to save memory/performance
            if st.button(f"Analyze Technicals for {ticker}", key=f"btn_{ticker}"):
                with st.spinner(f"Fetching {ticker} history..."):
                    hist = loader.fetch_price_history(ticker, local_only=True)

                    if not hist.empty:
                        hist_enriched = calculate_indicators(hist)
                        fig = plot_charts(hist_enriched, ticker)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"Historical data for {ticker} not found.")
