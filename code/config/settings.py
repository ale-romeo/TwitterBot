import os

# Paths
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code", "config")
mod_files_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mod_files")

# Config paths
PICTURES_PATH = os.path.join(config_path, "pictures")
COOKIES_PATH = os.path.join(config_path, "cookies")
MESSAGE_PATH = os.path.join(config_path, "messages.json")
POST_PATH = os.path.join(config_path, "posts.json")
LOG_PATH = os.path.join(config_path, "automation.log")
ACCOUNTS_PATH = os.path.join(config_path, "accounts.json")
QUARANTINE_PATH = os.path.join(config_path, "quarantine.json")
SUSPENDED_PATH = os.path.join(config_path, "suspended.json")
TWEETS_PATH = os.path.join(config_path, "tweets.json")
LOGS_PATH = os.path.join(config_path, "logs")

# Modified SeleniumBase file
BASECASE_PATH = os.path.join(mod_files_path, "base_case.py")

TWITTER_URL = "https://www.x.com/"
TEST_TWITTER_URL = "https://x.com/ChengpangZhoa/status/1859703180977897978"