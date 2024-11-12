# scripts/data_fetcher.py

import praw
from .config import REDDIT_CLIENT_ID, REDDIT_SECRET_KEY, REDDIT_USER_NAME
from datetime import datetime

def fetch_reddit_data(subreddit, comment_score_threshold=10, user_karma_threshold=1000):
    """
    Fetches data from a specified subreddit using the Reddit API for the last 30 days.
    Only includes comments with a score above `comment_score_threshold` and posted by users
    with karma above `user_karma_threshold`.
    
    Args:
    subreddit (str): Name of the subreddit to fetch data from.
    comment_score_threshold (int): Minimum score a comment must have to be included.
    user_karma_threshold (int): Minimum karma the user must have to be included.

    Returns:
    list: A list of dictionaries containing post and comment data.
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET_KEY,
        user_agent=REDDIT_USER_NAME
    )
    
    subreddit = reddit.subreddit(subreddit)
    posts = []

    # Use 'month' time filter to get posts from approximately the last 30 days
    for post in subreddit.search('daily discussion', sort='new', time_filter='month'):
        
        if post.num_comments > 0:
            post.comments.replace_more(limit=0)
            
            for comment in post.comments.list():
                comment_date = datetime.fromtimestamp(comment.created_utc)
                
                # Check if the comment score and user karma meet the thresholds
                if comment.score >= comment_score_threshold:
                    # Append the comment data if it meets the criteria
                    posts.append({
                        'id': post.id + '_' + comment.id,
                        'body': comment.body,
                        'created_utc': comment_date,
                        'score': comment.score,
                    })

    return posts
