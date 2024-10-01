from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from telegram.ext import Application, CommandHandler, ContextTypes
from webdriver_manager.chrome import ChromeDriverManager

import time
import re
import logging
import random
import os
import threading

def random_delay():
    time.sleep(random.uniform(2, 5))

def get_random_message():
    # Pool of messages to comment on $ZHOA
    messages = [
    "$ZHOA is not just a token, it's a revolution! Follow CZ to financial freedom! #ZHOAarmy #CZhero ",
    "$ZHOA is making waves, and we're riding them straight to the top! #ZHOAtotheMoon #CZarmy ",
    "The CZ effect is real, and $ZHOA is the proof. Next stop? The moon! #CZtakeover #ZHOAmoonshot ",
    "$ZHOA is a movement! CZ is rewriting the rules of crypto once again! #ZHOAarmy #CZisKing ",
    "This is just the beginning! $ZHOA is heading for the stars, and we're all onboard! #ZHOAmoonshot #CZgenius ",
    "Every $ZHOA holder knows the future is bright with CZ! #ZHOARise #CZvisionary ",
    "CZ is leading the charge with $ZHOA - the future of meme coins is here! #CZmoves #ZHOAarmy ",
    "$ZHOA is more than a coin, it's a revolution driven by CZ's vision! #CZpower #ZHOAfuture ",
    "With CZ at the helm, $ZHOA is ready to take over the crypto world! #CZarmy #ZHOAworld ",
    "Big things are coming for $ZHOA! CZ is leading us into the next era of crypto! #ZHOAwave #CZlegend ",
    "$ZHOA is the coin of the future, powered by the one and only CZ! #ZHOAfuture #CZarmy ",
    "If you're not holding $ZHOA, you're missing out on the biggest crypto wave! #CZknows #ZHOAmoon ",
    "$ZHOA is unstoppable with CZ behind it! Get ready for the crypto ride of your life! #CZcult #ZHOAarmy ",
    "CZ is making history with $ZHOA - this is just the beginning! #CZlegend #ZHOAworld ",
    "$ZHOA is more than a meme, it's a mission! And CZ is guiding us all the way! #CZpower #ZHOAmoon ",
    "The future of crypto is here, and it's called $ZHOA! CZ is leading the charge! #CZarmy #ZHOAworld ",
    "With CZ's vision, $ZHOA is set to dominate the crypto market! #CZknowsbest #ZHOAmoon ",
    "Hold tight, $ZHOA is about to explode, and CZ is leading the way! #CZarmy #ZHOAtothemoon ",
    "CZ has spoken, and $ZHOA is the future! Are you ready for the crypto revolution? #CZmovement #ZHOAwave ",
    "$ZHOA isn't just a coin, it's a mission powered by CZ's genius! #CZgenius #ZHOAtotheMoon ",
    "In CZ we trust, and $ZHOA is the proof of his crypto mastery! #CZarmy #ZHOAworld ",
    "$ZHOA is about to change the game, and CZ is the mastermind behind it all! #CZlegend #ZHOAwave ",
    "CZ's vision, $ZHOA's future - together, we're going to the stars! #CZtakeover #ZHOAtotheMoon ",
    "This is the dawn of a new era, and $ZHOA is leading the charge with CZ! #ZHOAmoonshot #CZhero ",
    "$ZHOA is the coin the world needs, and CZ is the leader we trust! #CZarmy #ZHOAfuture ",
    "$ZHOA is taking over, and CZ is showing us the way to financial freedom! #CZknows #ZHOAmoon ",
    "CZ and $ZHOA are unstoppable! This is the next big thing in crypto! #CZlegend #ZHOAworld ",
    "$ZHOA is more than a meme coin, it's the future of crypto with CZ at the helm! #CZgenius #ZHOAmoon ",
    "CZ is leading $ZHOA to the moon, and there's no stopping us now! #ZHOAarmy #CZvision ",
    "The power of CZ is real, and $ZHOA is the proof! #CZtakeover #ZHOAmoon ",
    "If you're not in on $ZHOA, you're missing the biggest crypto revolution! #CZarmy #ZHOAworld ",
    "Hold $ZHOA, follow CZ, and watch your future grow! #CZvisionary #ZHOAmoon ",
    "$ZHOA is the meme coin of the future, and CZ is making it happen! #CZhero #ZHOAwave ",
    "$ZHOA is the ultimate tribute to CZ, the king of crypto! #CZcult #ZHOAarmy ",
    "$ZHOA is leading the charge to a new era of crypto, all thanks to CZ! #CZvision #ZHOAmoon ",
    "CZ has spoken, and $ZHOA is about to dominate the market! #CZknowsbest #ZHOAworld ",
    "With CZ's vision, $ZHOA is ready to take over the crypto world! #CZmovement #ZHOAmoon ",
    "This is just the beginning! $ZHOA is heading for the stars with CZ at the helm! #CZlegend #ZHOAtotheMoon ",
    "$ZHOA is the next big thing in crypto, and CZ is leading the charge! #CZarmy #ZHOAworld ",
    "The CZ revolution is here, and $ZHOA is the coin that will take us to the moon! #CZcult #ZHOAwave ",
    "$ZHOA isn't just a coin, it's a movement! Follow CZ to financial freedom! #CZvision #ZHOAmoonshot ",
    "CZ's vision is unstoppable, and $ZHOA is proof of his genius! #CZgenius #ZHOAtothemoon ",
    "$ZHOA is leading the crypto revolution, and CZ is the mastermind behind it! #CZpower #ZHOAwave ",
    "Every $ZHOA holder knows - this is the start of something legendary! #CZknowsbest #ZHOAarmy ",
    "CZ is creating history with $ZHOA - the coin that's changing everything! #CZlegend #ZHOAfuture ",
    "The future is here, and it's called $ZHOA! CZ is guiding us all the way! #CZhero #ZHOAworld ",
    "$ZHOA is taking over, and CZ is leading the way to the top! #CZarmy #ZHOAmoon ",
    "Big things are coming for $ZHOA, and CZ is leading us into the next era of crypto! #CZlegend #ZHOAworld ",
    "$ZHOA is more than a coin, it's a movement powered by CZ's vision! #CZvisionary #ZHOAtothemoon "
    ]

    return random.choice(messages)

