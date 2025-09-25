#!/usr/bin/env python3
"""
Alternative Reddit scraper using different approaches
"""

import requests
import json
from typing import List, Dict
import time

class RedditJSONScraper:
    """
    Scraper that uses Reddit's JSON API endpoints
    """
    
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_posts(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """
        Search posts using Reddit's JSON API
        """
        posts = []
        
        try:
            if subreddit:
                # Search within specific subreddit
                url = f"{self.base_url}/r/{subreddit}/search.json"
                params = {'q': query, 'sort': 'relevance', 'limit': limit}
            else:
                # Search across all Reddit
                url = f"{self.base_url}/search.json"
                params = {'q': query, 'sort': 'relevance', 'limit': limit}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'children' in data['data']:
                for child in data['data']['children']:
                    post_data = child['data']
                    
                    post = {
                        'title': post_data.get('title', ''),
                        'content': post_data.get('selftext', ''),
                        'author': post_data.get('author', '[deleted]'),
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'url': post_data.get('url', ''),
                        'subreddit': post_data.get('subreddit', 'unknown'),
                        'created_utc': post_data.get('created_utc', 0),
                        'permalink': f"{self.base_url}{post_data.get('permalink', '')}"
                    }
                    posts.append(post)
            
        except Exception as e:
            print(f"Error with JSON API: {e}")
        
        return posts
    
    def get_hot_posts(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """
        Get hot posts from a subreddit using JSON API
        """
        posts = []
        
        try:
            url = f"{self.base_url}/r/{subreddit}/hot.json"
            params = {'limit': limit}
            
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and 'children' in data['data']:
                for child in data['data']['children']:
                    post_data = child['data']
                    
                    post = {
                        'title': post_data.get('title', ''),
                        'content': post_data.get('selftext', ''),
                        'author': post_data.get('author', '[deleted]'),
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'url': post_data.get('url', ''),
                        'subreddit': post_data.get('subreddit', 'unknown'),
                        'created_utc': post_data.get('created_utc', 0),
                        'permalink': f"{self.base_url}{post_data.get('permalink', '')}"
                    }
                    posts.append(post)
            
        except Exception as e:
            print(f"Error getting hot posts: {e}")
        
        return posts

class MockRedditScraper:
    """
    Mock scraper that returns sample data for testing
    """
    
    def __init__(self):
        self.sample_posts = [
            {
                'title': 'What are the best programming languages to learn in 2024?',
                'content': 'I want to start learning programming and wondering what languages are most in demand.',
                'author': 'programmer123',
                'score': 1250,
                'num_comments': 89,
                'url': 'https://reddit.com/r/programming/comments/example1',
                'subreddit': 'programming',
                'created_utc': 1640995200,
                'permalink': 'https://reddit.com/r/programming/comments/example1'
            },
            {
                'title': 'AI and Machine Learning trends for 2024',
                'content': 'Discussion about the latest developments in AI and ML.',
                'author': 'ai_enthusiast',
                'score': 890,
                'num_comments': 45,
                'url': 'https://reddit.com/r/MachineLearning/comments/example2',
                'subreddit': 'MachineLearning',
                'created_utc': 1640995200,
                'permalink': 'https://reddit.com/r/MachineLearning/comments/example2'
            },
            {
                'title': 'Python vs JavaScript: Which should I learn first?',
                'content': 'Beginner asking for advice on choosing between Python and JavaScript.',
                'author': 'newbie_dev',
                'score': 567,
                'num_comments': 32,
                'url': 'https://reddit.com/r/learnprogramming/comments/example3',
                'subreddit': 'learnprogramming',
                'created_utc': 1640995200,
                'permalink': 'https://reddit.com/r/learnprogramming/comments/example3'
            }
        ]
    
    def search_posts(self, query: str, subreddit: str = None, limit: int = 10) -> List[Dict]:
        """
        Return sample posts based on query
        """
        # Filter posts based on query keywords
        filtered_posts = []
        query_lower = query.lower()
        
        for post in self.sample_posts:
            if any(keyword in post['title'].lower() or keyword in post['content'].lower() 
                   for keyword in query_lower.split()):
                filtered_posts.append(post)
        
        # If no matches, return all posts
        if not filtered_posts:
            filtered_posts = self.sample_posts
        
        return filtered_posts[:limit]
    
    def get_hot_posts(self, subreddit: str, limit: int = 10) -> List[Dict]:
        """
        Return sample hot posts
        """
        return self.sample_posts[:limit]
