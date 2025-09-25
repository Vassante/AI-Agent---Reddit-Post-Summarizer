import streamlit as st
import time
from typing import List, Dict
import json

# Import our custom modules
from reddit_scraper import RedditScraper, RedditWebScraper
from alternative_scraper import RedditJSONScraper, MockRedditScraper
from text_summarizer import TextSummarizer, SimpleSummarizer

# Page configuration
st.set_page_config(
    page_title="Reddit Summarizer Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #FF4500;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #FF4500;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #1f77b4;
    }
    .bot-message {
        background-color: #fff5f5;
        border-left-color: #FF4500;
    }
    .summary-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .key-points {
        background-color: #e8f4fd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .post-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with error handling
try:
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'scraper_type' not in st.session_state:
        st.session_state.scraper_type = 'web'  # Default to web scraper (no API key needed)
    if 'max_words' not in st.session_state:
        st.session_state.max_words = None
    if 'max_paragraphs' not in st.session_state:
        st.session_state.max_paragraphs = None
except Exception as e:
    st.error(f"Error initializing session state: {e}")
    # Force reinitialize
    st.session_state.messages = []
    st.session_state.scraper_type = 'web'
    st.session_state.max_words = None
    st.session_state.max_paragraphs = None

def display_chat_message(message: str, is_user: bool = False):
    """Display a chat message with appropriate styling"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>Reddit Agent:</strong> {message}
        </div>
        """, unsafe_allow_html=True)

