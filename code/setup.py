import os
from config.settings import COOKIES_PATH, ACCOUNTS_PATH, MESSAGE_PATH, POST_PATH, LOG_PATH, QUARANTINE_PATH, TWEETS_PATH, PICTURES_PATH, SUSPENDED_PATH

def setup():
    print("Setting up directories...")
    # Create directories or files if they don't exist
    if not os.path.exists(PICTURES_PATH):
        os.system(f"mkdir -p {PICTURES_PATH}")
    if not os.path.exists(COOKIES_PATH):
        os.system(f"mkdir -p {COOKIES_PATH}")
    if not os.path.exists(LOG_PATH):
        os.system(f"mkdir -p {LOG_PATH}")

    print("Setting up config files...")

    # Create files if they don't exist
    if not os.path.exists(MESSAGE_PATH):
        os.system(f"touch {MESSAGE_PATH}")
    if not os.path.exists(POST_PATH):
        os.system(f"touch {POST_PATH}")
    if not os.path.exists(QUARANTINE_PATH):
        os.system(f"touch {QUARANTINE_PATH}")
    if not os.path.exists(TWEETS_PATH):
        os.system(f"touch {TWEETS_PATH}")
    if not os.path.exists(ACCOUNTS_PATH):
        os.system(f"touch {ACCOUNTS_PATH}")
    if not os.path.exists(SUSPENDED_PATH):
        os.system(f"touch {SUSPENDED_PATH}")

    # Install dependencies
    os.system("pip install -r requirements.txt")

    print("Setup complete.")

def main():
    setup()

if __name__ == '__main__':
    main()