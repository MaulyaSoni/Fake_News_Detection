import feedparser
from urllib.parse import quote_plus

GOOGLE_RSS = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_realtime_articles(text: str, limit=5):
    try:
        query = quote_plus(text[:120])
        url = GOOGLE_RSS.format(query=query)
        feed = feedparser.parse(url)

        articles = []
        for e in feed.entries[:limit]:
            articles.append({
                "title": e.get("title", ""),
                "source": "Google News"
            })

        return articles
    except:
        return ["No verified sources found"]
