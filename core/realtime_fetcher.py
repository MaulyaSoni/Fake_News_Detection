# core/realtime_fetcher.py
import feedparser
from urllib.parse import quote_plus

RSS = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_realtime_articles(text, limit=5):
    try:
        query = quote_plus(text[:120])
        feed = feedparser.parse(RSS.format(query=query))

        articles = []
        for e in feed.entries[:limit]:
            articles.append({
                "title": e.get("title", ""),
                "source": e.get("source", {}).get("title", "Google News"),
                "link": e.get("link", "")
            })

        return articles
    except:
        return []
