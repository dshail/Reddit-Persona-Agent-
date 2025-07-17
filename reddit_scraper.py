import os
import praw
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "RedditPersonaAgent/0.1")

if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
    raise ValueError("Missing one or more Reddit API credentials in environment variables.")

# Initialize Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

def extract_username_from_url(url: str) -> str:
    """
    Extracts Reddit username from profile URL.
    Example: https://www.reddit.com/user/kojied/ -> kojied
    """
    return url.rstrip("/").split("/")[-1]

def scrape_reddit_user(profile_url: str, limit: int = 50) -> Dict[str, List[Dict[str, str]]]:
    """
    Scrapes posts and comments of a Reddit user.
    Returns a dictionary with two keys: 'posts' and 'comments'.
    Each item is a dict with 'text' and 'permalink'.
    """
    username = extract_username_from_url(profile_url)
    redditor = reddit.redditor(username)

    posts = []
    try:
        for submission in redditor.submissions.new(limit=limit):
            posts.append({
                "text": submission.title + "\n" + (submission.selftext or ""),
                "permalink": f"https://www.reddit.com{submission.permalink}"
            })
    except Exception as e:
        print(f"Error fetching posts: {e}")

    comments = []
    try:
        for comment in redditor.comments.new(limit=limit):
            comments.append({
                "text": comment.body,
                "permalink": f"https://www.reddit.com{comment.permalink}"
            })
    except Exception as e:
        print(f"Error fetching comments: {e}")

    return {
        "posts": posts,
        "comments": comments
    }
