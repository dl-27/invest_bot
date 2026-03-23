import ollama
import httpx
import config

def get_chatbot_response(user_query, master_df):
    query_l = user_query.lower()
    filtered_df = master_df.copy()

    # DYNAMIC FILTERING
    for region in config.REGIONS:
        if region.lower() in query_l:
            filtered_df = filtered_df[filtered_df['Region'] == region]

    for sector in config.SECTORS:
        if sector.lower() in query_l:
            filtered_df = filtered_df[filtered_df['Sector'] == sector]

    # SORTING
    sort_col = 'Overall AI Score'
    if 'value' in query_l:
        sort_col = 'Value Score'
    elif 'growth' in query_l:
        sort_col = 'Growth Score'
    elif 'momentum' in query_l:
        sort_col = 'Momentum Score'

    # CONTEXT EXTRACTION (Top 15 by default)
    context_data = filtered_df.nsmallest(15, sort_col)

    subset_cols = ['Ticker', 'Name', 'Region', 'Sector', 'Value Score', 'Growth Score', 'Momentum Score',
                   'Overall AI Score', 'Free Cash Flow']
    context_str = context_data[subset_cols].to_markdown(index=False)

    # SYSTEM PROMPT
    system_prompt = f"""
    You are the 'Invest Bot' AI Advisor. Use the provided CSV data to answer.

    CURRENT DATASET:
    {context_str}

    SCORING LOGIC:
    - 1 is the best (Top 20% of Sector), 5 is the worst.
    - Value Scores are sector-normalized (e.g., Tech vs Tech).
    - Growth Scores incorporate Free Cash Flow (FCF) quality.

    INSTRUCTIONS:
    - Explain that rankings are relative to industry peers.
    - If a stock has high FCF, mention it as a sign of 'Quality Growth'.
    - Use specific scores from the table to justify recommendations.
    - Always include the financial disclaimer at the end.
    """

    try:
        stream = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_query},
            ],
            stream=True,
        )
        return stream
    except httpx.ConnectError:
        return "OFFLINE_ERROR"
    except Exception as e:
        return f"GENERAL_ERROR: {str(e)}"
