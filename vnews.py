import time, json
from datetime import datetime

import streamlit as st

from src.llm import configure_gemini, analyze_new
import constants as const
from src.core import fetch_articles


# Access API key from Streamlit secrets
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("secrets missing")
    # st.stop()


# 🖥️ Streamlit UI Setup
st.set_page_config(page_title="Daily News Digest - Money Pechu", page_icon="📰")

# Custom CSS for better aesthetics - Defined once at the start


st.title("📰 Daily News Digest  ")
st.markdown(const.CSS, unsafe_allow_html=True)
st.markdown(
    "made with ❤️ for Anand Sir & Money Pechu Team, by [@vragav17](https://www.linkedin.com/in/vragav17/)"
)

# User Inputs for News Fetching
st.sidebar.header("Configuration")
selected_keywords = st.sidebar.multiselect(
    "Select Keywords:",
    const.DEFAULT_KEYWORDS,
    default=["Jerome Powell", "Trump", "RBI"],
)
custom_keyword_input = st.sidebar.text_input(
    "Or add custom keyword(s) (comma-separated):", ""
)

# trusted_only = st.sidebar.toggle("Trusted Sites Only", value=True, help="Enable to fetch articles only from trusted news sources. Disable for open search across all Google News results.")

selected_domains_for_filter = []  # Initialize list to be populated based on toggle

max_results = st.sidebar.slider("Max articles per keyword", 1, 7, 3)

