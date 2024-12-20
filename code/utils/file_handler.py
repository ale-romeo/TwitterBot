import json
import os
import random
from config.settings import PICTURES_PATH, MESSAGE_PATH, POST_PATH, ACCOUNTS_PATH, LOG_PATH, TWEETS_PATH, RAID_MESSAGE_PATH

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
        " 🔸", " 👑", " ✨", " 👏", " 💸",
        " 🪙"
    ]
    return random.choices(emojis, k=random.randint(1, 3))

def get_random_picture(project):
    return os.path.join(PICTURES_PATH, project, random.choice(os.listdir(os.path.join(PICTURES_PATH, project))))

def get_raid_picture(project):
    return os.path.join(PICTURES_PATH, project, "raid.gif")

def get_project_raid_message(project):
    messages = load_json(RAID_MESSAGE_PATH)
    if project in messages:
        return messages[project]
    return None

def get_random_message(project):
    messages = load_json(MESSAGE_PATH)
    if project in messages:
        return random.choice(messages[project])
    return None

def get_random_post_text(project):
    posts = load_json(POST_PATH)
    if project in posts:
        return random.choice(posts[project])
    return None

def get_proxy(project, vps):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    if project in accounts_data and vps in accounts_data[project]:
        return accounts_data[project][vps]['proxy']
    return None

def get_accounts(vps=None, project=None):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data

    active_accounts = []

    if project:
        # Check if the project exists
        if project in accounts_data:
            project_data = accounts_data[project]

            # If VPS is specified, fetch specific VPS accounts
            if vps:
                if vps in project_data:
                    vps_accounts = project_data[vps]['accounts']
                    active_accounts.extend([
                        account for account in vps_accounts 
                        if not account.get('isLocked') and not account.get('isSuspended')
                    ])
            else:
                # Fetch all accounts for all VPSs under the project
                for vps_data in project_data.values():
                    vps_accounts = vps_data['accounts']
                    active_accounts.extend([
                        account for account in vps_accounts 
                        if not account.get('isLocked') and not account.get('isSuspended')
                    ])
    else:
        # If project is None, fetch all active accounts across all projects
        for project_data in accounts_data.values():
            for vps_data in project_data.values():
                vps_accounts = vps_data['accounts']
                active_accounts.extend([
                    account for account in vps_accounts 
                    if not account.get('isLocked') and not account.get('isSuspended')
                ])

    return active_accounts

def lock_account(username):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    account_found = False

    # Search through all projects and VPSs
    for project, project_data in accounts_data.items():
        for vps, vps_data in project_data.items():
            for account in vps_data['accounts']:
                if account.get('username') == username:
                    account['isLocked'] = True  # Lock the account
                    account_found = True
                    break

    if account_found:
        with open(ACCOUNTS_PATH, "w") as file:
            json.dump(accounts_data, file, indent=4)
        return True
    else:
        return False

def unlock_account(username):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    account_found = False

    # Search through all projects and VPSs
    for project, project_data in accounts_data.items():
        for vps, vps_data in project_data.items():
            for account in vps_data['accounts']:
                if account.get('username') == username:
                    account['isLocked'] = False  # Unlock the account
                    account_found = True
                    break

    if account_found:
        with open(ACCOUNTS_PATH, "w") as file:
            json.dump(accounts_data, file, indent=4)
        return True
    else:
        return False

def suspend_account(username):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    account_found = False

    # Search through all projects and VPSs
    for project, project_data in accounts_data.items():
        for vps, vps_data in project_data.items():
            for account in vps_data['accounts']:
                if account.get('username') == username:
                    account['isSuspended'] = True  # Suspend the account
                    account_found = True
                    break

    if account_found:
        with open(ACCOUNTS_PATH, "w") as file:
            json.dump(accounts_data, file, indent=4)
        return True
    else:
        return False

def unsuspend_account(username):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    account_found = False

    # Search through all projects and VPSs
    for project, project_data in accounts_data.items():
        for vps, vps_data in project_data.items():
            for account in vps_data['accounts']:
                if account.get('username') == username:
                    account['isSuspended'] = False  # Unsuspend the account
                    account_found = True
                    break

    if account_found:
        with open(ACCOUNTS_PATH, "w") as file:
            json.dump(accounts_data, file, indent=4)
        return True
    else:
        return False

def get_locked_accounts(project=None, vps=None):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    
    if not project or project not in accounts_data:
        print("Invalid project or project not found.")
        return []

    project_data = accounts_data[project]

    # If VPS is specified, fetch locked accounts for that VPS
    if vps and vps in project_data:
        locked_accounts = [
            account for account in project_data[vps]['accounts']
            if account.get('isLocked', False)
        ]
        return locked_accounts

    # If VPS is not specified, fetch locked accounts for all VPSs under the project
    locked_accounts = []
    for vps_key, vps_data in project_data.items():
        locked_accounts.extend([
            account for account in vps_data['accounts']
            if account.get('isLocked', False)
        ])
    return locked_accounts

def get_suspended_accounts(project=None, vps=None):
    accounts_data = load_json(ACCOUNTS_PATH)  # Load the JSON data
    
    if not project or project not in accounts_data:
        print("Invalid project or project not found.")
        return []

    project_data = accounts_data[project]

    # If VPS is specified, fetch locked accounts for that VPS
    if vps and vps in project_data:
        locked_accounts = [
            account for account in project_data[vps]['accounts']
            if account.get('isSuspended', False)
        ]
        return locked_accounts

    # If VPS is not specified, fetch locked accounts for all VPSs under the project
    locked_accounts = []
    for vps_key, vps_data in project_data.items():
        locked_accounts.extend([
            account for account in vps_data['accounts']
            if account.get('isSuspended', False)
        ])
    return locked_accounts

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