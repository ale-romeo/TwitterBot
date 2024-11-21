import os

user = os.getenv('USER')
PROXY_STRING = os.getenv('PROXY_STRING')
PICTURES_PATH = f"/home/{user}/Documents/TwitterBot/img/"
COOKIES_PATH = f"/home/{user}/Documents/TwitterBot/code/config/cookies/"
MESSAGE_PATH = f"/home/{user}/Documents/TwitterBot/code/config/messages.json"
POST_PATH = f"/home/{user}/Documents/TwitterBot/code/config/posts.json"
LOG_PATH = f"/home/{user}/Documents/TwitterBot/code/config/logs/automation.log"
ACCOUNTS_PATH = f"/home/{user}/Documents/TwitterBot/code/config/accounts.json"
QUARANTINE_PATH = f"/home/{user}/Documents/TwitterBot/code/config/quarantine.json"
SUSPENDED_PATH = f"/home/{user}/Documents/TwitterBot/code/config/suspended.json"
TWEETS_PATH = f"/home/{user}/Documents/TwitterBot/code/config/logs/tweets.json"
LOGS_PATH = f"/home/{user}/Documents/TwitterBot/code/config/logs/"

API_KEY = "aac405691061c7841c55612ed7477606"
TWITTER_URL = "https://www.x.com/"
PUBLIC_KEY = "4d9fc2f0-efb9-41a6-9986-586db3d92c3b"

TEST_TWITTER_URL = "https://x.com/aleromeo0/status/1854263974294118642"