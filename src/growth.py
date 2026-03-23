import streamlit as st

def render_tab(master_df, regions, sectors):
    st.header("Growth Rankings (FCF-Quality Adjusted)")

    with st.expander("**How to Read Growth Scores**"):
        st.markdown("""
        **Goal:** Find high-speed companies that also generate real cash.
        * **FCF Quality:** Companies with positive Free Cash Flow receive a higher rank than "paper-only" growth.
        * **1 (Strong Buy):** Hypergrowth with strong cash-flow generation.
        * **5 (Strong Sell):** Stagnating or cash-burning growth.
        """)

    st.markdown("### Filter Market Universe")
    col1, col2 = st.columns(2)
    with col1:
        selected_reg = st.selectbox("Filter by Region:", ["All"] + regions, key="grow_table_reg")
    with col2:
        selected_sec = st.selectbox("Filter by Sector:", ["All"] + sectors, key="grow_table_sec")

    filtered_df = master_df.copy()
    if selected_reg != "All":
        filtered_df = filtered_df[filtered_df['Region'] == selected_reg]
    if selected_sec != "All":
        filtered_df = filtered_df[filtered_df['Sector'] == selected_sec]

    display_cols = ['Ticker', 'Name', 'Revenue Growth (%)', 'Free Cash Flow', 'Growth Score']
    display_df = filtered_df[display_cols].sort_values(by='Growth Score', ascending=True)

    st.success(f"Showing {len(display_df)} companies matching criteria.")
    st.dataframe(
        display_df.style.background_gradient(subset=['Growth Score'], cmap='RdYlGn_r', vmin=1, vmax=5),
        use_container_width=True,
        hide_index=True
    )
