import streamlit as st

def render_tab(master_df, regions, sectors):
    st.header("Value Rankings (Sector-Normalized)")

    with st.expander("**How to Read Normalized Value Scores**"):
        st.markdown("""
        **Goal:** Find "Cheap" stocks relative to their specific industry peers.
        * **Sector Normalization:** We compare Tech companies to Tech medians, and Banks to Bank medians.
        * **1 (Strong Buy):** Top-tier value within its specific sector.
        * **5 (Strong Sell):** Significantly overvalued relative to its specific sector.
        """)

    st.markdown("### Filter Market Universe")
    col1, col2 = st.columns(2)
    with col1:
        selected_reg = st.selectbox("Filter by Region:", ["All"] + regions, key="val_table_reg")
    with col2:
        selected_sec = st.selectbox("Filter by Sector:", ["All"] + sectors, key="val_table_sec")

    filtered_df = master_df.copy()
    if selected_reg != "All":
        filtered_df = filtered_df[filtered_df['Region'] == selected_reg]
    if selected_sec != "All":
        filtered_df = filtered_df[filtered_df['Sector'] == selected_sec]

    # Added raw ratios for better transparency
    display_cols = ['Ticker', 'Name', 'Sector', 'P/E Ratio', 'P/B Ratio', 'Value Score']
    display_df = filtered_df[display_cols].sort_values(by='Value Score', ascending=True)

    st.success(f"Showing {len(display_df)} companies matching criteria.")
    st.dataframe(
        display_df.style.background_gradient(subset=['Value Score'], cmap='RdYlGn_r', vmin=1, vmax=5),
        use_container_width=True,
        hide_index=True
    )
