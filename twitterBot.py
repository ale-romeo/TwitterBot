from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging

logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class xActions():
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def login(self):
        try:
            self.driver.get("https://x.com/i/flow/login")
            time.sleep(2)
            self.driver.find_element(By.NAME, "text").send_keys("alexhaxtv@gmail.com")
            # Wait for the "Next" button to be clickable
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            time.sleep(5)


            self.driver.find_element(By.NAME, "text").send_keys("ZHOAMaster")
            # Wait for the "Next" button to be clickable
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            time.sleep(5)


            self.driver.find_element(By.NAME, "password").send_keys("$$ZHOA$$1B")
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
            )
            button.click()
            time.sleep(5)
            logging.info("Logged in successfully")

        except Exception as e:
            print(e)
            logging.error("Failed to login")
            self.teardown()

    def like_tweet(self, tweet_url):
        try:
            # Open the tweet
            self.driver.get(tweet_url)
            time.sleep(2)
            
            # Click the like button
            like_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='like']"))
            )
            like_button.click()
            logging.info(f"Liked tweet at {tweet_url}")
        except Exception as e:
            print(e)
            logging.error(f"Failed to like tweet at {tweet_url}")

    def retweet(self, tweet_url):
        # Open the tweet
        self.driver.get(tweet_url)
        time.sleep(2)

        # Click the retweet button
        retweet_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='retweet']"))
        )
        retweet_button.click()

    def comment_on_tweet(self, tweet_url, comment):
        # Open the tweet
        self.driver.get(tweet_url)
        time.sleep(2)
        
        # Click reply button
        reply_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='reply']"))
        )
        reply_button.click()

        # Type the comment
        comment_box = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='textbox']"))
        )
        comment_box.send_keys(comment)

        # Submit comment
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='tweetButton']"))
        )
        submit_button.click()

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
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            logging.info("Telegram bot initialized")
        except Exception as e:
            print(e)
            logging.error("Failed to initialize Telegram bot")

    async def start(self, update, context):
        await update.message.reply_text('Hi! I am your Twitter Raid bot! I will monitor for Twitter links.')

    async def handle_message(self, update, context):
        text = update.message.text
        twitter_link = self.extract_twitter_link(text)
        if twitter_link:
            await update.message.reply_text(f'Twitter link found: {twitter_link}')
            
            # Example: Like the tweet
            self.x_actions.like_tweet(twitter_link)
            await update.message.reply_text(f'Liked the tweet at {twitter_link}')
        else:
            await update.message.reply_text('No Twitter link detected.')

    async def commands(self, update, context):
        await update.message.reply_text('Available commands:\n/start - Start the bot\n/help - Show this help message')

    def extract_twitter_link(self, text):
        twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
        match = re.search(twitter_regex, text)
        if match:
            return match.group(0)
        return None

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
