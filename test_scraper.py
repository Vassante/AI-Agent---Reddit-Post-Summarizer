#!/usr/bin/env python3
"""
Test script for Reddit scraper
"""

from reddit_scraper import RedditWebScraper

def test_scraper():
    print("🧪 Testing Reddit Web Scraper")
    print("=" * 40)
    
    scraper = RedditWebScraper()
    
    # Test 1: Search for posts
    print("\n🔍 Test 1: Searching for 'python' posts")
    posts = scraper.search_posts("python", limit=5)
    print(f"Found {len(posts)} posts")
    
    for i, post in enumerate(posts, 1):
        print(f"{i}. {post['title'][:60]}...")
        print(f"   Subreddit: r/{post['subreddit']}")
        print(f"   Score: {post['score']}")
    
    # Test 2: Get hot posts from a specific subreddit
    print("\n🔥 Test 2: Getting hot posts from r/technology")
    hot_posts = scraper.get_hot_posts("technology", limit=3)
    print(f"Found {len(hot_posts)} hot posts")
    
    for i, post in enumerate(hot_posts, 1):
        print(f"{i}. {post['title'][:60]}...")
        print(f"   Score: {post['score']}")
    
    if not posts and not hot_posts:
        print("\n❌ No posts found. This could be due to:")
        print("   - Network connectivity issues")
        print("   - Reddit blocking the requests")
        print("   - Changes in Reddit's HTML structure")
        print("\n💡 Try running the demo script: python demo.py")
    else:
        print("\n✅ Scraper is working!")

if __name__ == "__main__":
    test_scraper()
