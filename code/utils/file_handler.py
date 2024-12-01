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

def remove_interacted_tweets(tweet_url):
    tweets = load_json(TWEETS_PATH)
    if not tweet_url in tweets:
        return False
    tweets.remove(tweet_url)
    with open(TWEETS_PATH, "w") as file:
        json.dump(tweets, file, indent=4)
    return True

def get_random_emojis():
    emojis = [
        " 🚀", " 🌕", " 🔥", " 💰", " 💎",
        " 🔸", " 👑", " ✨", " 👏"
    ]
    return random.choices(emojis, k=random.randint(1, 3))

def get_random_picture():
    return os.path.join(PICTURES_PATH, random.choice(os.listdir(PICTURES_PATH)))

def get_raid_picture():
    return os.path.join(PICTURES_PATH, "push.gif")

def get_random_message():
    messages = load_json(MESSAGE_PATH)
    return random.choice(messages)

def get_random_post_text():
    posts = load_json(POST_PATH)
    return random.choice(posts)

def get_accounts(number=1):
    accounts_path = os.path.join(ACCOUNTS_PATH, f"accounts{number}.json")
    accounts = load_json(accounts_path)
    if not accounts:
        return []
    return accounts

def get_account_and_number(username):
    for i in range(1, 5):
        accounts = get_accounts(i)
        for account in accounts:
            if account['username'] == username:
                return account, i
    return None, None

def move_account_to_quarantine(username):
    account_to_move, number = get_account_and_number(username)
    if not account_to_move:
        return False
    
    active_accounts = get_accounts(number)
    
    active_accounts.remove(account_to_move)
    accounts_path = os.path.join(ACCOUNTS_PATH, f"accounts{number}.json")
    with open(accounts_path, "w") as file:
        json.dump(active_accounts, file, indent=4)

    # Load quarantined accounts and add the account
    quarantine_accounts = load_json(QUARANTINE_PATH)
    # Add the account number to the account
    account_to_move['number'] = number
    quarantine_accounts.append(account_to_move)

    # Save the updated quarantined accounts
    with open(QUARANTINE_PATH, "w") as file:
        json.dump(quarantine_accounts, file, indent=4)
        
    return True

def move_account_to_suspended(username):
    account_to_move, number = get_account_and_number(username)
    if not account_to_move:
        return False
    
    active_accounts = get_accounts(number)
    
    active_accounts.remove(account_to_move)
    accounts_path = os.path.join(ACCOUNTS_PATH, f"accounts{number}.json")
    with open(accounts_path, "w") as file:
        json.dump(active_accounts, file, indent=4)

    # Load quarantined accounts and add the account
    suspended_accounts = load_json(SUSPENDED_PATH)
    # Add the account number to the account
    account_to_move['number'] = number
    suspended_accounts.append(account_to_move)

    # Save the updated suspended accounts
    with open(SUSPENDED_PATH, "w") as file:
        json.dump(suspended_accounts, file, indent=4)
        
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

    account_number = account_to_move['number']
    del account_to_move['number']

    # Load active accounts and add the account
    active_accounts = get_accounts(account_number)
    active_accounts.append(account_to_move)

    accounts_path = os.path.join(ACCOUNTS_PATH, f"accounts{account_number}.json")
    # Save the updated active accounts
    with open(accounts_path, "w") as file:
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