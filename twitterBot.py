import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

import time
import re
import logging
import random
import os
import pickle

def random_delay():
    time.sleep(random.uniform(2, 5))

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def get_random_message():
    # Pool of messages to comment on $ZHOA
    messages = load_json("conf/messages.json")

    return random.choice(messages)

def get_random_post_text():
    # Pool of messages to post on Twitter
    posts = load_json("conf/posts.json")

    return random.choice(posts)

def get_random_emojis():
    # Pool of emojis names to use in comments
    emojis = [
        "Rocket",
        "Full moon symbol",
        "Fire",
        "Money bag",
        "Gem stone",
        "Small orange diamond",
    ]

    return random.choices(emojis, k=random.randint(1, 3))

def get_random_picture():
    prefix = r"/home/user/Documents/TwitterBot/img/"
    # Pool of pictures to upload as comments
    pictures = load_json("conf/pictures.json")
    return prefix + random.choice(pictures)

accounts = load_json("conf/accounts.json")

def trace_account_status(account, status):
    if status:
        logging.info(f"Successfully interacted with {account['username']}'s account")
    else:
        logging.error(f"Failed {account['username']}")

def save_interacted_tweet(tweet_url):
    with open("interacted_tweets.txt", "a") as file:
        file.write(f"{tweet_url}\n")

def check_interacted_tweet(tweet_url):
    with open("interacted_tweets.txt", "r") as file:
        return tweet_url in file.read()

logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class NoHttpRequestsFilter(logging.Filter):
    def filter(self, record):
        return not ("HTTP Request" in record.getMessage() and "api.telegram.org" in record.getMessage())

# Apply the filter to the root logger
for handler in logging.getLogger().handlers:
    handler.addFilter(NoHttpRequestsFilter())

