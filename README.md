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
