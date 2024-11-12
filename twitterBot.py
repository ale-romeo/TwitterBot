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

def get_random_message():
    # Pool of messages to comment on $ZHOA
    messages = [
        "$ZHOA is on fire! Trust in CZ and join the ride. #ZHOAmoon #CZvision ",
        "Big moves ahead for $ZHOA. CZ knows best. #ZHOArise #CZarmy ",
        "$ZHOA isn't just a coin; it's a revolution. #CZgenius #ZHOAworld ",
        "Hold $ZHOA and watch the future unfold. #CZpower #ZHOAmovement ",
        "CZ's vision with $ZHOA is unmatched. This is just the start. #ZHOAmoonshot ",
        "If you're not holding $ZHOA, you're missing out. #CZlegend #ZHOAwave ",
        "$ZHOA to the moon, powered by CZ's brilliance! #ZHOAarmy #CZgenius ",
        "Every $ZHOA holder knows: the future is bright with CZ. #ZHOAfuture ",
        "CZ + $ZHOA = unstoppable. #CZhero #ZHOAworld ",
        "$ZHOA is here to stay, and CZ is making it happen. #CZpower #ZHOAmovement ",
        "The momentum is real with $ZHOA. Thank you, CZ! #ZHOArise #CZvisionary ",
        "All in on $ZHOA. This is the future. #CZarmy #ZHOAmoon ",
        "CZ is driving $ZHOA to greatness. Don't miss out. #CZlegend #ZHOAwave ",
        "$ZHOA is more than hype—it's the next big thing. #CZvision #ZHOAfuture ",
        "Trust in CZ, hold $ZHOA, and watch history be made. #ZHOAmovement ",
        "Ready for the $ZHOA wave? CZ is leading the way. #CZgenius #ZHOAworld ",
        "Big things coming for $ZHOA. CZ is the real deal. #CZarmy #ZHOAmoonshot ",
        "The $ZHOA community is strong. Thanks to CZ, we're heading up. #CZpower ",
        "$ZHOA holders know: with CZ, the sky's the limit. #CZhero #ZHOAwave ",
        "Get on board with $ZHOA or watch from the sidelines. #ZHOAfuture #CZgenius ",
        "$ZHOA is lit! CZ's got us on the path to moon vibes. #ZHOAmoon #CZlegend ",
        "Real ones know $ZHOA is the move. CZ's got this on lock. #ZHOAarmy #CZpower ",
        "$ZHOA fam, we up next. CZ's taking us straight up. #ZHOArise #CZgenius ",
        "Y'all sleeping on $ZHOA? Wake up. CZ's leading the charge. #ZHOAwave #CZvision ",
        "Hold tight, $ZHOA's blasting off. CZ doesn't miss. #ZHOAmoonshot #CZarmy ",
        "$ZHOA's the play, no cap. Trust in CZ. #ZHOAfuture #CZhero ",
        "CZ and $ZHOA = a whole vibe. This is just the start. #ZHOAworld #CZmovement ",
        "Stacking $ZHOA like it's gold. CZ knows what's up. #ZHOAarmy #CZlegend ",
        "$ZHOA is on the rise, and CZ is the captain. Let's get it! #CZpower #ZHOAmovement ",
        "Big CZ energy driving $ZHOA. Don't miss this wave. #ZHOAwave #CZgenius ",
        "$ZHOA fam, this is our time. CZ's got the blueprint. #ZHOAmoon #CZarmy ",
        "Riding the $ZHOA train with CZ at the wheel. Next stop: moon city. #ZHOAworld #CZhero ",
        "If you know, you know: $ZHOA is the future, and CZ's calling the shots. #CZpower #ZHOAmovement ",
        "$ZHOA is heating up! CZ's magic touch is real. #ZHOAmoonshot #CZgenius ",
        "All in on $ZHOA. CZ is the GOAT in this game. #ZHOArise #CZlegend ",
        "$ZHOA's the next big flex. CZ's leading the charge, don't get left behind. #ZHOAwave ",
        "Trust in CZ, hold $ZHOA, and secure your spot. This is it. #CZarmy #ZHOAmovement ",
        "$ZHOA gang, we're just warming up. CZ's vision is unmatched. #ZHOAfuture #CZgenius ",
        "Moon-bound with $ZHOA, powered by the one and only CZ. #CZpower #ZHOAworld ",
        "The $ZHOA hype is real, and CZ is steering the ship. Join or watch us fly. #CZmovement #ZHOAmoon ",
        "CZ and $ZHOA are about to change the crypto world forever! #CZpower #ZHOAwave ",
        "$ZHOA is lit. CZ leading us up. #ZHOAmoon ",
        "CZ + $ZHOA = next level. #ZHOAwave ",
        "Holding $ZHOA strong. CZ knows. #ZHOArise ",
        "$ZHOA fam, we're up. #CZpower ",
        "Moon vibes with $ZHOA. CZ's the man. #ZHOAarmy ",
        "Real $ZHOA move. CZ approved. #ZHOAfuture ",
        "Stack $ZHOA. Trust CZ. #ZHOAworld ",
        "$ZHOA to the moon, no cap. #CZlegend ",
        "$ZHOA pumping! CZ's magic. #ZHOAmovement ",
        "Big CZ energy in $ZHOA. #ZHOAwave ",
        "$ZHOA is fire. CZ on top. #ZHOAmoonshot ",
        "$ZHOA fam, next stop: moon. #CZgenius ",
        "Riding $ZHOA with CZ. #ZHOAworld ",
        "CZ + $ZHOA = win. #ZHOAarmy ",
        "HODL $ZHOA. CZ got this. #CZpower ",
        "$ZHOA is the move. #CZhero ",
        "$ZHOA hype is real. #ZHOAwave ",
        "$ZHOA fam stays winning. #CZlegend ",
        "Moon-bound with $ZHOA. #CZgenius ",
        "$ZHOA all day. CZ leads. #ZHOAmoon ",
        "CZ + $ZHOA = unstoppable. #ZHOAfuture ",
        "Holding $ZHOA strong. #ZHOAmovement ",
        "$ZHOA is fire. #ZHOAwave ",
        "Big CZ energy in $ZHOA. #ZHOAmoonshot ",
        "$ZHOA fam, next stop: moon. #CZhero ",
        "Riding $ZHOA with CZ. #ZHOAworld ",
        "CZ + $ZHOA = win. #ZHOAarmy ",
        "HODL $ZHOA. CZ got this. #CZpower ",
        "$ZHOA is the move. #ZHOAfuture ",
        "$ZHOA hype is real. #ZHOAworld ",
        "$ZHOA fam stays winning. #ZHOAmovement ",
        "Moon-bound with $ZHOA. #ZHOAmoon ",
        "$ZHOA all day. CZ leads. #ZHOAwave ",
        "CZ + $ZHOA = unstoppable. #CZlegend ",
        "Holding $ZHOA strong. #CZgenius ",
        "$ZHOA is fire. #ZHOAmoonshot ",
        "Big CZ energy in $ZHOA. #ZHOAarmy "
    ]

    return random.choice(messages)

