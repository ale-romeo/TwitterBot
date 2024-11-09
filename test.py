from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys


import time
import logging
import random
import os
import pickle

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
    "$ZHOA is more than a coin, it's a movement powered by CZ's vision! #CZvisionary #ZHOAtothemoon ",
    "CZ is the captain of the $ZHOA ship, and we're all aboard for the ride of a lifetime! #ZHOAmoonshot #CZarmy ",
    "$ZHOA is more than crypto—it's the future, and CZ is leading the way! #CZgenius #ZHOAworld ",
    "The world of crypto belongs to $ZHOA and CZ! Watch this revolution unfold! #CZlegend #ZHOAarmy ",
    "We're witnessing history with $ZHOA! CZ is taking us to the next level! #CZvisionary #ZHOArise ",
    "CZ isn't just a leader, he's the visionary behind $ZHOA's rise! #CZmovement #ZHOAfuture ",
    "Holding $ZHOA is like having a front-row seat to the future of crypto! #CZpower #ZHOAmoon ",
    "CZ's influence is undeniable, and $ZHOA is set to conquer the crypto space! #CZlegend #ZHOAwave ",
    "The stars align for $ZHOA, and CZ is lighting the path to the moon! #CZarmy #ZHOAmoonshot ",
    "If you're with CZ, you're with the future. $ZHOA is leading the way! #CZvision #ZHOAarmy ",
    "The crypto world will never be the same again with $ZHOA! CZ is revolutionizing the game! #CZgenius #ZHOAfuture ",
    "$ZHOA is about to take over, and CZ is the mastermind behind it all! #CZlegend #ZHOAmoonshot ",
    "CZ's vision for $ZHOA is crystal clear—it's all the way to the moon! #CZpower #ZHOAworld ",
    "With CZ in charge, $ZHOA is more than just a coin—it's the future of finance! #CZmovement #ZHOArise ",
    "The cult of CZ grows with every $ZHOA holder! This is more than crypto—it's a movement! #CZarmy #ZHOAwave ",
    "$ZHOA is paving the way for a new crypto era, and CZ is leading the charge! #CZlegend #ZHOAfuture ",
    "CZ's genius is unmatched, and $ZHOA is proof that the future of crypto is here! #CZvision #ZHOAmoon ",
    "$ZHOA is not just a meme coin—it's a revolution powered by CZ's vision! #CZgenius #ZHOAworld ",
    "With CZ's leadership, $ZHOA is set to soar higher than ever! #CZarmy #ZHOAmoonshot ",
    "We're all in on $ZHOA because CZ is taking us to the moon! #CZlegend #ZHOAwave ",
    "CZ is the king of crypto, and $ZHOA is his crown jewel! #CZpower #ZHOAfuture ",
    "The future is bright for $ZHOA, and CZ is lighting the way! #CZgenius #ZHOAworld ",
    "$ZHOA is going to the stars, and CZ is the rocket fuel! #CZlegend #ZHOAmoon ",
    "CZ's vision is unstoppable, and $ZHOA is proof of his genius! #CZpower #ZHOAarmy ",
    "With CZ at the helm, $ZHOA is the next big thing in crypto! #CZgenius #ZHOAwave ",
    "The $ZHOA revolution is here, and CZ is the mastermind! #CZarmy #ZHOAmoonshot ",
    "$ZHOA is the ultimate tribute to CZ's greatness! #CZlegend #ZHOAworld ",
    "Hold on tight—CZ is steering $ZHOA straight to the top! #CZpower #ZHOAmoon ",
    "The future of crypto is $ZHOA, and CZ is guiding us all the way! #CZvision #ZHOAfuture ",
    "$ZHOA is more than a coin—it's a mission, and CZ is our leader! #CZarmy #ZHOAwave ",
    "With CZ behind it, $ZHOA is the future of meme coins! #CZlegend #ZHOAmoon ",
    "CZ's leadership is taking $ZHOA to new heights! #CZgenius #ZHOAworld ",
    "The $ZHOA wave is coming, and CZ is the force driving it! #CZarmy #ZHOAmoonshot ",
    "$ZHOA is making history, and CZ is the architect behind it all! #CZlegend #ZHOAfuture ",
    "CZ's brilliance shines through every $ZHOA success story! #CZpower #ZHOAworld ",
    "The crypto revolution starts with $ZHOA, and CZ is the leader we trust! #CZarmy #ZHOAmoon ",
    "$ZHOA is the future of crypto, and CZ is lighting the way to the moon! #CZgenius #ZHOAmoonshot ",
    "Every $ZHOA holder knows the power of CZ's vision—this is just the beginning! #CZlegend #ZHOAwave ",
    "CZ is leading the charge with $ZHOA, and the future is bright! #CZarmy #ZHOAfuture ",
    "We're all following CZ to the moon, with $ZHOA in hand! #CZpower #ZHOAworld ",
    "$ZHOA is destined for greatness, and CZ is taking us there! #CZgenius #ZHOAmoon ",
    "In CZ we trust! $ZHOA is going to change the game! #CZlegend #ZHOAmoonshot ",
    "CZ is the visionary, and $ZHOA is the revolution! #CZarmy #ZHOAfuture ",
    "$ZHOA holders are the chosen few—CZ is leading us to the stars! #CZgenius #ZHOAworld ",
    "With CZ at the helm, $ZHOA is the future of crypto! #CZpower #ZHOAmoon ",
    "$ZHOA is going places, and CZ is taking us along for the ride! #CZarmy #ZHOAwave ",
    "CZ's vision for $ZHOA is unstoppable—watch it soar to the moon! #CZlegend #ZHOAfuture ",
    "$ZHOA is taking over, and CZ is leading the charge! #CZarmy #ZHOAworld ",
    "CZ's leadership is pushing $ZHOA to new heights! #CZgenius #ZHOAmoon ",
    "$ZHOA is more than a coin—it's a revolution, and CZ is the mastermind! #CZlegend #ZHOAfuture ",
    "CZ and $ZHOA are about to change the crypto world forever! #CZpower #ZHOAwave "
    ]

    return random.choice(messages)

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
    # Pool of pictures to upload as comments
    pictures = [
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\binance_square.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_1.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_2.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_3.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_4.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_5.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_6.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\cult_7.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\driving.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\moon.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\eating.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\freedom.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\gym.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\holder_guide.mp4",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\narrative_1.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\narrative_2.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\nike.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\out_of_prison.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\pump.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\wife.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\wild.jpg",
        r"C:\Users\alexr\OneDrive\Documenti\personal_projects\TwitterBot\img\zhoa.jpg",
    ]
    return random.choice(pictures)

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
        "email": "zhoafollower@gmail.com",
        "username": "FollowerZhoa",
        "password": "$$ZHOA$$1B"
    },
    {
        "email": "zhoaprince@gmail.com",
        "username": "ZhoaPrince",
        "password": "$$ZHOA$$1B"
    }
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
        #options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome()
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
        )
        
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

            # Type the comment
            comment_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            comment_box.send_keys(message)
            self.add_emojis(get_random_emojis())

            # Attach a picture
            picture = get_random_picture()
            self.send_picture(picture)
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
        if not self.login(email, username, password):
            logging.error(f"Failed to login to {username}'s account")
            return False
        
        if not self.get_tweet(tweet_url):
            logging.error(f"Failed to retrieve the tweet")
            return False
        
        if not self.like():
            logging.error(f"Failed to like the tweet")
            return False
        
        if not self.repost():
            logging.error(f"Failed to repost the tweet")
            return False

        message = get_random_message()
        if not self.comment(message):
            logging.error(f"Failed to comment on the tweet")
            return False
        
        if not self.bookmark():
            logging.error(f"Failed to bookmark the tweet")
            return False
        
        logging.info(f"Interactions completed successfully on {username}'s account")
        return True

    def restart(self):
        self.driver.delete_all_cookies()

    def teardown(self):
        self.driver.quit()
    
def main():
    xactions = xActions()
    for account in accounts:
        result = xactions.interact(account, "https://x.com/Lvnten/status/1855270432292602187")



if __name__ == "__main__":
    main()
