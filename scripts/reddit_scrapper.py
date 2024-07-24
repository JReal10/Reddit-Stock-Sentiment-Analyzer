import praw
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

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
    
def connect_to_db():
    """Establish connection to PostgreSQL database"""
    return psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
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
                    'id': post.id + '_' +  comment.id ,
                    'created_utc': datetime.fromtimestamp(comment.created_utc),
                    'body': comment.body,
                    'Score': comment.score,
                    'Post_url':post.url,
                })
    
    return pd.DataFrame(data)

#def save_to_database(df, db_path='data/reddit_data.db'):
    """Save scraped data to PostgreSQL database"""
    conn = connect_to_db()
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reddit_comments (
            id TEXT PRIMARY KEY,
            body TEXT,
            score INTEGER,
            created_utc TIMESTAMP,
            post_title TEXT
        )
    """)

    # Insert data
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO reddit_comments (id, author, body, score, created_utc, subreddit, post_id, post_title)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                score = EXCLUDED.score
        """, (row['id'], row['author'], row['body'], row['score'], row['created_utc'], 
              row['subreddit'], row['post_id'], row['post_title']))

    conn.commit()
    cur.close()
    conn.close()
    

def main():
    reddit = connect_to_reddit()
    subreddits = ['stocks', 'wallstreetbets']  # Add more subreddits as needed

    for subreddit in subreddits:
        print(f"Scraping r/{subreddit}...")
        df = scrape_subreddit(reddit, subreddit)
        #save_to_database(df)
        print(connect_to_db())
        print(f"Saved {len(df)} comments from r/{subreddit}")

if __name__ == "__main__":
    main()