# Fetch news button
if st.sidebar.button("🚀 Fetch & Analyze News"):
    all_keywords = selected_keywords + [
        kw.strip() for kw in custom_keyword_input.split(",") if kw.strip()
    ]

    if len(all_keywords) > 10:
        st.error("Please limit the number of keywords to 10 or fewer.")
        st.stop()
    # Dictionary to hold raw fetched articles for AI analysis
    raw_fetched_articles = {}

    fetch_analystics_placeholder = st.empty()  # Placeholder for progress updates
    with fetch_analystics_placeholder:
        # --- Step 1: Fetch raw articles for each keyword ---
        st.markdown("## Fetching Articles...")
        progress_bar = st.progress(0)
        for idx, kw in enumerate(all_keywords):
            st.info(f" 🔍 Fetching news for '{kw}'...")
            articles = fetch_articles(kw, selected_domains_for_filter, max_results)
            if not articles:
                st.warning(f"No articles found for '{kw}' with current filters.")
            else:
                raw_fetched_articles[kw] = articles
            time.sleep(0.5)  # Small delay to be polite to APIs and show progress
            progress_bar.progress((idx + 1) / len(all_keywords))

        if not raw_fetched_articles:
            st.error(
                "No articles were fetched for any selected keywords. Please check your keywords and filters."
            )
            st.stop()  # Stop execution if no articles to analyze

        # --- Step 2: Perform AI Analysis on collected articles ---
        st.markdown("## Analyzing Articles with AI...")
        with st.spinner(" 🔍 Analyzing Articles with AI... "):
            configure_gemini(GEMINI_API_KEY)  # Ensure Gemini model is configured
            try:
                ai_raw_response = analyze_new(raw_fetched_articles)

            except Exception as e:
                if "429" in str(e):
                    st.error("Rate limit exceeded. Please try again later.")
                st.error(f"Error during AI analysis: {e}")
                st.stop()

            # Extract and parse JSON string from the AI response
            import re

            try:
                raw_text = ai_raw_response["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                json_match = re.search(r"```json\n(.*?)```", raw_text, re.DOTALL)
                if json_match:
                    news_data = json.loads(json_match.group(1))
                else:
                    st.error(
                        "AI response did not contain a valid JSON block. Displaying raw AI response for debugging."
                    )
                    st.json(ai_raw_response)  # Use st.json for raw response debugging
                    st.stop()
            except (KeyError, IndexError, AttributeError, json.JSONDecodeError) as e:
                st.error(
                    f"Error parsing AI response: {e}. Raw AI response for debugging:"
                )
                st.json(
                    ai_raw_response
                )  # Display full raw response for easier debugging
                st.stop()
        fetch_analystics_placeholder.empty()

        # Clear the placeholder after fetching and analyzing

    # --- Step 3: Display AI-summarized and grouped news using the predefined UI style ---

    # Overall AI Summary for the Day
    st.subheader("Today's AI Summary")
    # Check if 'ai_summary_4_the_day' exists to avoid KeyError if LLM output varies
    if "ai_summary_4_the_day" in news_data:
        st.markdown(
            f'<div class="event-summary-text">{news_data["ai_summary_4_the_day"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning("Overall AI summary not available in the AI's response.")

    # Create tabs for each event group
    # Exclude 'ai_summary_4_the_day' from tab creation as it's the global summary
    tab_titles = [
        key.replace("_", " ").title()
        for key in news_data
        if key != "ai_summary_4_the_day"
    ]

    # Handle case where no categories are returned by the LLM
    if not tab_titles:
        st.info("No categorized news summaries were generated by the AI.")
    else:
        tabs = st.tabs(tab_titles)

        for i, category_name_raw in enumerate(
            [key for key in news_data if key != "ai_summary_4_the_day"]
        ):
            with tabs[i]:
                # Ensure category_name_raw exists and is a list of events
                category_events = news_data.get(category_name_raw, [])
                if not isinstance(category_events, list):
                    st.error(
                        f"Expected a list of events for category '{category_name_raw}', but got {type(category_events)}"
                    )
                    continue

                st.markdown(
                    f'<p class="section-header">{category_name_raw.replace("_", " ").title()}</p>',
                    unsafe_allow_html=True,
                )

                if not category_events:
                    st.info(
                        f"No specific events summarized for {category_name_raw.replace('_', ' ').title()}."
                    )

                for event in category_events:
                    # Check for 'event_summary' and 'articles' keys
                    if "event_summary" in event:
                        st.markdown(
                            f'<div class="event-summary-text">{event["event_summary"]}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.warning(
                            f"Event summary missing for an event in {category_name_raw.replace('_', ' ').title()}."
                        )

                    st.subheader("Related Articles:")

                    articles_list = event.get("articles", [])
                    if not articles_list:
                        st.info("No related articles found for this event.")
                    else:
                        for article in articles_list:
                            # Format the timestamp for better display
                            try:
                                published_dt = datetime.fromisoformat(
                                    article.get("published", "")
                                )
                                formatted_time = published_dt.strftime(
                                    "%B %d, %Y, %I:%M %p"
                                )
                            except (ValueError, TypeError):
                                formatted_time = article.get(
                                    "published", "Date N/A"
                                )  # Fallback if format is unexpected or missing

                            article_url = article.get("article_url", "#")
                            st.markdown(
                                f"""<div class="article-card"> 
                                        <p class="article-title"> {article.get("title", "No Title")}</p>
                                        <p class="article-snippet">{article.get("ai_summary", "No AI Summary available.")}</p>
                                        <p class="article-meta">Publisher: {article.get("publisher", "Unknown")} | Published: {formatted_time}</p>
                                        <a href="{article_url}" target="_blank" class="read-more-link">Read full article</a>
                                        </div>""",
                                unsafe_allow_html=True,
                            )

                            st.markdown(f"</div>", unsafe_allow_html=True)
                        st.markdown("---")

    # Download button for the full AI analysis
    st.markdown("### Download Full AI Analysis")
    if news_data:
        # Convert news_data to JSON string for download
        st.markdown("You can download the full AI analysis in JSON format:")
        st.download_button(
            label="Download Full AI Analysis",
            data=json.dumps(news_data, indent=2),
            file_name=f"news_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            help="Download the full AI analysis in JSON format.",
        )
else:
    st.info(
        """
Use the sidebar to configure your news preferences and fetch the latest articles.\n
You can select keywords, add custom keywords, and choose number of articles per keyword.\n
Click the '🚀 Fetch & Analyze News' button to get started
"""
    )
