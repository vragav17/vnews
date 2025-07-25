# 🔒 Full list of trusted domains (India + US)
ALL_TRUSTED_DOMAINS = [
    # 🇮🇳 Indian sources
    "moneycontrol.com",
    "livemint.com",
    "economictimes.indiatimes.com",
    "business-standard.com",
    "ndtv.com",
    "reuters.com",
    "cnbctv18.com",
    "financialexpress.com",
    "themorningcontext.com",
    # 🇺🇸 US business sources
    "bloomberg.com",
    "ft.com",
    "wsj.com",
    "cnbc.com",
    "fortune.com",
    "forbes.com",
    "businessinsider.com",
    "marketwatch.com",
    "investopedia.com",
    "nasdaq.com",
    "seekingalpha.com",
    "themotleyfool.com",
    "axios.com",
]

# Default keywords for selection
DEFAULT_KEYWORDS = [
    "Jerome Powell",
    "Trump",
    "RBI",
    "SEBI",
    "Infosys",
    "HDFC Bank",
    "IRFC",
    "Reliance",
    "TCS",
    "Adani Group",
    "Nifty",
    "Sensex",
    "Apple",
    "Tesla",
    "Microsoft",
    "US Economy",
    "Oil Prices",
]

DEFAULT_SITES = [
    "moneycontrol.com",
    "livemint.com",
    "economictimes.indiatimes.com",
    "business-standard.com",
    "financialexpress.com",
    "themorningcontext.com",
    "bloomberg.com",
    "wsj.com",
]

CSS = """
    <style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    
    .main-header {
        font-size: 3em;
        font-weight: bold;
        color: #1a1a1a;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 2em;
        font-weight: bold;
        color: #333333;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .event-summary-text {
        font-size: 1.1em;
        line-height: 1.6;
        color: #555555;
        background-color: #ffffff;
        padding: 15px;
        border-left: 5px solid #4CAF50; /* Green border for event summaries */
        border-radius: 5px;
        margin-bottom: 1.5rem;
    }
    .article-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border: 1px solid #e0e0e0;
    }
    .article-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #1e88e5; /* Blue for titles */
        margin-bottom: 0.5rem;
    }
    .article-meta {
        font-size: 0.9em;
        color: #777777;
        margin-bottom: 0.5rem;
    }
    /* Note: 'snippet' is not in the current AI output structure, so this might not be used */
    .article-snippet {
        font-size: 1em;
        color: #333333;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .read-more-link {
        color: #007bff;
        text-decoration: none;
        font-weight: bold;
    }
    .read-more-link:hover {
        text-decoration: underline;
    }
    </style>
    """
