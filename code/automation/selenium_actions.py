import random
import undetected_chromedriver as uc
from captcha.solver import solve_funcaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logging_handler import trace_account_status, log_error
from utils.helpers import short_random_delay, random_delay
from utils.file_handler import get_random_emojis, get_random_picture, get_random_message, load_cookies, save_cookies, move_account_to_quarantine
from config.settings import TEST_TWITTER_URL


class SeleniumActions():
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
        self.driver.set_page_load_timeout(20)

    def deal_auth_required(self, username):
        log_error(f"AUTH REQUIRED - {username}")
        quarantine_op = move_account_to_quarantine(username)
        if not quarantine_op:
            log_error(f"NOT FOUND - {username}")
        return True

    def check_auth_required(self, username):
        if self.driver.current_url == "https://x.com/account/access":
            self.deal_auth_required(username)
            return True
        try:
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.ID, "arkose_iframe")
                )
            )
            self.deal_auth_required(username)
            return True
        except:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.ID, "arkoseFrame")
                    )
                )
                self.deal_auth_required(username)
                return True
            except:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='submit']"))
                    )
                    self.deal_auth_required(username)
                    return True
                except:
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "button[contains(text(), 'email')]"))
                        )
                        self.deal_auth_required(username)
                        return True
                    except:
                        try:
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Try again')]"))
                            )
                            self.deal_auth_required(username)
                            return True
                        except:
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
            short_random_delay()

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
                save_cookies(username, self.driver.get_cookies())
                return True
                
            username_box.send_keys(username)
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            short_random_delay()
            
            password_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_box.send_keys(password)
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
            )
            button.click()
            random_delay()
            save_cookies(username, self.driver.get_cookies())
            return True

        except:
            self.check_auth_required(username)
            return False
        
    def verify_login(self, username, tweet_url):
        try:
            short_random_delay()
            self.driver.get(tweet_url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="login"]'))
                )
                log_error(f"COOKIES FAILED - {username}")
                short_random_delay()
                return False
            except:
                return True
        except:
            return False

    def funcaptcha_solver(self):
        # Solve FunCaptcha
        solution_token = solve_funcaptcha()
        # Detect FunCaptcha iframe
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, "arkoseFrame")
            )
        )
        # Detect Verification iframe
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[aria-label='Verification challenge']")
            )
        )
        # Inject the solution token into the response field
        response_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "FunCaptcha-Token"))
        )
        self.driver.execute_script(f"arguments[0].value='{solution_token}';", response_field)
        # Detect Visual iframe
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[aria-label='Visual challenge']")
            )
        )
        # Detect Play button
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
        )
        self.driver.execute_script("arguments[0].click();", play_button)
        random_delay()

        if solution_token:
            # Click the submit button (if required for the form)
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
            )
            self.driver.execute_script("arguments[0].click();", submit_button)
            print("Captcha solution submitted.")
            random_delay()
        else:
            print("Captcha solving failed. No solution token obtained.")
            return False
        return True

    def post_tweet(self, message, picture):
        try:
            short_random_delay()
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']"))
            )
            tweet_box.send_keys(message)
            short_random_delay()
            self.add_emojis(get_random_emojis())

            short_random_delay()
            self.send_picture(picture)
            short_random_delay()

            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButtonInline']"))
            )
            self.driver.execute_script("arguments[0].click();", submit_button)
            random_delay()
            return True
        except:
            return False

    def get_tweet(self, tweet_url, retries=3):
        try:
            self.driver.get(tweet_url)
            random_delay()
            try:
                self.tweet = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet'][@tabindex='-1']"))
                )
                short_random_delay()
                return True
            except:
                try:
                    self.tweet = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
                    )
                    short_random_delay()
                    return True
                except:
                    return False

        except:
            return False

    def like(self):
        try:
            try:
                unlike_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unlike']")
                if unlike_button:
                    short_random_delay()
                    return True
            except:
                like_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='like']")
                self.driver.execute_script("arguments[0].click();", like_button)
                short_random_delay()
            return True
        except:
            return False

    def repost(self):
        try:
            try:
                unretweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unretweet']")
                if unretweet_button:
                    short_random_delay()
                    return True
            except:
                retweet_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='retweet']")
                self.driver.execute_script("arguments[0].click();", retweet_button)
                short_random_delay()
                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='retweetConfirm']"))
                )
                self.driver.execute_script("arguments[0].click();", confirm_button)
                short_random_delay()
                return True
        except:
            return False

    def send_picture(self, picture):
        try:
            add_photo_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='fileInput']"))
            )
            add_photo_button.send_keys(picture)
            random_delay()
            return True
        except:
            return False

    def add_emojis(self, emojis):
        try:
            add_emoji_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Add emoji']"))
            )
            self.driver.execute_script("arguments[0].click();", add_emoji_button)

            for emoji in emojis:
                emoji_search = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Search emojis']"))
                )
                emoji_search.send_keys(emoji)
                short_random_delay()
                
                emoji_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label='{emoji}']"))
                )
                self.driver.execute_script("arguments[0].click();", emoji_button)
                short_random_delay()

                emoji_clear = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='clearButton']"))
                )
                self.driver.execute_script("arguments[0].click();", emoji_clear)
                short_random_delay()

            emoji_search.send_keys(Keys.ESCAPE)
            random_delay()
            
            return True
        except:
            return False

    def comment(self, message):
        try:
            reply_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='reply']")
            self.driver.execute_script("arguments[0].click();", reply_button)
            short_random_delay()
            
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

            submit_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tweetButton']"))
            )
            self.driver.execute_script("arguments[0].click();", submit_button)
            random_delay()

            return True
        except:
            return False

    def bookmark(self):
        try:
            random_delay()
            try:
                unbookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='unbookmark']")
                if unbookmark_button:
                    short_random_delay()
                    return True
            except:
                bookmark_button = self.tweet.find_element(By.CSS_SELECTOR, "[data-testid='bookmark']")
                self.driver.execute_script("arguments[0].click();", bookmark_button)
                short_random_delay()
                return True
        except:
            return False
        
    def post(self, account, message, picture, retries=1):
        try:
            email = account['email']
            username = account['username']
            password = account['password']

            # Delete all cookies to ensure a fresh start
            short_random_delay()
            self.driver.get("https://x.com")
            short_random_delay()

            cookies = load_cookies(username)
            if cookies:  # Load cookies if available
                for cookie in cookies:
                    self.driver.add_cookie(cookie)

                if not self.verify_login(username, TEST_TWITTER_URL):  # Check if cookies are valid
                    print(f"COOKIES EXPIRED - {username}")
                    self.restart()
                    
                    if not self.login(email, username, password):
                        trace_account_status(account, False)
                        return False
            else:
                if not self.login(email, username, password):
                    trace_account_status(account, False)
                    return False
            
            # Check if it gets redirected to an authentication page
            if self.get_tweet(TEST_TWITTER_URL):
                if self.driver.current_url != TEST_TWITTER_URL:
                    if self.check_auth_required(username):
                        return False
                else:
                    if retries > 0:
                        self.post(account, message, picture, retries - 1)
                    else:
                        trace_account_status(account, False)
                        return False
            else:
                trace_account_status(account, False)
                return False
            
            self.driver.get("https://x.com/home")
            random_delay()
            if not self.post_tweet(message, picture):
                trace_account_status(account, False)
                return False
            
            trace_account_status(account, True)
            
            self.restart()
            return True

        except TimeoutError:
            if self.check_auth_required(username):
                return False
            # Retry the post if it fails
            if retries > 0:
                self.post(account, message, picture, retries - 1)
            else:
                trace_account_status(account, False)
                return False

        except:
            self.check_auth_required(username)
            return False

    def interact(self, account, tweet_url, retries=1):
        try:
            email = account['email']
            username = account['username']
            password = account['password']

            random_delay()
            self.driver.get("https://x.com")
            short_random_delay()

            cookies = load_cookies(username)
            if cookies:  # Load cookies if available
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                short_random_delay()
                
                if not self.verify_login(username, tweet_url=tweet_url):  # Check if cookies are valid                     
                    print(f"COOKIES EXPIRED - {username}")
                    self.restart()

                    if not self.login(email, username, password):
                        trace_account_status(account, False)
                        return False
            else:
                if not self.login(email, username, password):
                    trace_account_status(account, False)
                    return False

            # Check if it gets redirected to an authentication page
            if self.get_tweet(tweet_url):
                if self.driver.current_url != tweet_url:
                    if self.check_auth_required(username):
                        return False
                else:
                    if retries > 0:
                        self.interact(account, tweet_url, retries - 1)
                    else:
                        trace_account_status(account, False)
                        return False
            else:
                trace_account_status(account, False)
                return False
            
            # Check if there are some issues with the account
            if not self.like() or not self.repost() or not self.comment(get_random_message()) or not self.bookmark():
                if retries > 0:
                    self.interact(account, tweet_url, retries - 1)
                else:
                    trace_account_status(account, False)
                    return False
            
            trace_account_status(account, True)

            self.restart()
            return True
        
        except TimeoutError:
            if self.check_auth_required(username):
                return False
            # Retry the interaction if it fails
            if retries > 0:
                self.interact(account, tweet_url, retries - 1)
            else:
                trace_account_status(account, False)
                return False

        except:
            self.check_auth_required(username)
            trace_account_status(account, False)
            return False

    def restart(self):
        self.driver.delete_all_cookies()

    def teardown(self):
        self.driver.quit()

