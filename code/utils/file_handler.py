import json
import os
import pickle
import random
from config.settings import PICTURES_PATH, MESSAGE_PATH, POST_PATH, ACCOUNTS_PATH, QUARANTINE_PATH, LOG_PATH, COOKIES_PATH, TWEETS_PATH, SUSPENDED_PATH

def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)

def save_interacted_tweet(tweet_url):
    tweets = load_json(TWEETS_PATH)
    tweets.append(tweet_url)
    with open(TWEETS_PATH, "w") as file:
        json.dump(tweets, file, indent=4)
    
def check_interacted_tweet(tweet_url):
    tweets = load_json(TWEETS_PATH)
    return tweet_url in tweets

def save_cookies(username, cookies):
    # Save cookies to COOKIES_PATH directory
    if not os.path.exists(COOKIES_PATH):
        os.makedirs(COOKIES_PATH)
    with open(COOKIES_PATH + f"{username}_cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)

def load_cookies(username):
    # Load cookies from COOKIES_PATH directory if exists
    if os.path.exists(COOKIES_PATH + f"{username}_cookies.pkl"):
        with open(COOKIES_PATH + f"{username}_cookies.pkl", "rb") as file:
            return pickle.load(file)
    return False

def get_random_emojis():
    emojis = [
        "Rocket", "Full moon symbol", "Fire", "Money bag", "Gem stone",
        "Small orange diamond", "Crown", "Sparkles", "Clapping hands sign"
    ]
    return random.choices(emojis, k=random.randint(1, 3))

def get_random_picture():
    return PICTURES_PATH + random.choice(os.listdir(PICTURES_PATH))

def get_raid_picture():
    return PICTURES_PATH + "push.gif"

def get_random_message():
    messages = load_json(MESSAGE_PATH)
    return random.choice(messages)

def get_random_post_text():
    posts = load_json(POST_PATH)
    return random.choice(posts)

def get_accounts():
    accounts = load_json(ACCOUNTS_PATH)
    return accounts

def move_account_to_quarantine(username):
    active_accounts = load_json(ACCOUNTS_PATH)

    account_to_move = None
    for account in active_accounts:
        if account['username'] == username:
            account_to_move = account
            break

    if not account_to_move:
        # Account not found in active accounts
        return False
    
    active_accounts.remove(account_to_move)
    with open(ACCOUNTS_PATH, "w") as file:
        json.dump(active_accounts, file, indent=4)

    # Load quarantined accounts and add the account
    quarantine_accounts = load_json(QUARANTINE_PATH)
    quarantine_accounts.append(account_to_move)

    # Save the updated quarantined accounts
    with open(QUARANTINE_PATH, "w") as file:
        json.dump(quarantine_accounts, file, indent=4)
        
    return True

def move_account_to_suspended(username):
    active_accounts = load_json(ACCOUNTS_PATH)

    account_to_move = None
    for account in active_accounts:
        if account['username'] == username:
            account_to_move = account
            break

    if not account_to_move:
        # Account not found in active accounts
        return False
    
    active_accounts.remove(account_to_move)
    with open(ACCOUNTS_PATH, "w") as file:
        json.dump(active_accounts, file, indent=4)

    # Load quarantined accounts and add the account
    quarantine_accounts = load_json(SUSPENDED_PATH)
    quarantine_accounts.append(account_to_move)

    # Save the updated quarantined accounts
    with open(SUSPENDED_PATH, "w") as file:
        json.dump(quarantine_accounts, file, indent=4)
        
    return True

def get_quarantined_accounts():
    accounts = load_json(QUARANTINE_PATH)
    return accounts

def move_account_to_active(username):
    quarantine_accounts = load_json(QUARANTINE_PATH)

    account_to_move = None
    for account in quarantine_accounts:
        if account['username'] == username:
            account_to_move = account
            break

    if not account_to_move:
        # Account not found in quarantine
        return False
    
    quarantine_accounts.remove(account_to_move)
    with open(QUARANTINE_PATH, "w") as file:
        json.dump(quarantine_accounts, file, indent=4)

    # Load active accounts and add the account
    active_accounts = load_json(ACCOUNTS_PATH)
    active_accounts.append(account_to_move)

    # Save the updated active accounts
    with open(ACCOUNTS_PATH, "w") as file:
        json.dump(active_accounts, file, indent=4)

    return True

def get_logs():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as log_file:
            lines = log_file.readlines()[-20:]
            log_content = ''.join(lines)
    else:
        log_content = "Log file not found."
    return log_content

def erase_logs():
    with open(LOG_PATH, 'w') as f:
        f.write('')