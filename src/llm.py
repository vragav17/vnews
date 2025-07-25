import google.generativeai as genai


def configure_gemini(api_key):
    genai.configure(api_key=api_key)


def analyze_new(news_dict):
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    prompt = f"""
You're an AI news analyst. Given a dictionary of news articles categorized under keywords (like Infosys, Trump, etc.), your task is to:

Group similar articles together into event-based clusters under each keyword.

Each event must have:

An AI-generated summary of the event.

A list of related articles (title, publisher, relative publish time, and verified URL).

If articles are outdated or unrelated to a recent event, exclude them.

Return the output in the following JSON :
{{
  "ai_summary_4_the_day": "...",
  "{{keyword}}": [
    {{
      "event_summary": "AI-generated summary of the event.",
      "articles": [
        {{
          "title": "Article title",
          "ai_summary": "AI-generated summary of the article.",
          "publisher": "Publisher name",
          "published": "Relative publish time",
          "article_url": "Verified URL"
        }},
        ...
      ]
    }},
    ...}}

Here are the news articles dictionary:

{news_dict}
"""
    response = model.generate_content(prompt)
    return response.to_dict()