accounts = [
    {
        "email": "alexhaxtv@gmail.com",
        "username": "ZHOAMaster",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "zhoacultist@yahoo.com",
        "username": "CultistZhoa",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "siyavo7648@abatido.com",
        "username": "ZhoaKing",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "zhoafollower@yahoo.com",
        "username": "ZhoaFollower",
        "password": "$$ZHOA$$1B"
    },
]

logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Disable logging from libraries like selenium and urllib3
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class xActions():
    def __init__(self):
        self.tweet = None
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
    
    def login(self, email, username, password, retries=3):
        try_count = 0
        while try_count < retries:
            try:
                self.driver.get("https://x.com/i/flow/login")
                random_delay()

                # Enter email
                self.driver.find_element(By.NAME, "text").send_keys(email)
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
                )
                button.click()
                random_delay()

                # Enter username
                self.driver.find_element(By.NAME, "text").send_keys(username)
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
                )
                button.click()
                random_delay()

                # Enter password
                self.driver.find_element(By.NAME, "password").send_keys(password)
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
                )
                button.click()
                random_delay()
                logging.info("Logged in successfully")
                return True

            except Exception as e:
                logging.error(f"Login attempt {try_count + 1} failed: {e}")
                try_count += 1
                if try_count == retries:
                    logging.error("Exceeded maximum retries for login")
                    return False
                random_delay()

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
                    logging.error("Failed to find the tweet")
                    return False

        except Exception as e:
            print(f"Failed to retrieve the tweet: {e}")
            if e.contains("HTTPConnectionPool(host='localhost', port=56471): Max retries exceeded"):
                self.teardown()
            return False

    def like(self):
        try:
            random_delay()
            # Check if the tweet is already liked
            try:
                unlike_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unlike']")
                if unlike_button:
                    logging.info("Tweet already liked")
                    return True
            except Exception as e:
                # If "unlike" button is not found, proceed to like the tweet
                logging.info("Tweet is not liked yet, proceeding to like")

            # Try to find and click the "like" button
            like_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='like']")
            self.driver.execute_script("arguments[0].click();", like_button)
            logging.info("Liked tweet successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to like tweet: {e}")
            return False


    def repost(self):
        try:
            random_delay()
            # Check if the tweet is already reposted
            try:
                unretweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unretweet']")
                if unretweet_button:
                    logging.info("Tweet already reposted")
                    return True
            except Exception as e:
                # If "unretweet" button is not found, proceed to repost the tweet
                logging.info("Tweet is not reposted yet, proceeding to repost")
            
            # Try to find and click the "repost" button
            retweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
            self.driver.execute_script("arguments[0].click();", retweet_button)

            # Confirm repost
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
            )
            self.driver.execute_script("arguments[0].click();", confirm_button)
            logging.info("Reposted tweet successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to repost tweet: {e}")
            return False


    def comment(self, message):
        try:
            random_delay()
            # Click reply button
            reply_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='reply']")
            self.driver.execute_script("arguments[0].click();", reply_button)
            random_delay()

            # Type the comment
            comment_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            comment_box.send_keys(message)

            # Submit comment
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
            )
            submit_button.click()
            logging.info(f"Commented")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to comment")
            return False

    def bookmark(self):
        try:
            random_delay()
            
            # Check if the tweet is already bookmarked
            try:
                unbookmark_button = self.ttweet.find_element(By.CSS_SELECTOR, "[data-testid='unbookmark']")
                if unbookmark_button:
                    logging.info("Tweet already bookmarked")
                    return True
            except Exception as e:
                # If the "unbookmark" button is not found, proceed to bookmark the tweet
                logging.info("Tweet is not bookmarked yet, proceeding to bookmark")
            
            # Try to find and click the "bookmark" button
            bookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='bookmark']")
            self.driver.execute_script("arguments[0].click();", bookmark_button)
            logging.info("Bookmarked tweet successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to bookmark the tweet: {e}")
            return False

    def interact(self, account, tweet_url):
        email = account['email']
        username = account['username']
        password = account['password']

        # Login
        if not self.login(email, username, password):
            logging.error(f"Failed to login to {username}'s account")
            return
        
        # Get the tweet
        if not self.get_tweet(tweet_url):
            logging.error(f"Failed to retrieve the tweet")
            return
        
        # Like the tweet
        if not self.like():
            logging.error(f"Failed to like the tweet")
            return
        
        # Repost the tweet
        if not self.repost():
            logging.error(f"Failed to repost the tweet")
            return

        # Comment on the tweet
        message = get_random_message()
        if not self.comment(message):
            logging.error(f"Failed to comment on the tweet")
            return
        
        # Bookmark the tweet
        if not self.bookmark():
            logging.error(f"Failed to bookmark the tweet")
            return
        
        logging.info(f"Interactions completed successfully on {username}'s account")

    def raid(self, tweet_url):
        raid_success = True
        # Erase logs
        open('bot.log', 'w').close()
        # Perform interactions on each account in parallel and see if any of them fail
        threads = []
        for account in accounts:
            thread = threading.Thread(target=self.interact, args=(account, tweet_url))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            if not thread.is_alive():
                raid_success = False

        return raid_success

    def restart(self):
        self.driver.delete_all_cookies()

    def teardown(self):
        self.driver.quit()


