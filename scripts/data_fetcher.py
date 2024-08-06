# scripts/data_fetcher.py

import praw
from .config import REDDIT_CLIENT_ID, REDDIT_SECRET_KEY, REDDIT_USER_NAME
from datetime import datetime


def fetch_reddit_data(subreddit):
    """
    Fetches data from a specified subreddit using the Reddit API.
    
    Args:
    subreddit (str): Name of the subreddit to fetch data from.
    limit (int): Maximum number of posts to fetch.

    Returns:
    list: A list of dictionaries containing post data.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET_KEY,
        user_agent=REDDIT_USER_NAME
    )
    
    subreddit = reddit.subreddit(subreddit)
    posts = []
    
    for post in subreddit.search('daily discussion', sort='new', time_filter='week'):
        if post.num_comments > 0:
            # Scraping comments for each post
            post.comments.replace_more(limit= 10)                    
            for comment in post.comments.list():
                posts.append({
                    'id': post.id + '_' +  comment.id ,
                    'body': comment.body,
                    'created_utc': datetime.fromtimestamp(comment.created_utc),
                    'score': comment.score,
                    'post_url':post.url,
                })
    
    return posts