class xActions():
    def __init__(self):
        self.tweet = None
        options = uc.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-logging')

        
        self.driver = uc.Chrome(options=options)
        self.driver.set_window_size(800, 800)
        
    def save_cookies(self, username):
        """Save cookies for a specific account."""
        cookies = self.driver.get_cookies()
        with open(f"cookies/{username}_cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)
        logging.info(f"Saved cookies for {username}")

    def load_cookies(self, username):
        """Load cookies for a specific account."""
        if os.path.exists(f"cookies/{username}_cookies.pkl"):
            with open(f"cookies/{username}_cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            logging.info(f"Loaded cookies for {username}")
            return True
        return False
    
    def login(self, email, username, password):
        try:        
            self.driver.get("https://x.com/i/flow/login")
            random_delay()

            textbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            textbox.send_keys(email)
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            random_delay()

            try:
                try:
                    username_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "text"))
                    )
                except:
                    password_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    )
                    password_box.send_keys(password)
                    button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
                    )
                    button.click()
                    random_delay()
                    self.save_cookies(username)
                    return True
            except:
                # Manually authenticate if the account is not recognized
                time.sleep(30)
                try:
                    username_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "text"))
                    )
                except:
                    return False
                
            username_box.send_keys(username)
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            random_delay()
            
            password_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_box.send_keys(password)
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
            )
            button.click()
            random_delay()
            self.save_cookies(username)
            return True

        except:
            # Reload the page if the login fails
            self.driver.get("https://x.com")
            return False
        
    def verify_login(self, username, tweet_url):
        try:
            random_delay()
            self.driver.get(tweet_url)
            random_delay()
            # Check if the login was successful
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='UserAvatar-Container-"+ username +"']"))
                )
                return True
            except:
                logging.error(f"Failed to load cookies for {username}")
                return False
        except:
            return False

    def post_tweet(self, message, picture):
        try:
            random_delay()
            
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            tweet_box.send_keys(message)
            self.add_emojis(get_random_emojis())

            self.send_picture(picture)
            random_delay()

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            submit_button.click()
            return True
        except:
            return False

    def get_tweet(self, tweet_url):
        try:
            self.driver.get(tweet_url)
            random_delay()
            # Try to find the tweet with tabindex="-1"
            try:
                self.tweet = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet'][@tabindex='-1']"))
                )
                return True
            except:
                try:
                    # If not found, fall back to finding the tweet without tabindex
                    self.tweet = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
                    )
                    return True
                except:
                    return False

        except:
            # Reload the page if the tweet isn't found
            self.driver.get("https://x.com")
            return False

    def like(self):
        try:
            random_delay()
            # Check if the tweet is already liked
            try:
                unlike_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unlike']")
                if unlike_button:
                    return True
            except:
                like_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='like']")
                self.driver.execute_script("arguments[0].click();", like_button)
            return True
        except:
            return False

    def repost(self):
        try:
            random_delay()
            # Check if the tweet is already reposted
            try:
                unretweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unretweet']")
                if unretweet_button:
                    return True
            except:
                retweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
                self.driver.execute_script("arguments[0].click();", retweet_button)

                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
                )
                self.driver.execute_script("arguments[0].click();", confirm_button)
                return True
        except:
            return False

    def send_picture(self, picture):
        try:
            random_delay()

            add_photo_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fileInput']"))
            )
            random_delay()
            add_photo_button.send_keys(picture)
            
            return True
        except Exception as e:
            return False

    def add_emojis(self, emojis):
        try:
            random_delay()
            add_emoji_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Add emoji']"))
            )
            self.driver.execute_script("arguments[0].click();", add_emoji_button)

            for emoji in emojis:
                # Search for the desired emoji
                emoji_search = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Search emojis']"))
                )
                emoji_search.send_keys(emoji)
                random_delay()
                
                emoji_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='{emoji}']"))
                )
                self.driver.execute_script("arguments[0].click();", emoji_button)

                # Clear the search bar
                emoji_clear = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='clearButton']"))
                )
                self.driver.execute_script("arguments[0].click();", emoji_clear)
                random_delay()

            # Simulate pressing the 'Esc' key to close the emoji picker
            emoji_search.send_keys(Keys.ESCAPE)
            
            return True
        except:
            return False

    def comment(self, message):
        try:
            random_delay()
            
            reply_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='reply']")
            self.driver.execute_script("arguments[0].click();", reply_button)
            random_delay()

            # Randomly but weightedly select between commenting text + emojis / picture / text + emojis + picture / emojis
            comment_type = random.choices(['text', 'picture', 'text_picture', 'emojis'], weights=[0.1, 0.05, 0.8, 0.05])[0]
            if comment_type == 'text':
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
                )
                comment_box.send_keys(message)
                self.add_emojis(get_random_emojis())

            elif comment_type == 'picture':
                picture = get_random_picture()
                self.send_picture(picture)

            elif comment_type == 'text_picture':
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
                )
                comment_box.send_keys(message)
                self.add_emojis(get_random_emojis())

                picture = get_random_picture()
                self.send_picture(picture)

            elif comment_type == 'emojis':
                self.add_emojis(get_random_emojis())

            random_delay()

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
            )
            submit_button.click()
            return True
        except:
            return False

    def bookmark(self):
        try:
            random_delay()
            
            # Check if the tweet is already bookmarked
            try:
                unbookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unbookmark']")
                if unbookmark_button:
                    return True
            except:
                bookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='bookmark']")
                self.driver.execute_script("arguments[0].click();", bookmark_button)
                return True
        except:
            return False
        
    def post(self, account, message, picture):
        email = account['email']
        username = account['username']
        password = account['password']

        # Delete all cookies to ensure a fresh start
        self.driver.get("https://rmooreblog.netlify.app/")
        self.driver.delete_all_cookies()

        random_delay()
        self.driver.get("https://x.com")
        if self.load_cookies(username):
            if not self.verify_login(username):  # Check if cookies are valid
                print(f"Cookies expired for {username}. Logging in manually.")
                self.driver.delete_all_cookies()  # Clear cookies if invalid
                if not self.login(email, username, password):  # Attempt login
                    trace_account_status(account, False)
                    return False
                self.save_cookies(username)  # Update cookies after login
        else:
            # Perform login if no cookies are found
            if not self.login(email, username, password):
                trace_account_status(account, False)
                return False
            self.save_cookies(username)

        random_delay()
        if not self.post_tweet(message, picture):
            logging.error(f"Failed to post tweet for {username}")
            return False
        
        logging.info(f"Successfully posted tweet for {username}")
        return True

    def interact(self, account, tweet_url):
        try:
            email = account['email']
            username = account['username']
            password = account['password']

            # Delete all cookies to ensure a clean session
            self.driver.get("https://rmooreblog.netlify.app/")
            self.driver.delete_all_cookies()

            random_delay()
            self.driver.get("https://x.com")
            if self.load_cookies(username):
                if not self.verify_login(username):  # Check if cookies are valid
                    print(f"Cookies expired for {username}. Logging in manually.")
                    self.driver.delete_all_cookies()  # Clear cookies if invalid
                    if not self.login(email, username, password):  # Attempt login
                        trace_account_status(account, False)
                        return False
                    self.save_cookies(username)  # Update cookies after login
            else:
                # Perform login if no cookies are found
                if not self.login(email, username, password):
                    trace_account_status(account, False)
                    return False
                self.save_cookies(username)

            # Check if there are some issues with the account
            if not self.get_tweet(tweet_url) or not self.like() or not self.repost() or not self.comment(get_random_message()) or not self.bookmark():
                trace_account_status(account, False)
                return False
            
            trace_account_status(account, True)
            return True
        except:
            # Reload the page if the interaction fails
            self.driver.get("https://rmooreblog.netlify.app/")
            return False

    def restart(self):
        self.driver.delete_all_cookies()

    def teardown(self):
        self.driver.quit()


