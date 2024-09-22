from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import random

def random_delay():
    time.sleep(random.uniform(2, 5))

def get_random_message(token):
    # Pool of messages to comment on $ZHOA
    zhoa = [
    "$ZHOA to the moon! CZ is leading us to the stars! #ZHOA #CZarmy ",
    "The next big thing in crypto is here, and it's called $ZHOA! CZ is making history once again! #ZHOAworld ",
    "If you're not holding $ZHOA, are you even in the crypto game?  CZ is the GOAT!  #BinanceBoss #ZHOAarmy ",
    "In CZ we trust!  $ZHOA is more than a meme, it's a movement!  #ZHOAtoTheMoon #CZcult ",
    "Big things are coming for $ZHOA! The future of crypto is bright with CZ at the helm.  #CZfam #ZHOAHype ",
    "The Binance CEO creating a meme coin? That's all I need to hear. $ZHOA is going viral!  #CZlegend #ZHOAcoin ",
    "$ZHOA isn't just a coin, it's the ultimate tribute to the king of crypto, CZ!  #CZcult #ZHOAarmy ",
    "Every $ZHOA holder knows - this is the start of something legendary!  CZ leads, we follow! 🐉 #CZarmy #ZHOAmoon ",
    "$ZHOA holders are the chosen ones. CZ is taking us to financial freedom!  #CZfam #ZHOAWarriors ",
    "Ready for the next crypto explosion? $ZHOA is going to change the game!  CZ is the mastermind behind it all!  #CZhype #ZHOAarmy ",
    "CZ said it, I believe it: $ZHOA is gonna be legendary!  #CZknowsbest #ZHOAmoonshot ",
    "Follow CZ to the promised land! $ZHOA is taking us there!  #CZarmy #ZHOAHODL ",
    "Get ready for the $ZHOA wave - it's taking over!  CZ is the captain of this rocket ship  #ZHOATakeover #CZLegend ",
    "When CZ speaks, crypto listens. $ZHOA is the next chapter in the CZ empire!  #CZfam #ZHOArise ",
    "The cult of CZ grows stronger with $ZHOA! This is the future of meme coins, and we're here for it!  #CZcult #ZHOAarmy "
]

    # Pool of messages to comment on generic tokens
    generic = [
        "This token is going to change the game!  #HODL #CryptoRevolution ",
        "The future of crypto is here, and it's looking bright!  #NextBigThing #ToTheMoon ",
        "If you're not in, you're missing out!  Time to load up before it's too late! #CryptoRise #MoonMission ",
        "Get ready for a wild ride, this token is about to take off! #CryptoBoom #BuyTheDip ",
        "Holding strong and waiting for the moon!  #HODLgang #CryptoJourney ",
        "This token is more than just hype - it's the real deal!  #BelieveTheHype #CryptoLife ",
        "The crypto market never sleeps, and this token is waking up!  #AllNightHODL #CryptoDreams ",
        "Big things are coming for this token!  Don't miss out on the next wave!  #CryptoGrowth #FutureOfFinance ",
        "In crypto we trust!  This token is just getting started! #BuyAndHold #CryptoFaith ",
        "It's not a matter of if, it's a matter of when!  #PatiencePays #CryptoPower ",
        "The only way is up!  Keep holding and watch this token fly! #MoonShot #CryptoJourney ",
        "Every dip is an opportunity!  This token is going to explode soon! #CryptoDip #HODLStrong ",
        "Get ready for the next big breakout!  This token is set to soar!  #BreakingResistance #CryptoRise ",
        "This is just the beginning, we're headed for new heights!  #HODLandProsper #CryptoFuture ",
        "Feeling bullish on this one!  The next leg up is coming! #CryptoBullRun #NextMoonMission ",
        "This token has the potential to go parabolic!  #Next100x #CryptoGains ",
        "Every great journey starts with the first step!  This token is on the move! #NextCryptoGem #FutureOfFinance ",
        "Get in before the FOMO kicks in!  This token is about to make waves!  #EarlyAdopter #CryptoFOMO ",
        "HODLing this token like my life depends on it!  Big gains are coming! #CryptoDiamondHands #MoonMission ",
        "The road to financial freedom starts here!  This token is the way forward! #NextBigCrypto #FinancialRevolution ",
    ]
    if token == "$ZHOA":
        return random.choice(zhoa)
    else:
        return random.choice(generic)

logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

