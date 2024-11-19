import random
import time
import re

def random_delay():
    time.sleep(random.uniform(3, 8))

def short_random_delay():
    time.sleep(random.uniform(1, 3))

def extract_tweet_link(text):
    twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
    match = re.search(twitter_regex, text)
    if match:
        return match.group(0)
    return None