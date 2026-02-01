import feedparser
from urllib.parse import quote

TRUSTED_DOMAINS = [
    "ndtv.com",
    "indiatoday.in",
    "thehindu.com",
    "timesofindia.indiatimes.com",
    "reuters.com",
    "bbc.com",
    "hindustantimes.com",
    "news18.com"
]

def fetch_evidence(query: str, max_results=6):
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)

    evidence = []

    for entry in feed.entries[:max_results]:
        source = entry.get("source", {}).get("href", "")
        trusted = any(d in source for d in TRUSTED_DOMAINS)

        evidence.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "trusted": trusted
        })

    return evidence
