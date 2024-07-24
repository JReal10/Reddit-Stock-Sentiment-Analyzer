import praw
import pandas as pd
#import sqlite3
from datetime import datetime
# Bring your packages onto the path

# scripts/reddit_scraper.py
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from config import config

def connect_to_reddit():
    """Establish connection to Reddit API"""
    return praw.Reddit(
        client_id=config.CLIENT_ID,
        client_secret=config.SECRET_KEY,
        user_agent=config.USER_NAME
    )
def scrape_subreddit(reddit, subreddit_name, post_limit=100):
    """Scrape posts and comments from a subreddit"""
    subreddit = reddit.subreddit(subreddit_name)
    data = []

    for post in subreddit.search('daily discussion', sort='new', time_filter='day'):
        if post.num_comments > 0:
            # Scraping comments for each post
            post.comments.replace_more(limit= 5)                    
            for comment in post.comments.list():
                data.append({
                    'id': comment.id,
                    'author': comment.author.name if comment.author else '[deleted]',
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': datetime.fromtimestamp(comment.created_utc),
                    'subreddit': subreddit_name,
                    'post_id': post.id,
                    'post_title': post.title
                })
    
    return pd.DataFrame(data)

#def save_to_database(df, db_path='data/reddit_data.db'):
    """Save scraped data to SQLite database"""
    conn = sqlite3.connect(db_path)
    df.to_sql('reddit_comments', conn, if_exists='append', index=False)
    conn.close()

def main():
    reddit = connect_to_reddit()
    subreddits = ['stocks', 'wallstreetbets']  # Add more subreddits as needed

    for subreddit in subreddits:
        print(f"Scraping r/{subreddit}...")
        df = scrape_subreddit(reddit, subreddit)
        #save_to_database(df)
        print(f"Saved {len(df)} comments from r/{subreddit}")

if __name__ == "__main__":
    main()