import os
import seleniumbase as _

# Paths
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
config_path = os.path.join(base_path, "code", "config")
mod_files_path = os.path.join(base_path, "mod_files")
logs_path = os.path.join(config_path, "logs")
seleniumbase_path = os.path.dirname(os.path.abspath(_.__file__))
media_path = os.path.join(base_path, "media")
profiles_path = os.path.join(base_path, "profiles")

# Config paths
PICTURES_PATH = os.path.join(media_path, "img")
MESSAGE_PATH = os.path.join(media_path, "text", "messages.json")
RAID_MESSAGE_PATH = os.path.join(media_path, "text", "raid_messages.json")
POST_PATH = os.path.join(media_path, "text", "posts.json")
LOG_PATH = os.path.join(logs_path, "automation.log")
TWEETS_PATH = os.path.join(logs_path, "tweets.json")
ACCOUNTS_PATH = os.path.join(config_path, "accounts.json")
LOGS_PATH = logs_path
PROFILES_PATH = profiles_path

# Modified SeleniumBase file
ORIGINAL_BASECASE_PATH = os.path.join(seleniumbase_path, "fixtures", "base_case.py")
MODIFIED_BASECASE_PATH = os.path.join(mod_files_path, "base_case.py")

TWITTER_URL = "https://www.x.com/"
TEST_TWITTER_URL = "https://x.com/ChengpangZhoa/status/1859703180977897978"