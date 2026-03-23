"""
src/app.py
----------
The main file for the Invest Bot
Features: Sector Overviews, Technical Momentum, Value/Growth Rankings, AI Chatbot, and Sentiment
"""

import streamlit as st
import os
import pandas as pd
import config
import data_store
from data_loader import DataLoader
import momentum
import growth
import value
import data_processor
import chatbot
import sentiment

# --- 1. Page Configuration ---
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide"
)

# --- 2. Initialize Session State ---
if "loader" not in st.session_state:
    st.session_state.loader = DataLoader()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. Sidebar: Control Panel ---
st.sidebar.title(f"{config.APP_ICON} Control Center")

if st.sidebar.button("Update Database"):
    with st.spinner("Syncing with Yahoo Finance..."):
        progress_bar = st.sidebar.progress(0)
        data_store.fetch_all_data(lambda p, t: progress_bar.progress(p))
        st.sidebar.success("Database Updated!")
        st.rerun()

if st.sidebar.button("Count Indicators"):
    with st.spinner("Processing local metrics..."):
        progress_bar = st.sidebar.progress(0)
        data_processor.build_master_table(progress_callback=lambda p, t: progress_bar.progress(p))
        st.sidebar.success("Master Table Ready!")
        st.rerun()

st.sidebar.divider()
selected_sector = st.sidebar.selectbox("Active Sector Context:", config.SECTORS)

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# --- 4. Main UI Flow ---
st.title(f"{config.APP_ICON} {config.APP_TITLE}")

MASTER_FILE = "data/master_metrics.csv"
if not os.path.exists(MASTER_FILE):
    st.warning("Please use the sidebar to 'Update Database' then 'Count Indicators' to begin.")
else:
    master_df = pd.read_csv(MASTER_FILE)
    tabs = st.tabs(["Overview", "Momentum", "Value", "Growth", "AI Advisor", "Sentiment"])

    # --- TAB 1: OVERVIEW ---
    with tabs[0]:
        st.subheader(f"Current Market Data: {selected_sector}")
        region_tabs = st.tabs(config.REGIONS)

        for i, region in enumerate(config.REGIONS):
            with region_tabs[i]:
                df = st.session_state.loader.get_market_data(selected_sector, region)

                if not df.empty:
                    score_cols = ["Ticker", "Momentum Score", "Value Score", "Growth Score", "Overall AI Score"]
                    overview_display = pd.merge(df, master_df[score_cols], on="Ticker", how="left")

                    cols_to_show = ["Company Name", "Ticker", "Current_Price", "Div_2025", "Momentum Score", "Value Score", "Growth Score", "Overall AI Score"]
                    final_cols = [c for c in cols_to_show if c in overview_display.columns]

                    st.dataframe(
                        overview_display[final_cols].style.format({
                            "Current_Price": "{:.2f}",  # Rounds to 2 decimal places
                            "Div_2025": "{:.2f}"
                        }, na_rep="N/A").background_gradient(
                            subset=["Momentum Score", "Value Score", "Growth Score", "Overall AI Score"],
                            cmap='RdYlGn_r',
                            vmin=1,
                            vmax=5
                        ),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info(f"No local data for {region} {selected_sector}")

    with tabs[1]:
        momentum.render_momentum_tab(master_df=master_df, loader=st.session_state.loader)
    with tabs[2]:
        value.render_tab(master_df, config.REGIONS, config.SECTORS)
    with tabs[3]:
        growth.render_tab(master_df, config.REGIONS, config.SECTORS)

    # --- TAB 5: AI ADVISOR ---
    with tabs[4]:
        st.header("AI Investment Advisor")
        st.caption("Grounded in Momentum, Value, and Growth local scores.")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask about top stocks..."):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                with st.status("Advisor is working...", expanded=True) as status:
                    st.write("Searching Master Table for relevant metrics...")
                    st.write("Connecting to local Llama 3 brain...")

                    response_placeholder = st.empty()
                    full_response = ""

                    stream = chatbot.get_chatbot_response(prompt, master_df)

                    if stream == "OFFLINE_ERROR":
                        status.update(label="Ollama Offline", state="error")
                        st.error("Ollama is not running. Please open the Ollama app on your computer.")
                    elif isinstance(stream, str) and stream.startswith("GENERAL_ERROR"):
                        status.update(label="Error", state="error")
                        st.error(stream)
                    else:
                        try:
                            status.update(label="Analyzing Data...", state="running")
                            for chunk in stream:
                                content = chunk['message']['content']
                                full_response += content
                                response_placeholder.markdown(full_response + "▌")

                            status.update(label="Complete", state="complete", expanded=False)
                            response_placeholder.markdown(full_response)
                        except Exception:
                            status.update(label="Connection Lost", state="error")
                            st.error("Lost connection to Ollama mid-stream.")

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        # --- TAB 6: NEWS SENTIMENT ---
        with tabs[5]:
            st.header("News Sentiment Analysis")
            st.caption("AI-powered analysis of the latest relevant headlines.")

            # Selection based on Sidebar Sector
            available_tickers = []
            for reg in config.REGIONS:
                available_tickers.extend(config.SECTOR_UNIVERSE[selected_sector].get(reg, []))

            selected_ticker = st.selectbox("Select Stock for Deep Dive:", available_tickers)

            if st.button(f"Analyze Sentiment for {selected_ticker}"):
                # Look up company name from master_df for the AI prompt
                stock_info = master_df[master_df['Ticker'] == selected_ticker].iloc[0]
                name = stock_info['Name']

                with st.status(f"Processing headlines for {name}...", expanded=True) as status:
                    st.write("Fetching RSS feed from Yahoo Finance...")
                    avg_score, news_results = sentiment.process_sentiment_for_ticker(selected_ticker, name)

                    if not news_results:
                        status.update(label="No Relevant News", state="error")
                        st.warning(f"No recent headlines found that mention {selected_ticker} or {name}.")
                    else:
                        status.update(label=f"Analysis Complete (Avg: {avg_score})", state="complete")

                        # Display the Summary Metric
                        st.metric("Aggregate Sentiment Score (1-5)", avg_score, help="1=Bullish, 5=Bearish")

                        # Display the Detailed News Table
                        st.subheader("Analyzed Headlines")
                        news_df = pd.DataFrame(news_results)

                        news_df.columns = ["Headline", "Source Link", "AI Score", "AI Reasoning"]

                        st.dataframe(
                            news_df.style.background_gradient(
                                subset=['AI Score'],
                                cmap='RdYlGn_r',
                                vmin=1,
                                vmax=5
                            ).format({"AI Score": "{:.0f}"}),  # Keep score as an integer
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Source Link": st.column_config.LinkColumn("Source Link"),
                                "Headline": st.column_config.TextColumn("Headline", width="large"),
                                "AI Reasoning": st.column_config.TextColumn("AI Reasoning", width="medium")
                            }
                        )