class xActions():
    def __init__(self):
        self.tweet = None
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1600, 900)
    
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
        try:
            self.driver.get(tweet_url)
            random_delay()
            # Try to find the tweet with tabindex="-1"
            try:
                self.tweet = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet'][@tabindex='-1']"))
                )
            except:
                # If not found, fall back to finding the tweet without tabindex
                self.tweet = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
                )

        except Exception as e:
            print(f"Failed to retrieve the tweet: {e}")
            return None

    def like(self):
        try:
            random_delay()
            # Click the like button
            like_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='like']")
            self.driver.execute_script("arguments[0].click();", like_button)
            logging.info(f"Liked tweet")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to like tweet")
            return False

    def repost(self):
        try:
            random_delay()
            # Click the repost button
            retweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
            self.driver.execute_script("arguments[0].click();", retweet_button)

            # Confirm repost
            confirm_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
            )
            self.driver.execute_script("arguments[0].click();", confirm_button)
            logging.info(f"Reposted tweet")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to repost tweet")
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
            
            # Click the bookmark button
            bookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='bookmark']")
            self.driver.execute_script("arguments[0].click();", bookmark_button)
            logging.info(f"Bookmarked tweet")
            return True
        except Exception as e:
            print(e)
            logging.error(f"Failed to bookmark")
            return False

    def teardown(self):
        # Close the browser
        self.driver.quit()


class tgActions():
    def __init__(self, x_actions):
        try:
            self.x_actions = x_actions
            self.application = Application.builder().token('7646025864:AAHYxgepOWJ7eH0K1dyBdrLl0GIDen1bh0o').build()

            # Register command and message handlers
            self.application.add_handler(CommandHandler('start', self.start))
            self.application.add_handler(CommandHandler('reset', self.reset))
            self.application.add_handler(CommandHandler('token', self.token))
            self.application.add_handler(CommandHandler('tweet', self.tweet))
            self.application.add_handler(CommandHandler('help', self.commands))
            logging.info("Telegram bot initialized")
        except Exception as e:
            print(e)
            logging.error("Failed to initialize Telegram bot")

    async def commands(self, update):
        await update.message.reply_text('Available commands:\n/start - Start the bot\n/reset - Reset the bot\n/tweet - Interact with a tweet\n/help - Show available commands')

    async def start(self, update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Welcome! This bot will help you interact with tweets on Twitter. Please enter the token name you want to interact with using /token.')
        context.user_data['start'] = True

    async def reset(self, update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Bot has been reset. Please enter the token name you want to interact with:')
        context.user_data['start'] = False
        context.user_data['token_name'] = None

    async def token(self, update, context: ContextTypes.DEFAULT_TYPE):
        if 'start' not in context.user_data or not context.user_data['start']:
            await update.message.reply_text('Please use /start to begin.')
            return
        
        token_name = update.message.text.split(' ')[1]
        if token_name.lower() == 'zhoa':
            context.user_data['token_name'] = '$ZHOA'
            await update.message.reply_text('Token name set to $ZHOA')
        elif token_name.lower() == 'generic':
            context.user_data['token_name'] = 'generic'
            await update.message.reply_text('Token name set to generic')
        else:
            await update.message.reply_text('Invalid token name. Please enter a valid token name. Token inserted: ' + token_name)

    async def tweet(self, update, context: ContextTypes.DEFAULT_TYPE):
        # Check if the bot has been started
        if 'start' not in context.user_data or not context.user_data['start']:
            await update.message.reply_text('Please start the bot first by typing /start.')
            return

        # Check if the token name is set
        if 'token_name' not in context.user_data or not context.user_data['token_name']:
            await update.message.reply_text('Please enter the token name first using /token.')
            return
        
        # Ask the user to provide the Twitter link in the same message
        twitter_link = self.extract_twitter_link(update.message.text.split(' ')[1])
        if not twitter_link:
            await update.message.reply_text('No valid Twitter link detected. Please provide a valid Twitter link directly in the /tweet command.')
            return
        
        # Acknowledge the Twitter link
        await update.message.reply_text(f'Twitter link found: {twitter_link}')

        # Perform interactions on Twitter
        self.x_actions.get_tweet(twitter_link)
        like = self.x_actions.like()
        repost = self.x_actions.repost()
        comment = self.x_actions.comment(get_random_message(context.user_data['token_name']))
        bookmark = self.x_actions.bookmark()

        if not like or not bookmark or not repost or not comment:
            await update.message.reply_text('Failed to perform interactions. Please try again later.')
        else:
            await update.message.reply_text('Interactions completed successfully!')

    def start_polling(self):
        self.application.run_polling()

    def extract_twitter_link(self, text):
        twitter_regex = r'https?://(www\.)?x\.com/[a-zA-Z0-9_]+/status/\d+'
        match = re.search(twitter_regex, text)
        if match:
            return match.group(0)
        return None

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