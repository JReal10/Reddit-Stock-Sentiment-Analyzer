# scripts/data_fetcher.py

import praw
from .config import REDDIT_CLIENT_ID, REDDIT_SECRET_KEY, REDDIT_USER_NAME
from datetime import datetime, timedelta, date

def fetch_reddit_data(subreddit, start_date=None, end_date=None):
    """
    Fetches data from a specified subreddit using the Reddit API within a given date range.
    
    Args:
    subreddit (str): Name of the subreddit to fetch data from.
    start_date (date or datetime): The start date for fetching data (inclusive).
    end_date (date or datetime): The end date for fetching data (inclusive).

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
    
    # If no dates are provided, default to the last week
    if not start_date:
        start_date = datetime.now().date() - timedelta(days=7)
    if not end_date:
        end_date = datetime.now().date()
    
    # Convert date to datetime if necessary
    if isinstance(start_date, date):
        start_date = datetime.combine(start_date, datetime.min.time())
    if isinstance(end_date, date):
        end_date = datetime.combine(end_date, datetime.max.time())
    
    # Convert to UTC timestamp for Reddit API
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    for post in subreddit.search('daily discussion', sort='new', time_filter='all'):
        post_date = datetime.fromtimestamp(post.created_utc)
        
        # Check if the post is within the specified date range
        if start_date <= post_date <= end_date:
            if post.num_comments > 0:
                post.comments.replace_more(limit=10)
                for comment in post.comments.list():
                    comment_date = datetime.fromtimestamp(comment.created_utc)
                    # Check if the comment is within the specified date range
                    if start_date <= comment_date <= end_date:
                        posts.append({
                            'id': post.id + '_' + comment.id,
                            'body': comment.body,
                            'created_utc': comment_date,
                            'score': comment.score,
                            'post_url': post.url,
                        })
        elif post_date < start_date:
            # Stop searching if we've gone past the start date
            break
    
    return posts