def get_random_post_text():
    # Pool of messages to post on Twitter
    posts = [
        "In a world where crypto trends come and go, $ZHOA stands tall as a testament to innovation and vision. Under the leadership of CZ, we're not just watching history unfold; we're part of it. Whether you're a seasoned investor or just stepping into the crypto world, this is the moment to ride the $ZHOA wave. #ZHOAarmy #CZlegend #CryptoRevolution",
        "The power of CZ's leadership has always been a game-changer in the world of crypto. Now, with $ZHOA, we're witnessing a new era of opportunity and growth. From its potential for exponential gains to the vibrant community backing it, $ZHOA is more than just a token—it's a movement that promises to reshape the market. If you're not on board yet, you're missing out on the future of decentralized finance. #ZHOAfuture #CZpower #CryptoInnovation",
        "The rise of $ZHOA isn't just another story in the crypto space; it's the story of transformation, ambition, and the unstoppable force that is CZ. With each passing day, $ZHOA proves that it's not just a meme coin; it's a symbol of resilience and strategy. From strong market moves to a dedicated following, the $ZHOA wave is building momentum. Are you part of the revolution or just watching from the sidelines? #ZHOAmoonshot #CZgenius #CryptoCommunity",
        "Every $ZHOA holder knows this isn't just an investment—it's a statement of belief in what crypto can achieve. With CZ's unmatched insight and innovative drive, $ZHOA is more than ready to make waves that extend far beyond today's charts. As we hold and watch it rise, we remember: fortune favors the bold. Don't let this opportunity pass you by. #CZvision #ZHOAmoon #NextBigThing",
        "In the fast-paced world of crypto, stability and vision are rare. Enter $ZHOA, a token backed by the strategic brilliance of CZ. For those in the know, $ZHOA isn't just another trend; it's the beginning of something bigger, a shift in how we understand meme coins and their impact on the market. Every step with CZ is a step toward a brighter, more prosperous future. Are you ready to see how high this wave will take you? #CZhero #ZHOAmoonshot #CryptoLeaders",
        "The world of crypto is unpredictable, but one thing remains constant: CZ's leadership has the power to transform the market. Now, with $ZHOA, we're witnessing a revolution unfold. From its rapid growth to its loyal community, $ZHOA embodies the spirit of innovation and ambition. If you're holding, you know the excitement; if you're watching, it's time to get involved. This is the journey to financial freedom, powered by $ZHOA and guided by CZ. #ZHOAwave #CZarmy #CryptoSuccess",
        "$ZHOA is not just another coin; it's the manifestation of CZ's vision for a brighter future in the crypto realm. Each holder is part of a global movement that thrives on trust, ambition, and the belief that together, we can reach for the stars. The community is growing, the momentum is unstoppable, and the journey is only just beginning. Don't miss your chance to be part of the $ZHOA revolution. #ZHOArise #CZmovement #NextLevelCrypto"
    ]

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
    prefix = r"C:\Users\Administrator\Documents\TwitterBot\img"
    # Pool of pictures to upload as comments
    pictures = [
        r"\binance_square.jpg",
        r"\cult_1.jpg",
        r"\cult_2.jpg",
        r"\cult_3.jpg",
        r"\cult_4.jpg",
        r"\cult_5.jpg",
        r"\cult_6.jpg",
        r"\cult_7.jpg",
        r"\driving.jpg",
        r"\moon.jpg",
        r"\eating.jpg",
        r"\freedom.jpg",
        r"\gym.jpg",
        r"\holder_guide.mp4",
        r"\narrative_1.jpg",
        r"\narrative_2.jpg",
        r"\nike.jpg",
        r"\out_of_prison.jpg",
        r"\pump.jpg",
        r"\wife.jpg",
        r"\wild.jpg",
        r"\zhoa.jpg",
        r"\box.mp4",
        r"\bullish.mp4",
        r"\christ.mp4",
        r"\diddy.mp4",
        r"\paperoni.mp4",
        r"\printer.mp4",
        r"\push.mp4",
    ]
    return prefix + random.choice(pictures)

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
        "email": "zhoaking@tutamail.com",
        "username": "KingZhoa",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "zhoafollower@gmail.com",
        "username": "FollowerZhoa",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "zhoaprince@gmail.com",
        "username": "ZhoaPrince",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "cryptosucksfr@proton.me",
        "username": "CryptoSucksfr",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "bnbhodler@proton.me",
        "username": "BnBHodl3r",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "williamcryptospear@proton.me",
        "username": "WCryptospeare",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "zhoaraidermasterproton.me@proton.me",
        "username": "ZhoaRaider",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "lebrongemss@proton.me",
        "username": "LeBronGemss",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "cryptosiummm@proton.me",
        "username": "CryptoSiummm",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "kaicenatmydad@proton.me",
        "username": "KaiCenatmydad",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "ishowcryptospeed@proton.me",
        "username": "iShowCryptoSpee",
        "password": "$$ZHOA$$1B"
    }
]

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
        with open(f"{username}_cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)
        logging.info(f"Saved cookies for {username}")

    def load_cookies(self, username):
        """Load cookies for a specific account."""
        if os.path.exists(f"{username}_cookies.pkl"):
            with open(f"{username}_cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            logging.info(f"Loaded cookies for {username}")
            return True
        return False
    
    def login(self, email, username, password):
        try:        
            # Perform manual login if cookies aren't loaded or are expired
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

            self.save_cookies(username)
            return True

        except Exception as e:
            random_delay()
            return False
        
    def post_tweet(self, message, picture):
        try:
            random_delay()
            # Type the tweet
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            tweet_box.send_keys(message)
            self.add_emojis(get_random_emojis())

            # Attach a picture
            self.send_picture(picture)
            random_delay()

            # Submit tweet
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            submit_button.click()
            return True
        except Exception as e:
            return
        
    def post(self, account, message, picture):
        email = account['email']
        username = account['username']
        password = account['password']

        if not self.load_cookies(username):
            if not self.login(email, username, password):
                trace_account_status(account, False)
                return False
        
        if not self.post_tweet(message, picture):
            trace_account_status(account, False)
            return False
        
        trace_account_status(account, True)
        return True

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

        except Exception as e:
            return False

    def like(self):
        try:
            random_delay()
            # Check if the tweet is already liked
            try:
                unlike_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unlike']")
                if unlike_button:
                    return True
            except Exception as e:
                # Try to find and click the "like" button
                like_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='like']")
                self.driver.execute_script("arguments[0].click();", like_button)
            return True
        except Exception as e:
            return False


    def repost(self):
        try:
            random_delay()
            # Check if the tweet is already reposted
            try:
                unretweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unretweet']")
                if unretweet_button:
                    return True
            except Exception as e:
                # Try to find and click the "repost" button
                retweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
                self.driver.execute_script("arguments[0].click();", retweet_button)

                # Confirm repost
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
                )
                self.driver.execute_script("arguments[0].click();", confirm_button)
                return True
        except Exception as e:
            return False

    def send_picture(self, picture):
        try:
            random_delay()
            # Click the "Add photo" button
            add_photo_button = WebDriverWait(self.driver, 10).until(
                # button is located by its aria-label attribute: aria-label="Add photos or video"
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
            # Click the "Add emoji" button
            add_emoji_button = WebDriverWait(self.driver, 10).until(
                # button is located by its aria-label attribute: aria-label="Add emoji"
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
                # Click the desired emoji
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
        except Exception as e:
            return False

    def comment(self, message):
        try:
            random_delay()
            # Click reply button
            reply_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='reply']")
            self.driver.execute_script("arguments[0].click();", reply_button)
            random_delay()

            # Randomly but weightedly select between commenting text + emojis / picture / text + emojis + picture / emojis
            comment_type = random.choices(['text', 'picture', 'text_picture', 'emojis'], weights=[0.1, 0.05, 0.8, 0.05])[0]
            if comment_type == 'text':
                # Type the comment
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
                )
                comment_box.send_keys(message)
                self.add_emojis(get_random_emojis())
            elif comment_type == 'picture':
                # Attach a picture
                picture = get_random_picture()
                self.send_picture(picture)
            elif comment_type == 'text_picture':
                # Type the comment
                comment_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
                )
                comment_box.send_keys(message)
                self.add_emojis(get_random_emojis())

                # Attach a picture
                picture = get_random_picture()
                self.send_picture(picture)
            elif comment_type == 'emojis':
                self.add_emojis(get_random_emojis())

            random_delay()

            # Submit comment
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
            )
            submit_button.click()
            return True
        except Exception as e:
            return False

    def bookmark(self):
        try:
            random_delay()
            
            # Check if the tweet is already bookmarked
            try:
                unbookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unbookmark']")
                if unbookmark_button:
                    return True
            except Exception as e:
                # Try to find and click the "bookmark" button
                bookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='bookmark']")
                self.driver.execute_script("arguments[0].click();", bookmark_button)
                return True
        except Exception as e:
            return False

    def interact(self, account, tweet_url):
        email = account['email']
        username = account['username']
        password = account['password']
        if not self.load_cookies(username):
            if not self.login(email, username, password):
                trace_account_status(account, False)
                return False
        
        # Check if there are some issues with the account
        if not self.get_tweet(tweet_url) or not self.like() or not self.repost() or not self.comment(get_random_message()) or not self.bookmark():
            trace_account_status(account, False)
            return False
        
        trace_account_status(account, True)
        return True

    def restart(self):
        self.driver.delete_all_cookies()

    def teardown(self):
        self.driver.quit()


class tgActions():
    def __init__(self):
        try:
            self.application = Application.builder().token('7845049094:AAHTfvuka55LWrGGtp-lI5t_Kx_L3GAlhzk').build()

            # Register command and message handlers
            self.application.add_handler(CommandHandler('post', self.post))
            self.application.add_handler(CommandHandler('logs', self.logs))
            self.application.add_handler(MessageHandler(filters.TEXT, self.monitor_group_messages))
            logging.info("Telegram bot initialized")
        except Exception as e:
            print(e)
            logging.error("Failed to initialize Telegram bot")

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
    tg_actions = tgActions()
    tg_actions.start_polling()

if __name__ == "__main__":
    main()
