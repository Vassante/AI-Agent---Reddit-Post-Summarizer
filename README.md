# AI-Agent---Reddit-Content-Summarizer
A **Streamlit-powered AI agent** that scrapes Reddit posts and generates intelligent summaries.
Built with **Cursor AI**, this agent lets you:
* Search Reddit or analyze a specific Reddit post via URL
* Summarize discussions with word limit or paragraph limit controls
* Choose between API scraper (requires Reddit API keys) or web scraping (no keys required)
* Chat-style interface to ask questions about trending topics

## Tech Stack:
* Streamlit – Interactive web UI
* PRAW – Reddit API wrapper
* Requests – HTTP requests
* BeautifulSoup4 – HTML parsing
* NLTK – Natural language processing
* python-dotenv – Manage API keys securely

## Features:
* **Multiple Scraper Options:**
  * Reddit API Scraper (requires credentials)
  * Reddit JSON Scraper fallback
  * Web Scraper (no API key needed)
  * Mock Scraper for demo mode
* **Flexible Summarization:**
  * Automatic summaries
  * User-controlled word limits
  * User-controlled paragraph limits
* **Interactive UI:**
  * Streamlit chat interface
  * Sidebar configuration for scraper type, subreddit, post limits, and summary length
  * Clean and responsive design
* **Manual URL Support:**
  * Analyze any Reddit post by pasting its URL

## How to use the app:
* Run the main app: *python main.py*
* The app will start at *http://localhost:8501*

## Installation Required:
1. Clone Repository:
   git clone https://github.com/your-username/reddit-summarizer-agent.git
   cd reddit-summarizer-agent
2. Create Virtual Environment:
   python3 -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
3. Install Dependencies:
   pip install -r requirements.txt
4. (Optional) Configure Reddit API Keys
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_SECRET=your_client_secret
   REDDIT_USER_AGENT=your_user_agent 

## Notes:
* Web scraper works without API keys but may be slower
* API scraper requires Reddit API credentials
* Respect Reddit’s rate limits and terms of service
* Some posts may not be accessible due to privacy or moderation settings
