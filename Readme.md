# Daily News Scraper & AI Digest

This project is a Streamlit-based application that fetches, analyzes, and summarizes the latest financial and business news using Google News RSS feeds and Gemini AI. It provides an interactive dashboard for users to select keywords, view AI-generated summaries, and download the full analysis.

## Features

- Fetches news articles from Google News and other financial sources.
- Uses Gemini AI to summarize and group news by events and topics.
- Interactive Streamlit UI with keyword selection and custom configuration.
- Downloadable JSON report of the full AI analysis.
- Custom CSS for a clean, readable dashboard.

## Project Structure

```
.gitignore
.pre-commit-config.yaml
constants.py
Readme.md
requirements.txt
vnews.py
__pycache__/
.streamlit/
.trails/
src/
```

- **vnews.py**: Main Streamlit app for news scraping and display.
- **src/**: Core modules for LLM integration, utilities, and article fetching.
- **.trails/**: Contains test scripts, sample data, and intermediate results.
- **.streamlit/secrets.toml**: Stores API keys for Gemini AI.
- **requirements.txt**: Python dependencies.
- **constants.py**: UI constants and default keywords/sites.

## Setup

1. **Clone the repository**  
   ```sh
   git clone <repo-url>
   cd news_scraper
   ```

2. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```

3. **Add Gemini API Key**  
   Create `.streamlit/secrets.toml` and add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "<your-gemini-api-key>"
   ```

4. **Run the app**  
   ```sh
   streamlit run vnews.py
   ```

## Usage

- Use the sidebar to select keywords and configure preferences.
- Click "Fetch & Analyze News" to get the latest articles and AI summaries.
- Download the full analysis as a JSON file.

## Development

- Code formatting is enforced via [Black](https://github.com/psf/black) (see [.pre-commit-config.yaml](.pre-commit-config.yaml)).
- Ignore virtual environments, cache, and config files via [.gitignore](.gitignore).

## License

MIT License

---


Made with ❤️ for Anand Sir & Money Pechu Team, by [@vragav17](https://www.linkedin.com/in/vragav17/)