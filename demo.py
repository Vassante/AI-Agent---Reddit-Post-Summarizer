#!/usr/bin/env python3
"""
Demo script for Reddit Summarizer Agent
Tests the core functionality without the web interface
"""

import sys
from reddit_scraper import RedditWebScraper
from text_summarizer import SimpleSummarizer

def demo_reddit_summarizer():
    """Demonstrate the Reddit summarizer functionality"""
    print("🤖 Reddit Summarizer Agent - Demo")
    print("=" * 50)
    
    # Initialize components
    print("📥 Initializing components...")
    scraper = RedditWebScraper()
    summarizer = SimpleSummarizer()
    
    # Test query
    query = "artificial intelligence"
    subreddit = "technology"
    num_posts = 5
    
    print(f"🔍 Searching for '{query}' in r/{subreddit}...")
    
    try:
        # Search for posts
        posts = scraper.search_posts(query, subreddit=subreddit, limit=num_posts)
        
        if not posts:
            print("❌ No posts found. This might be due to:")
            print("   - Network connectivity issues")
            print("   - Reddit's anti-bot measures")
            print("   - The subreddit not existing")
            return
        
        print(f"✅ Found {len(posts)} posts")
        
        # Display posts
        print("\n📝 Posts found:")
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post['title'][:80]}...")
            print(f"   Subreddit: r/{post['subreddit']}")
            print(f"   Score: {post['score']}")
            print(f"   Comments: {post['num_comments']}")
        
        # Summarize
        print(f"\n📊 Summarizing {len(posts)} posts...")
        summary_data = summarizer.summarize_reddit_posts(posts, query)
        
        # Display summary
        print("\n" + "="*50)
        print("📋 SUMMARY")
        print("="*50)
        print(f"\n🔍 Query: {summary_data['query']}")
        print(f"📊 Total posts analyzed: {summary_data['total_posts']}")
        
        print(f"\n📝 Overall Summary:")
        print(summary_data['summary'])
        
        if summary_data['key_points']:
            print(f"\n🔑 Key Points:")
            for point in summary_data['key_points'][:10]:
                print(f"   • {point}")
        
        print("\n✅ Demo completed successfully!")
        print("💡 To use the full interface, run: python main.py")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("💡 This might be due to network issues or Reddit's anti-bot measures")
        print("   Try running the full app with: python main.py")

if __name__ == "__main__":
    demo_reddit_summarizer()
