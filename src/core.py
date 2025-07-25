from googlenewsdecoder import gnewsdecoder
import feedparser
import pytz
from dateutil import parser as date_parser


# Decode redirected Google News link
def decode_gnewsurl(url):
    try:
        decoded = gnewsdecoder(url, interval=1)  # interval adds a delay, good practice
        return decoded.get("decoded_url", url)
    except Exception:
        return url


def fetch_articles(keyword, selected_domains, max_results=5, trusted_only=False):
    query = keyword.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)

    ist = pytz.timezone("Asia/Kolkata")
    articles = []

    for entry in feed.entries:
        if len(articles) >= max_results:
            break

        raw_link = (
            entry.links[0].href if "links" in entry and entry.links else entry.link
        )
        resolved_url = decode_gnewsurl(raw_link)

        try:
            published_utc = date_parser.parse(entry.published)
            published_str = published_utc.astimezone(ist).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            published_str = entry.published

        articles.append(
            {"title": entry.title, "link": resolved_url, "published": published_str}
        )

    return articles
