import feedparser
from urllib.parse import quote

TRUSTED_DOMAINS = [
    "ndtv.com",
    "indiatoday.in",
    "thehindu.com",
    "timesofindia.indiatimes.com",
    "reuters.com",
    "bbc.com"
]

def fetch_evidence(query: str, max_results=5):
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)

    evidence = []

    for entry in feed.entries[:max_results]:
        source = entry.get("source", {}).get("href", "")
        domain_ok = any(d in source for d in TRUSTED_DOMAINS)

        evidence.append({
            "title": entry.title,
            "link": entry.link,
            "trusted": domain_ok
        })

    return evidence