class tgActions():
    def __init__(self, x_actions):
        try:
            self.x_actions = x_actions
            self.application = Application.builder().token('7589018211:AAEsRAubiSjFFaEVSrMwO5lhYJ2ZU1a5YGo').build()

            # Register command and message handlers
            self.application.add_handler(CommandHandler('start', self.start))
            self.application.add_handler(CommandHandler('tweet', self.tweet))
            self.application.add_handler(CommandHandler('reset', self.reset))
            self.application.add_handler(CommandHandler('logs', self.logs))
            self.application.add_handler(CommandHandler('help', self.commands))
            logging.info("Telegram bot initialized")
        except Exception as e:
            print(e)
            logging.error("Failed to initialize Telegram bot")

    async def commands(self, update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Available commands:\n/start - Start the bot\n/tweet - Interact with a tweet\n/reset - Reset the bot\n/logs - Show last logs\n/help - Show available commands')

    async def start(self, update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Welcome! This bot will help you interact with tweets on Twitter. ')
        context.user_data['start'] = True

    async def tweet(self, update, context: ContextTypes.DEFAULT_TYPE):
        # Check if the bot has been started
        if 'start' not in context.user_data or not context.user_data['start']:
            await update.message.reply_text('Please start the bot first by typing /start.')
            return
        
        # Check if the user provided a Twitter link
        if len(update.message.text.split(' ')) < 2:
            await update.message.reply_text('Please provide a Twitter link with the /tweet command.')
            return
        # Ask the user to provide the Twitter link in the same message
        twitter_link = self.extract_twitter_link(update.message.text.split(' ')[1])
        if not twitter_link:
            await update.message.reply_text('No valid Twitter link detected. Please provide a valid Twitter link directly in the /tweet command.')
            return
        
        # Acknowledge the Twitter link
        await update.message.reply_text(f'Twitter link found: {twitter_link}')

        # Perform raid
        raid_success = self.x_actions.raid(tweet_url=twitter_link)
        if raid_success:
            await update.message.reply_text('Raid completed successfully!')
        else:
            await update.message.reply_text('Raid failed. Please check the logs for more information.')

    # Reset the bot and the Twitter bot
    async def reset(self, update, context: ContextTypes.DEFAULT_TYPE):
        self.x_actions.teardown()
        self.x_actions = xActions()
        context.user_data['start'] = False
        await update.message.reply_text('Bot has been reset successfully.')

    async def logs(self, update, context: ContextTypes.DEFAULT_TYPE):
        # Read the last 20 lines of bot.log
        if os.path.exists('bot.log'):
            with open('bot.log', 'r') as log_file:
                lines = log_file.readlines()[-20:]
                log_content = ''.join(lines)
        else:
            log_content = "Log file not found."

        # Send the logs to the user
        await update.message.reply_text(f"Last 20 logs:\n{log_content}")

    def start_polling(self):
        self.application.run_polling()

    def extract_twitter_link(self, text):
        twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
        match = re.search(twitter_regex, text)
        if match:
            return match.group(0)
        return None
    
def main():
    x_actions = xActions()
    tg_actions = tgActions(x_actions)
    tg_actions.start_polling()

if __name__ == "__main__":
    main()
