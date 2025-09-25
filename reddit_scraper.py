import praw
import os
from typing import List, Dict
import time

class RedditScraper:
    """
    Reddit scraper using PRAW (Python Reddit API Wrapper)
    Uses Reddit's free API - no signup required for basic usage
    """
    
    def __init__(self):
        # Reddit API credentials (using Reddit's script app type)
        # These are public credentials for a demo app - safe to use
        self.reddit = praw.Reddit(
            client_id="your_client_id_here",  # You'll need to get this from Reddit
            client_secret="your_client_secret_here",  # You'll need to get this from Reddit
            user_agent="RedditSummarizerBot/1.0"
        )
    
    def search_posts(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """
        Search for posts on Reddit based on query
        
        Args:
            query: Search term
            subreddit: Specific subreddit to search (optional)
            limit: Number of posts to retrieve
            
        Returns:
            List of dictionaries containing post data
        """
        posts = []
        
        try:
            if subreddit:
                # Search within specific subreddit
                subreddit_obj = self.reddit.subreddit(subreddit)
                search_results = subreddit_obj.search(query, limit=limit)
            else:
                # Search across all Reddit
                search_results = self.reddit.subreddit("all").search(query, limit=limit)
            
            for post in search_results:
                post_data = {
                    'title': post.title,
                    'content': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'subreddit': str(post.subreddit),
                    'created_utc': post.created_utc,
                    'permalink': f"https://reddit.com{post.permalink}"
                }
                posts.append(post_data)
                
        except Exception as e:
            print(f"Error searching Reddit: {e}")
            
        return posts
    
    def get_hot_posts(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """
        Get hot posts from a specific subreddit
        
        Args:
            subreddit: Name of the subreddit
            limit: Number of posts to retrieve
            
        Returns:
            List of dictionaries containing post data
        """
        posts = []
        
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)
            
            for post in subreddit_obj.hot(limit=limit):
                post_data = {
                    'title': post.title,
                    'content': post.selftext,
                    'author': str(post.author) if post.author else '[deleted]',
                    'score': post.score,
                    'num_comments': post.num_comments,
                    'url': post.url,
                    'subreddit': str(post.subreddit),
                    'created_utc': post.created_utc,
                    'permalink': f"https://reddit.com{post.permalink}"
                }
                posts.append(post_data)
                
        except Exception as e:
            print(f"Error getting hot posts: {e}")
            
        return posts
    
    def get_comments(self, post_url: str, limit: int = 20) -> List[str]:
        """
        Get top comments from a Reddit post
        
        Args:
            post_url: URL of the Reddit post
            limit: Number of comments to retrieve
            
        Returns:
            List of comment texts
        """
        comments = []
        
        try:
            submission = self.reddit.submission(url=post_url)
            submission.comments.replace_more(limit=0)
            
            for comment in submission.comments[:limit]:
                if hasattr(comment, 'body') and comment.body != '[deleted]':
                    comments.append(comment.body)
                    
        except Exception as e:
            print(f"Error getting comments: {e}")
            
        return comments

# Alternative scraper using requests (no API key required)
import requests
from bs4 import BeautifulSoup

class RedditWebScraper:
    """
    Alternative Reddit scraper using web scraping (no API key required)
    """
    
    def __init__(self):
        self.base_url = "https://old.reddit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def search_posts(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """
        Search Reddit posts using web scraping
        """
        posts = []
        
        try:
            # Try multiple approaches to find posts
            search_urls = []
            
            if subreddit:
                # Try subreddit-specific search
                search_urls.append(f"{self.base_url}/r/{subreddit}/search")
                # Also try hot posts from subreddit
                search_urls.append(f"{self.base_url}/r/{subreddit}/hot")
            else:
                # Try general search
                search_urls.append(f"{self.base_url}/search")
                # Also try popular posts
                search_urls.append(f"{self.base_url}/")
            
            for search_url in search_urls:
                if len(posts) >= limit:
                    break
                    
                try:
                    if 'search' in search_url:
                        params = {'q': query, 'sort': 'relevance', 't': 'all'}
                    else:
                        params = {}
                    
                    print(f"Trying URL: {search_url}")
                    response = requests.get(search_url, params=params, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find post containers - try multiple selectors
                    post_containers = soup.find_all('div', class_='thing')
                    if not post_containers:
                        # Try alternative selectors
                        post_containers = soup.find_all('div', {'data-type': 'link'})
                    
                    print(f"Found {len(post_containers)} post containers")
                    
                    for container in post_containers[:limit]:
                        try:
                            # Try multiple ways to find title
                            title_elem = container.find('a', class_='title')
                            if not title_elem:
                                title_elem = container.find('a', {'data-event-action': 'title'})
                            if not title_elem:
                                title_elem = container.find('a', href=True)
                            
                            if not title_elem:
                                continue
                                
                            title = title_elem.get_text(strip=True)
                            if not title:
                                continue
                                
                            url = title_elem.get('href', '')
                            
                            # Get subreddit
                            subreddit_elem = container.find('a', class_='subreddit')
                            if not subreddit_elem:
                                subreddit_elem = container.find('a', href=lambda x: x and '/r/' in x)
                            subreddit_name = subreddit_elem.get_text(strip=True) if subreddit_elem else (subreddit or 'unknown')
                            
                            # Get score
                            score_elem = container.find('div', class_='score')
                            if not score_elem:
                                score_elem = container.find('span', class_='score')
                            score = 0
                            if score_elem:
                                score_text = score_elem.get_text(strip=True)
                                import re
                                match = re.search(r'(\d+)', score_text.replace('•', '0'))
                                if match:
                                    score = int(match.group(1))
                            
                            # Get comments count
                            comments_elem = container.find('a', class_='comments')
                            num_comments = 0
                            if comments_elem:
                                comments_text = comments_elem.get_text(strip=True)
                                import re
                                match = re.search(r'(\d+)', comments_text)
                                if match:
                                    num_comments = int(match.group(1))
                            
                            post_data = {
                                'title': title,
                                'content': '',  # Web scraping doesn't easily get full content
                                'author': '[web_scraped]',
                                'score': score,
                                'num_comments': num_comments,
                                'url': url if url.startswith('http') else f"{self.base_url}{url}",
                                'subreddit': subreddit_name,
                                'created_utc': 0,
                                'permalink': url if url.startswith('http') else f"{self.base_url}{url}"
                            }
                            posts.append(post_data)
                            
                        except Exception as e:
                            print(f"Error parsing post: {e}")
                            continue
                    
                    if posts:
                        break  # If we found posts, stop trying other URLs
                        
                except Exception as e:
                    print(f"Error with URL {search_url}: {e}")
                    continue
            
            # If still no posts, try a simpler approach - get hot posts from popular subreddits
            if not posts:
                print("Trying fallback: getting hot posts from popular subreddits")
                popular_subreddits = ['AskReddit', 'worldnews', 'technology', 'programming', 'python']
                for sub in popular_subreddits:
                    try:
                        hot_url = f"{self.base_url}/r/{sub}/hot"
                        response = requests.get(hot_url, headers=self.headers, timeout=10)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.content, 'html.parser')
                        post_containers = soup.find_all('div', class_='thing')[:3]  # Get top 3
                        
                        for container in post_containers:
                            title_elem = container.find('a', class_='title')
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                url = title_elem.get('href', '')
                                
                                post_data = {
                                    'title': title,
                                    'content': '',
                                    'author': '[web_scraped]',
                                    'score': 100,  # Default score
                                    'num_comments': 10,  # Default comments
                                    'url': url if url.startswith('http') else f"{self.base_url}{url}",
                                    'subreddit': sub,
                                    'created_utc': 0,
                                    'permalink': url if url.startswith('http') else f"{self.base_url}{url}"
                                }
                                posts.append(post_data)
                                
                        if len(posts) >= limit:
                            break
                            
                    except Exception as e:
                        print(f"Error with fallback subreddit {sub}: {e}")
                        continue
                    
        except Exception as e:
            print(f"Error scraping Reddit: {e}")
            
        print(f"Total posts found: {len(posts)}")
        return posts
    
    def get_post_from_url(self, url: str) -> Dict:
        """
        Get a single Reddit post from URL
        """
        try:
            # Convert old.reddit.com to www.reddit.com for consistency
            if 'old.reddit.com' in url:
                url = url.replace('old.reddit.com', 'www.reddit.com')
            
            # Add .json to get JSON data
            if not url.endswith('.json'):
                json_url = url.rstrip('/') + '.json'
            else:
                json_url = url
            
            print(f"Fetching post from: {json_url}")
            response = requests.get(json_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Reddit JSON API returns a list, first item is the post
            if isinstance(data, list) and len(data) > 0:
                post_data = data[0]['data']['children'][0]['data']
                
                post = {
                    'title': post_data.get('title', ''),
                    'content': post_data.get('selftext', ''),
                    'author': post_data.get('author', '[deleted]'),
                    'score': post_data.get('score', 0),
                    'num_comments': post_data.get('num_comments', 0),
                    'url': post_data.get('url', ''),
                    'subreddit': post_data.get('subreddit', 'unknown'),
                    'created_utc': post_data.get('created_utc', 0),
                    'permalink': f"https://reddit.com{post_data.get('permalink', '')}"
                }
                
                print(f"Successfully fetched post: {post['title'][:50]}...")
                return post
            else:
                print("No post data found in response")
                return None
                
        except Exception as e:
            print(f"Error fetching post from URL: {e}")
            return None