class tgActions():
    def __init__(self):
        try:
            # Get the token from the environment variable
            token = os.getenv('TEL_BOT_TOKEN')
            if not token:
                raise ValueError("No token provided")
            self.application = Application.builder().token(token).build()

            # Register command and message handlers
            self.application.add_handler(CommandHandler('post', self.post))
            self.application.add_handler(CommandHandler('logs', self.logs))
            self.application.add_handler(MessageHandler(filters.TEXT, self.monitor_group_messages))
            logging.info("Telegram bot initialized")
        except Exception as e:
            print(e)
            logging.error("Failed to initialize Telegram bot")

    def extract_twitter_link(self, text):
        twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
        match = re.search(twitter_regex, text)
        if match:
            return match.group(0)
        return None

    async def monitor_group_messages(self, update, context: ContextTypes.DEFAULT_TYPE):
        chat_type = update.effective_chat.type
        """Monitor group messages for Twitter links."""
        message_text = update.message.text
        twitter_link = self.extract_twitter_link(message_text)

        if twitter_link and not check_interacted_tweet(twitter_link):
            await update.message.reply_text(f"ZHOA ARMY!! IT'S TIME TO SHINE 🔥🔥\n{twitter_link}")
            # Optionally, trigger the raid or interaction logic here
            result = self.raid(tweet_url=twitter_link)
            save_interacted_tweet(twitter_link)
            if chat_type == 'private':
                if result:
                    await update.message.reply_text("Raid successful!")
                else:
                    await update.message.reply_text("Raid failed. Please check the logs for more information.")

    def raid(self, tweet_url):
        raid_success = True
        open('bot.log', 'w').close()  # Erase logs
        xactions = xActions()

        for account in accounts:
            raid_success = xactions.interact(account, tweet_url)
            xactions.restart()
        xactions.teardown()
        return raid_success
    
    async def post(self, update, context: ContextTypes.DEFAULT_TYPE):
        chat_type = update.effective_chat.type

        if chat_type == 'private':
            if len(update.message.text.split(' ')) < 2:
                await update.message.reply_text('No message provided. Random message will be used.')
                message = get_random_post_text()
            else:
                message = ' '.join(update.message.text.split(' ')[1:])
            picture = get_random_picture()

            xactions = xActions()
            account = random.choice(accounts)
            post_success = xactions.post(account, message, picture)
            xactions.teardown()
            if post_success:
                await update.message.reply_text('Tweet posted successfully!')
            else:
                await update.message.reply_text('Failed to post the tweet.\nPlease check the logs for more information.')

    async def logs(self, update, context: ContextTypes.DEFAULT_TYPE):
        chat_type = update.effective_chat.type

        if chat_type == 'private':
            if os.path.exists('bot.log'):
                with open('bot.log', 'r') as log_file:
                    lines = log_file.readlines()[-20:]
                    log_content = ''.join(lines)
            else:
                log_content = "Log file not found."

            await update.message.reply_text(f"Last 20 logs:\n{log_content}")

    def start_polling(self):
        self.application.run_polling()

    
def main():
    tg_actions = tgActions()
    tg_actions.start_polling()

if __name__ == "__main__":
    main()
