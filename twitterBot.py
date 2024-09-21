from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import random

def random_delay():
    time.sleep(random.uniform(2, 5))

logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class xActions():
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def login(self):
        try:
            self.driver.get("https://x.com/i/flow/login")
            random_delay()

            # Enter email
            self.driver.find_element(By.NAME, "text").send_keys("alexhaxtv@gmail.com")
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            random_delay()

            # Enter username
            self.driver.find_element(By.NAME, "text").send_keys("ZHOAMaster")
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            random_delay()

            # Enter password
            self.driver.find_element(By.NAME, "password").send_keys("$$ZHOA$$1B")
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
            )
            button.click()
            logging.info("Logged in successfully")

        except Exception as e:
            print(e)
            logging.error("Failed to login")
            self.teardown()

    def get_tweet(self, tweet_url):
        self.driver.get(tweet_url)

    def like(self, tweet_url):
        try:
            random_delay()
            
            # Click the like button
            like_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='like']"))
            )
            self.driver.execute_script("arguments[0].click();", like_button)
            logging.info(f"Liked tweet at {tweet_url}")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to like tweet at {tweet_url}")
            return False

    def repost(self, tweet_url):
        try:
            random_delay()

            # Click the repost button
            retweet_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweet']"))
            )
            self.driver.execute_script("arguments[0].click();", retweet_button)

            # Confirm repost
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
            )
            self.driver.execute_script("arguments[0].click();", confirm_button)
            logging.info(f"Reposted tweet at {tweet_url}")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to repost tweet at {tweet_url}")
            return False

    def comment(self, tweet_url, comment):
        try:
            random_delay()
            # Click reply button
            reply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='reply']"))
            )
            self.driver.execute_script("arguments[0].click();", reply_button)
            random_delay()

            # Type the comment
            comment_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            comment_box.send_keys(comment)

            # Submit comment
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
            )
            submit_button.click()
            logging.info(f"Commented on tweet at {tweet_url}")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to comment on tweet at {tweet_url}")
            return False        

    def bookmark(self, tweet_url):
        try:
            random_delay()
            
            # Click the bookmark button
            bookmark_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='bookmark']"))
            )
            self.driver.execute_script("arguments[0].click();", bookmark_button)
            logging.info(f"Bookmarked tweet at {tweet_url}")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to bookmark tweet at {tweet_url}")
            return False

    def teardown(self):
        # Close the browser
        self.driver.quit()


class tgActions():
    def __init__(self, x_actions):
        try:
            self.x_actions = x_actions
            self.token = '7646025864:AAHYxgepOWJ7eH0K1dyBdrLl0GIDen1bh0o'
            self.application = Application.builder().token(self.token).build()

            # Register command and message handlers
            self.application.add_handler(CommandHandler('start', self.start))
            self.application.add_handler(CommandHandler('help', self.commands))
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            logging.info("Telegram bot initialized")
        except Exception as e:
            print(e)
            logging.error("Failed to initialize Telegram bot")

    async def commands(self, update, context):
        await update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show this help message')

    async def start(self, update, context):
        await update.message.reply_text('Hi! I am your Twitter Raid bot! I will monitor for Twitter links.')

    def extract_twitter_link(self, text):
        twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
        match = re.search(twitter_regex, text)
        if match:
            return match.group(0)
        return None

    async def handle_message(self, update, context):
        text = update.message.text
        twitter_link = self.extract_twitter_link(text)
        if twitter_link:
            await update.message.reply_text(f'Twitter link found: {twitter_link}')
            
            self.x_actions.get_tweet(twitter_link)
            like = self.x_actions.like(twitter_link)
            bookmark = self.x_actions.bookmark(twitter_link)
            repost = self.x_actions.repost(twitter_link)
            comment = self.x_actions.comment(twitter_link, "TO THE MOON!")
            if not like:
                await update.message.reply_text(f'Failed to like the tweet at {twitter_link}')

            if not bookmark:
                await update.message.reply_text(f'Failed to bookmark the tweet at {twitter_link}')

            if not repost:
                await update.message.reply_text(f'Failed to repost the tweet at {twitter_link}')

            if not comment:
                await update.message.reply_text(f'Failed to comment on the tweet at {twitter_link}')

            await update.message.reply_text(f'Other actions completed on tweet at {twitter_link}')

        else:
            await update.message.reply_text('No Twitter link detected.')
    

    def start_polling(self):
        self.application.run_polling()

def main():
    # Initialize Twitter automation actions
    x = xActions()
    x.login()  # Logs in to Twitter

    # Initialize Telegram bot with xActions
    tg_bot = tgActions(x)
    
    # Start the Telegram bot
    tg_bot.start_polling()

if __name__ == '__main__':
    main()