def display_summary(summary_data: Dict):
    """Display the summary in a formatted way"""
    st.markdown("### 📊 Summary")
    
    # Show length info if available
    if 'summary_length' in summary_data:
        words = summary_data['summary_length']['words']
        paragraphs = summary_data['summary_length']['paragraphs']
        st.info(f"📏 Summary length: {words} words, {paragraphs} paragraph{'s' if paragraphs > 1 else ''}")
    
    # Overall summary
    st.markdown(f"""
    <div class="summary-box">
        <h4>Overall Summary</h4>
        <p>{summary_data['summary']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key points
    if summary_data['key_points']:
        st.markdown("### 🔑 Key Points")
        key_points_html = ""
        for point in summary_data['key_points'][:10]:  # Show top 10
            key_points_html += f'<span class="key-points">{point}</span> '
        st.markdown(key_points_html, unsafe_allow_html=True)
    
    # Individual post summaries
    if summary_data.get('post_summaries'):
        st.markdown("### 📝 Individual Post Summaries")
        for post in summary_data['post_summaries'][:5]:  # Show top 5
            st.markdown(f"""
            <div class="post-card">
                <h5>{post['title']}</h5>
                <p><strong>Subreddit:</strong> r/{post['subreddit']} | 
                   <strong>Score:</strong> {post['score']} | 
                   <strong>Summary:</strong> {post['summary']}</p>
                <a href="{post['url']}" target="_blank">View Original Post</a>
            </div>
            """, unsafe_allow_html=True)

def process_user_query(query: str, subreddit: str = None, num_posts: int = 10, max_words: int = None, max_paragraphs: int = None, manual_url: str = None) -> Dict:
    """Process user query and return summary"""
    try:
        # Initialize scraper with fallbacks
        scraper = None
        scraper_name = ""
        
        if st.session_state.scraper_type == 'api':
            try:
                scraper = RedditScraper()
                scraper_name = "Reddit API"
            except:
                pass
        
        if not scraper:
            try:
                scraper = RedditJSONScraper()
                scraper_name = "Reddit JSON API"
            except:
                pass
        
        if not scraper:
            try:
                scraper = RedditWebScraper()
                scraper_name = "Web Scraper"
            except:
                pass
        
        if not scraper:
            scraper = MockRedditScraper()
            scraper_name = "Mock Scraper (Demo Mode)"
        
        st.write(f"Using: {scraper_name}")
        
        # Initialize summarizer
        try:
            summarizer = TextSummarizer()
        except:
            summarizer = SimpleSummarizer()
        
        # Search for posts or get from manual URL
        if manual_url:
            with st.spinner("🔍 Fetching Reddit post..."):
                post = scraper.get_post_from_url(manual_url)
                if post:
                    posts = [post]
                else:
                    posts = []
        else:
            with st.spinner("🔍 Searching Reddit..."):
                if subreddit:
                    posts = scraper.search_posts(query, subreddit=subreddit, limit=num_posts)
                else:
                    posts = scraper.search_posts(query, limit=num_posts)
            
        
        if not posts:
            if manual_url:
                error_msg = f"Sorry, I couldn't fetch the Reddit post from the provided URL. Please check if the URL is correct and the post is accessible."
            else:
                error_msg = f"Sorry, I couldn't find any posts related to '{query}'. Try a different search term or check if the subreddit exists."
            
            return {
                'summary': error_msg,
                'key_points': [],
                'total_posts': 0,
                'query': query
            }
        
        # Summarize posts
        with st.spinner("📝 Summarizing content..."):
            summary_data = summarizer.summarize_reddit_posts(posts, query, max_words, max_paragraphs)
        
        return summary_data
        
    except Exception as e:
        return {
            'summary': f"An error occurred while processing your request: {str(e)}",
            'key_points': [],
            'total_posts': 0,
            'query': query
        }

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Reddit Summarizer Agent</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Scraper type selection
        scraper_type = st.selectbox(
            "Choose scraper type:",
            ["web", "api"],
            index=0 if st.session_state.scraper_type == 'web' else 1,
            help="Web scraper doesn't require API keys, API scraper requires Reddit API credentials"
        )
        st.session_state.scraper_type = scraper_type
        
        # Number of posts
        num_posts = st.slider("Number of posts to analyze:", 5, 25, 10)
        
        # Data source selection
        data_source = st.radio(
            "Choose data source:",
            ["Search Reddit", "Manual Reddit URL"],
            help="Search Reddit or analyze a specific Reddit post"
        )
        
        subreddit = None
        manual_url = None
        
        if data_source == "Search Reddit":
            # Subreddit filter
            subreddit = st.text_input(
                "Specific subreddit (optional):",
                placeholder="e.g., python, MachineLearning, AskReddit",
                help="Leave empty to search all of Reddit"
            )
        else:
            # Manual URL input
            manual_url = st.text_input(
                "Reddit post URL:",
                placeholder="https://reddit.com/r/subreddit/comments/...",
                help="Paste the full URL of a Reddit post to analyze"
            )
            
            if manual_url:
                # Validate URL
                if not (manual_url.startswith('http') and 'reddit.com' in manual_url):
                    st.error("Please enter a valid Reddit URL (e.g., https://reddit.com/r/subreddit/comments/...)")
                    manual_url = None
        
        st.markdown("---")
        st.markdown("### 📏 Summary Length")
        
        # Summary length options with safer implementation
        try:
            length_option = st.radio(
                "Choose summary length control:",
                ["Automatic (default)", "Word limit", "Paragraph limit"],
                help="Control how long the summary should be"
            )
            
            # Reset length parameters when switching options
            if length_option == "Automatic (default)":
                st.session_state.max_words = None
                st.session_state.max_paragraphs = None
            elif length_option == "Word limit":
                st.session_state.max_paragraphs = None
                # Use a simpler approach for the slider
                word_limit = st.slider(
                    "Maximum words in summary:",
                    min_value=50,
                    max_value=1000,
                    value=200,
                    step=25,
                    help="Limit the summary to a specific number of words"
                )
                st.session_state.max_words = word_limit
            elif length_option == "Paragraph limit":
                st.session_state.max_words = None
                # Use a simpler approach for the slider
                paragraph_limit = st.slider(
                    "Maximum paragraphs in summary:",
                    min_value=1,
                    max_value=10,
                    value=3,
                    step=1,
                    help="Limit the summary to a specific number of paragraphs"
                )
                st.session_state.max_paragraphs = paragraph_limit
                
        except Exception as e:
            st.error(f"Error with length control: {e}")
            # Fallback to automatic
            st.session_state.max_words = None
            st.session_state.max_paragraphs = None
        
        # Show current settings
        st.markdown("**Current Settings:**")
        if st.session_state.max_words:
            st.write(f"📏 Word limit: {st.session_state.max_words}")
        elif st.session_state.max_paragraphs:
            st.write(f"📏 Paragraph limit: {st.session_state.max_paragraphs}")
        else:
            st.write("📏 Length: Automatic")
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Ask a question** in the chat below
        2. **Specify a subreddit** (optional) in the sidebar
        3. **Wait for the agent** to search and summarize
        4. **Review the results** and ask follow-up questions
        
        **Example questions:**
        - "What are people saying about AI?"
        - "Latest trends in machine learning"
        - "Best programming languages 2024"
        """)
        
        st.markdown("---")
        st.markdown("### ⚠️ Important Notes")
        st.markdown("""
        - **Web scraper** works without API keys but may be slower
        - **API scraper** requires Reddit API credentials (see README)
        - Rate limiting may apply for extensive searches
        - Some posts may not be accessible due to privacy settings
        """)
    
    # Main chat interface
    st.markdown("### 💬 Chat with Reddit Agent")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(message['content'], message['is_user'])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about Reddit! (e.g., 'What are people saying about AI?')")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({'content': user_input, 'is_user': True})
        display_chat_message(user_input, True)
        
        # Process the query with error handling
        try:
            max_words = st.session_state.get('max_words', None)
            max_paragraphs = st.session_state.get('max_paragraphs', None)
            
            with st.spinner("🤖 Processing your request..."):
                summary_data = process_user_query(
                    user_input, 
                    subreddit, 
                    num_posts, 
                    max_words, 
                    max_paragraphs,
                    manual_url
                )
        except Exception as e:
            st.error(f"Error processing query: {e}")
            summary_data = {
                'summary': f"Sorry, an error occurred while processing your request: {str(e)}",
                'key_points': [],
                'total_posts': 0,
                'query': user_input
            }
        
        # Add bot response to chat with length info
        length_info = ""
        if 'summary_length' in summary_data:
            words = summary_data['summary_length']['words']
            paragraphs = summary_data['summary_length']['paragraphs']
            length_info = f" (Summary: {words} words, {paragraphs} paragraph{'s' if paragraphs > 1 else ''})"
        
        if manual_url:
            bot_response = f"I analyzed the Reddit post from the provided URL. Here's what I discovered:{length_info}"
        else:
            bot_response = f"I found {summary_data['total_posts']} posts related to '{user_input}'. Here's what I discovered:{length_info}"
        st.session_state.messages.append({'content': bot_response, 'is_user': False})
        display_chat_message(bot_response, False)
        
        # Display detailed summary
        display_summary(summary_data)
        
        # Store summary data in session state for potential follow-up questions
        st.session_state.last_summary = summary_data
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>🤖 Reddit Summarizer Agent | Built with Streamlit | Free to use</p>
        <p>⚠️ Please respect Reddit's terms of service and rate limits</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
