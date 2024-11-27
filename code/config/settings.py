import os

# Main path
main_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code", "config")

# Paths
PICTURES_PATH = os.path.join(main_path, "pictures")
COOKIES_PATH = os.path.join(main_path, "cookies")
MESSAGE_PATH = os.path.join(main_path, "messages.json")
POST_PATH = os.path.join(main_path, "posts.json")
LOG_PATH = os.path.join(main_path, "automation.log")
ACCOUNTS_PATH = os.path.join(main_path, "accounts.json")
QUARANTINE_PATH = os.path.join(main_path, "quarantine.json")
SUSPENDED_PATH = os.path.join(main_path, "suspended.json")
TWEETS_PATH = os.path.join(main_path, "tweets.json")
LOGS_PATH = os.path.join(main_path, "logs")

TWITTER_URL = "https://www.x.com/"
TEST_TWITTER_URL = "https://x.com/ChengpangZhoa/status/1859703180977897978"