"""
Configuration file for Reddit Summarizer Agent
"""

# Reddit API Configuration (Optional)
# Get these from https://www.reddit.com/prefs/apps
REDDIT_CONFIG = {
    'client_id': 'your_client_id_here',
    'client_secret': 'your_client_secret_here',
    'user_agent': 'RedditSummarizerBot/1.0'
}

# Application Settings
APP_CONFIG = {
    'default_num_posts': 10,
    'max_num_posts': 25,
    'min_num_posts': 5,
    'default_summary_sentences': 3,
    'max_summary_sentences': 10,
    'request_timeout': 30,
    'rate_limit_delay': 1,  # seconds between requests
}

# Scraper Settings
SCRAPER_CONFIG = {
    'default_scraper': 'web',  # 'web' or 'api'
    'fallback_scraper': 'web',
    'retry_attempts': 3,
    'retry_delay': 2,
}

# UI Settings
UI_CONFIG = {
    'page_title': 'Reddit Summarizer Agent',
    'page_icon': '🤖',
    'layout': 'wide',
    'theme': {
        'primary_color': '#FF4500',  # Reddit orange
        'background_color': '#ffffff',
        'secondary_background_color': '#f0f2f6',
        'text_color': '#262730',
    }
}

# Error Messages
ERROR_MESSAGES = {
    'no_posts_found': "Sorry, I couldn't find any posts related to your query. Try a different search term or check if the subreddit exists.",
    'scraper_error': "An error occurred while scraping Reddit. Please try again or check your internet connection.",
    'summarization_error': "An error occurred while summarizing the content. Please try again.",
    'api_error': "Reddit API error. Please check your API credentials or try using the web scraper instead.",
    'network_error': "Network error. Please check your internet connection and try again.",
    'rate_limit_error': "Rate limit exceeded. Please wait a moment before trying again.",
}

# Success Messages
SUCCESS_MESSAGES = {
    'posts_found': "Found {count} posts related to your query. Analyzing and summarizing...",
    'summary_complete': "Summary complete! Here's what I found:",
    'scraper_ready': "Reddit scraper is ready to use.",
}

# Default Subreddits for suggestions
POPULAR_SUBREDDITS = [
    'AskReddit',
    'worldnews',
    'technology',
    'programming',
    'MachineLearning',
    'python',
    'javascript',
    'webdev',
    'datascience',
    'artificial',
    'futurology',
    'science',
    'explainlikeimfive',
    'todayilearned',
    'mildlyinteresting'
]
