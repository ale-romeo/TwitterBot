import json
import os
import pickle

def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

def save_interacted_tweet(tweet_url):
    with open("interacted_tweets.txt", "a") as file:
        file.write(f"{tweet_url}\n")

def check_interacted_tweet(tweet_url):
    if not os.path.exists("interacted_tweets.txt"):
        return False
    with open("interacted_tweets.txt", "r") as file:
        return tweet_url in file.read()

def save_cookies(self, username):
    cookies = self.driver.get_cookies()
    with open(f"cookies/{username}_cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)

def load_cookies(self, username):
    if os.path.exists(f"cookies/{username}_cookies.pkl"):
        with open(f"cookies/{username}_cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        return True
    return False