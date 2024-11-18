import random
import time
import os
import re
from utils.file_handler import load_json
from config.settings import PICTURE_PATH, MESSAGE_PATH, POST_PATH

def random_delay():
    time.sleep(random.uniform(3, 8))

def get_random_emojis():
    emojis = [
        "Rocket", "Full moon symbol", "Fire", "Money bag", "Gem stone",
        "Small orange diamond", "Crown", "Sparkles", "Clapping hands sign"
    ]
    return random.choices(emojis, k=random.randint(1, 3))

def get_random_picture():
    user = os.getenv('USER')
    prefix = f"/home/{user}/Documents/TwitterBot/img/"
    return prefix + random.choice(os.listdir('img/'))

def get_random_message():
    messages = load_json("conf/messages.json")
    return random.choice(messages)

def get_random_post_text():
    posts = load_json("conf/posts.json")
    return random.choice(posts)

def extract_tweet_link(text):
    twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
    match = re.search(twitter_regex, text)
    if match:
        return match.group(0)
    return None