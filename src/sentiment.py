"""
src/sentiment.py
----------------
Sentiment Engine.
Uses Feedparser for data and Ollama (Llama 3) for deep-reasoning scoring
"""

import feedparser
import ollama
import json

# Configuration
MODEL_NAME = "llama3"
OLLAMA_URL = "http://localhost:11434"

def fetch_ticker_news(ticker, limit=20):
    """Fetches and cleans headlines from Yahoo Finance RSS"""
    rss_url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
    feed = feedparser.parse(rss_url)

    news_items = []
    for entry in feed.entries[:20]:
        news_items.append({
            "title": entry.title,
            "link": entry.link,
            "published": getattr(entry, 'published', 'N/A')
        })
    return news_items

def analyze_sentiment_local(ticker, company_name, headline):
    """Uses Local Llama 3 to score a single headline"""
    prompt = f"""
    Analyze the sentiment of this financial headline for {company_name} ({ticker}).
    
    HEADLINE: "{headline}"
    
    SCORING RULES:
    1 = Extremely Positive (Bullish)
    2 = Slightly Positive
    3 = Neutral
    4 = Slightly Negative
    5 = Extremely Negative (Bearish)
    
    Respond ONLY with a JSON object in this format:
    {{"score": int, "reason": "one sentence explanation"}}
    """

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1}
        )

        # Parse the JSON from the AI response
        result = json.loads(response['message']['content'])
        return result.get("score", 3), result.get("reason", "Neutral sentiment.")
    except Exception:
        return 3, "AI analysis unavailable."

def process_sentiment_for_ticker(ticker, company_name, max_articles=10):
    """Main entry point for the Sentiment Tab"""
    raw_news = fetch_ticker_news(ticker)

    # Relevance Filter: if the ticker or company is mentioned
    short_name = company_name.split()[0].lower()
    processed_results = []

    for item in raw_news:
        if len(processed_results) >= max_articles:
            break

        title_lower = item['title'].lower()
        if ticker.lower() in title_lower or short_name in title_lower:
            score, reason = analyze_sentiment_local(ticker, company_name, item['title'])

            processed_results.append({
                "title": item['title'],
                "link": item['link'],
                "score": score,
                "reason": reason
            })

    # Calculate aggregate average score
    if not processed_results:
        return 3.0, []

    avg_score = sum(r['score'] for r in processed_results) / len(processed_results)
    return round(avg_score, 2), processed_results
