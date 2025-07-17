import pytest
from unittest.mock import MagicMock, patch
from reddit_scraper import scrape_reddit_user

@patch("reddit_scraper.praw.Reddit")
def test_scrape_reddit_user_returns_expected_data(mock_reddit_class):
    # Mock Redditor object
    mock_redditor = MagicMock()
    mock_redditor.comments.new.return_value = [
        MagicMock(body="Comment 1"),
        MagicMock(body="Comment 2")
    ]
    mock_redditor.submissions.new.return_value = [
        MagicMock(title="Post 1", selftext="Body 1"),
        MagicMock(title="Post 2", selftext="Body 2")
    ]

    # Configure the Reddit instance to return the mock redditor
    mock_reddit_instance = mock_reddit_class.return_value
    mock_reddit_instance.redditor.return_value = mock_redditor

    # Call the function
    user_url = "https://www.reddit.com/user/testuser/"
    user_text = scrape_reddit_user(user_url, limit=2)

    # Assertions
    assert isinstance(user_text, str)
    assert "Comment 1" in user_text
    assert "Post 1" in user_text
    assert "Body 2" in user_text
