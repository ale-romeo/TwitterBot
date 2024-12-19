import os
import random
import pyperclip
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.logging_handler import trace_account_status, log_error, trace_account_raid
from utils.file_handler import get_random_emojis, get_random_picture, get_random_message, lock_account, suspend_account
from config.settings import TEST_TWITTER_URL, PROFILES_PATH
from config.env import PROJECT

class SeleniumActions:
    def __init__(self, proxy, processed_tracker):
        self.tweet = None
        self.proxy = proxy
        self.processed_tracker = processed_tracker

    def random_delay(self, sb):
        sb.sleep(random.uniform(1, 3))
        return True

    def deal_auth_required(self, username):
        log_error(f"AUTH REQUIRED - {username}")
        quarantine_op = lock_account(username)
        if not quarantine_op:
            log_error(f"NOT FOUND - {username}")
        return True
    
    def deal_suspended(self, username):
        log_error(f"SUSPENDED - {username}")
        suspended_op = suspend_account(username)
        if not suspended_op:
            log_error(f"NOT FOUND - {username}")
        return True

    def check_auth_required(self, sb, username):
        if sb.get_current_url() == "https://x.com/account/access" or sb.is_text_visible("Your account has been locked", selector="span"):
            return self.deal_auth_required(username)

        return False

    def check_suspended(self, sb, username):
        if sb.is_text_visible("suspended", selector="span"):
            return self.deal_suspended(username)
        
        return False
    
    def login(self, sb, email, username, password):
        try:
            # Navigate to Twitter login page
            sb.uc_open("https://x.com/i/flow/login")
            self.random_delay(sb)
            input_selector = "input[name='text']"
            password_selector = "input[name='password']"
            next_button_selector = "//span[contains(text(), 'Next')]"
            login_button_selector = "//span[contains(text(), 'Log in')]"

            # Enter email and proceed
            try:
                sb.update_text(input_selector, email, timeout=10, retry=True)
                sb.slow_click(next_button_selector, by=By.XPATH)
                self.random_delay(sb)
            except:
                return False

            # Handle username or password input
            try:
                sb.update_text(input_selector, username, timeout=10, retry=True)
                sb.slow_click(next_button_selector, by=By.XPATH)
                self.random_delay(sb)
            except:
                pass

            try:
                sb.update_text(password_selector, password, timeout=10, retry=True)
                sb.slow_click(login_button_selector, by=By.XPATH)
                self.random_delay(sb)
                sb.save_cookies(username)
                return True
            except:
                self.check_suspended(sb, username)
                return False

        except:
            return False

    def verify_login(self, sb, tweet_url):
        try:
            sb.uc_open(tweet_url)
            self.random_delay(sb)

            try:
                sb.assert_element("[data-testid='login']", timeout=5)
                sb.sleep(1)
                return False
            except:
                return True
        except:
            return False

    def post_tweet(self, sb, message, picture):
        tweet_box_selector = "[data-testid='tweetTextarea_0']"
        submit_button_selector = "[data-testid='tweetButtonInline']"
        # Type the tweet message
        try:
            sb.add_text(tweet_box_selector, message, timeout=10)
        except:
            return False

        self.random_delay(sb)

        try:
            self.add_emojis(sb, tweet_box_selector, get_random_emojis())
        except:
            pass

        self.random_delay(sb)

        try:
            self.send_picture(sb, picture)
        except:
            pass

        self.random_delay(sb)

        try:
            sb.slow_click(submit_button_selector, timeout=10)
            self.random_delay(sb)
            return True
        except:
            return False

    def get_tweet(self, sb, tweet_url):
        tweet_selector_with_tabindex = "//article[@data-testid='tweet'][@tabindex='-1']"
        tweet_selector = "//article[@data-testid='tweet']"
        try:
            sb.uc_open(tweet_url)
            self.random_delay(sb)
            
            try:
                self.tweet = sb.find_element(tweet_selector_with_tabindex, by=By.XPATH)
                return True
            except:
                pass

            try:
                self.tweet = sb.find_element(tweet_selector, by=By.XPATH)
                return True
            except:
                return False

        except:
            return False

    def like(self, sb):
        unlike_selector = "[data-testid='unlike']"
        like_selector = "[data-testid='like']"
        # Check if the tweet is already liked
        try:
            self.tweet.find_element(By.CSS_SELECTOR, unlike_selector)
            return True  # Already liked
        except:
            pass

        try:
            sb.execute_script("arguments[0].click();", self.tweet.find_element(By.CSS_SELECTOR, like_selector))
            sb.sleep(0.5)
            return True
        except:
            return False

    def repost(self, sb):
        unretweet_selector = "[data-testid='unretweet']"
        retweet_selector = "[data-testid='retweet']"
        retweet_confirm_selector = "[data-testid='retweetConfirm']"
        # Check if already reposted
        try:
            self.tweet.find_element(By.CSS_SELECTOR, unretweet_selector)
            return True
        except:
            pass

        try:
            sb.execute_script("arguments[0].click();", self.tweet.find_element(By.CSS_SELECTOR, retweet_selector))
            sb.sleep(0.5)
            sb.slow_click(retweet_confirm_selector, timeout=5)
            return True
        except:
            return False

    def send_picture(self, sb, picture):
        # Locate and upload the picture using the file input element
        file_input_selector = "[data-testid='fileInput']"
        try:
            sb.choose_file(file_input_selector, picture, timeout=5)
            return True 
        except:
            return False
     
    def add_emojis(self, sb, text_box, emojis):
        try:
            for emoji in emojis:
                pyperclip.copy(emoji)
                sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
            return True
        except:
            return False
    
    def comment(self, sb, message):
        reply_button_selector = "[data-testid='reply']"
        textarea_selector = "[data-testid='tweetTextarea_0']"
        submit_button_selector = "[data-testid='tweetButton']"
        try:
            sb.execute_script("arguments[0].click();", self.tweet.find_element(By.CSS_SELECTOR, reply_button_selector))
            self.random_delay(sb)
        except:
            return False
        
        comment_type = random.choices(
            ['text', 'picture', 'text_picture', 'emojis'],
            weights=[0.15, 0.1, 0.7, 0.05]
        )[0]

        # Comment logic based on the type
        if comment_type in ['text', 'text_picture']:
            try:
                sb.add_text(textarea_selector, message, timeout=10)
                self.add_emojis(sb, textarea_selector, get_random_emojis())
                self.random_delay(sb)
            except:
                return False

        if comment_type in ['picture', 'text_picture']:
            try:
                self.send_picture(sb, get_random_picture())
                self.random_delay(sb)
            except:
                return False

        if comment_type == 'emojis':
            try:
                self.add_emojis(sb, textarea_selector, get_random_emojis())
                self.random_delay(sb)
            except:
                return False

        try:
            sb.slow_click(submit_button_selector, timeout=10)
            return True
        except:
            return False

    def bookmark(self, sb):
        unbookmark_selector = "[data-testid='unbookmark']"
        bookmark_selector = "[data-testid='bookmark']"
        # Check if the tweet is already bookmarked
        try:
            self.tweet.find_element(By.CSS_SELECTOR, unbookmark_selector)
            return True # Already bookmarked
        except:
            pass

        try:
            sb.execute_script("arguments[0].click();", self.tweet.find_element(By.CSS_SELECTOR, bookmark_selector))
            sb.sleep(0.5)
            return True
        except:
            return False
        
    def post(self, account, message, picture):
        email = account['email']
        username = account['username']
        password = account['password']
        
        try:
            with SB(
                uc=True,  # Enable undetected-chromedriver mode
                headless=False,  # Optional: Set True for headless mode
                proxy=self.proxy,  # Assign proxy if needed
                window_size="800,800",  # Set window size for the browser
                user_data_dir=os.path.join(PROFILES_PATH, username)  # Set user data directory for the browser
            ) as sb:
                # Open the website and clear cookies for a fresh start
                sb.uc_open("https://x.com")
                self.random_delay(sb)

                if not self.verify_login(sb, TEST_TWITTER_URL):
                    sb.delete_all_cookies()
                    sb.sleep(1)
                    if sb.load_cookies(username, -1):  # Load cookies if available
                        self.random_delay(sb)
                        
                        if not self.verify_login(sb, TEST_TWITTER_URL):
                            sb.delete_all_cookies()
                            sb.sleep(1)

                            if not self.login(sb, email, username, password):
                                return trace_account_status(account, False)
                    else:
                        # Perform login if no cookies are available
                        if not self.login(sb, email, username, password):
                            return trace_account_status(account, False)

                # Check for redirection to an authentication page
                sb.uc_open(TEST_TWITTER_URL)
                self.random_delay(sb)
                if sb.get_current_url() != TEST_TWITTER_URL and self.check_auth_required(sb, username):
                    sb.delete_all_cookies()
                    return False

                # Navigate to home and attempt to post the tweet
                sb.uc_open("https://x.com/home")
                self.random_delay(sb)
                if not self.post_tweet(sb, message, picture):
                    return trace_account_status(account, False)

                return trace_account_status(account, True)

        except:
            return trace_account_status(account, False)

    def interact(self, sb, account, tweet_url, comment=False):
        if not self.get_tweet(sb, tweet_url):
            return False
        
        self.random_delay(sb)

        # Check for redirection to an authentication page
        if sb.get_current_url() != tweet_url and self.check_auth_required(sb, account['username']):
            return False

        # Perform interactions (like, repost, comment, bookmark)
        interaction_success = (
            self.like(sb) and self.random_delay(sb) and
            self.repost(sb) and self.random_delay(sb) and
            self.bookmark(sb) and self.random_delay(sb)
        )

        if comment:
            interaction_success = interaction_success and self.comment(sb, get_random_message(project=PROJECT))

        self.random_delay(sb)

        if not interaction_success:
            return False

        return True

    def process_account(self, account):
        try:
            email = account['email']
            username = account['username']
            password = account['password']

            # Check if the tracker is empty
            if not self.processed_tracker:
                trace_account_raid(account, 0, 0)
                return True

            with SB(
                uc=True,  # Enable undetected-chromedriver mode
                headless=False,  # Optional: Set True for headless mode
                proxy=self.proxy,  # Assign proxy if needed
                window_size="800,800",  # Set window size for the browser
                user_data_dir=os.path.join(PROFILES_PATH, username)  # Set user data directory for the browser
            ) as sb:
                # Open X.com and clear session for a fresh start
                sb.uc_open("https://x.com")
                self.random_delay(sb)

                if self.check_auth_required(sb, username):
                    return False

                if not self.verify_login(sb, TEST_TWITTER_URL):
                    sb.delete_all_cookies()
                    sb.sleep(1)
                    if sb.load_cookies(username, -1):  # Load cookies if available
                        self.random_delay(sb)

                        if not self.verify_login(sb, TEST_TWITTER_URL):
                            sb.delete_all_cookies()
                            sb.sleep(1)

                            if not self.login(sb, email, username, password):
                                return trace_account_status(account, False)
                    else:
                        # Perform login if no cookies are found
                        if not self.login(sb, email, username, password):
                            return trace_account_status(account, False)

                # Check if the account is suspended
                if self.check_suspended(sb, username):
                    return False
                
                success_count = 0
                for link, processed_accounts in list(self.processed_tracker.items()):
                    if username in processed_accounts:
                        continue
                    
                    success = self.interact(sb, account, link, comment=random.choice([True, False]))

                    if success:
                        processed_accounts.add(username)
                        success_count += 1
                        
                trace_account_raid(account, len(self.processed_tracker.keys()), success_count)
                return True

        except:
            return trace_account_status(account, False)
