"""
src/app.py
----------
Main UI for Static Data.
"""

import streamlit as st
import config
from data_loader import DataLoader

st.set_page_config(page_title=config.APP_TITLE, page_icon=config.APP_ICON, layout="wide")
loader = DataLoader()

# Sidebar
st.sidebar.title(f"{config.APP_ICON} Controls")
selected_sector = st.sidebar.selectbox("Choose a Sector:", config.SECTORS)

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()

# Main Content
st.title(f"{config.APP_TITLE}")
st.markdown(f"### Global Analysis: **{selected_sector}**")

# Tabs
main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs(["Market Overview", "Momentum", "Value", "News"])

with main_tab1:
    # Region Sub-tabs
    region_tabs = st.tabs([f"{r}" for r in config.REGIONS])

    @st.cache_data
    def load_data(sec, reg):
        return loader.get_stocks_by_region(sec, reg)

    for i, region_name in enumerate(config.REGIONS):
        with region_tabs[i]:
            with st.spinner(f"Loading {region_name} data..."):
                df = load_data(selected_sector, region_name)

                if not df.empty:
                    # Formatting
                    df.index = df.index + 1
                    cols = ["Company Name", "Ticker", "Current_Price", "Market_Cap", "Trailing_PE", "Revenue_Growth"]
                    # Filter columns that exist
                    cols = [c for c in cols if c in df.columns]

                    # Metrics
                    c1, c2 = st.columns(2)
                    c1.metric(f"Companies Loaded", len(df))

                    # Show Table
                    st.dataframe(df[cols], use_container_width=True)
                else:
                    st.warning("No data loaded. Check internet connection or API limits.")

with main_tab2: st.info("Step 2: Momentum Analysis coming soon.")
with main_tab3: st.info("Step 3: Value Analysis coming soon.")
with main_tab4: st.info("Step 5: Sentiment coming soon.")