import random
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.logging_handler import trace_account_status, log_error
from utils.file_handler import get_random_emojis, get_random_picture, get_random_message, move_account_to_quarantine, move_account_to_suspended
from config.settings import TEST_TWITTER_URL
from config.env import PROXY_STRING


class SeleniumActions:
    def __init__(self):
        # Initialization
        self.uc = True  # Enable undetected-chromedriver mode
        self.headless = False  # Optional: Set True for headless mode
        self.incognito = True  # Enable incognito mode for stealth
        self.start_page_load_timeout = 20  # Set page load timeout
        self.proxy = PROXY_STRING  # Assign proxy if needed
        self.tweet = None  # Store the tweet element
        self.driver = SB(uc=self.uc, headless=self.headless, incognito=self.incognito, proxy=self.proxy, start_page_load_timeout=self.start_page_load_timeout)

    def teardown(self):
        self.driver.quit()

    def random_delay(self):
        self.driver.sleep(random.uniform(1, 3))

    def safe_find_element(self, by, value, timeout=10):
        try:
            return self.driver.wait_for_element_visible(by=by, value=value, timeout=timeout)
        except:
            return None

    def deal_auth_required(self, username):
        log_error(f"AUTH REQUIRED - {username}")
        quarantine_op = move_account_to_quarantine(username)
        if not quarantine_op:
            log_error(f"NOT FOUND - {username}")
        return True

    def check_auth_required(self, username):
        try:
            # Check if redirected to access page
            if self.driver.get_current_url() == "https://x.com/account/access":
                self.deal_auth_required(username)
                return True

            # Check for Arkose iframe (common for FunCaptcha)
            if self.driver.is_element_present("iframe#arkose_iframe"):
                self.driver.switch_to_frame("arkose_iframe")
                self.deal_auth_required(username)
                return True

            # Check for ArkoseFrame
            if self.driver.is_element_present("iframe#arkoseFrame"):
                self.driver.switch_to_frame("arkoseFrame")
                self.deal_auth_required(username)
                return True

            # Check for submit button
            if self.driver.is_element_present("input[type='submit']"):
                self.deal_auth_required(username)
                return True

            # Check for email button
            if self.driver.is_element_present("button:contains('email')"):
                self.deal_auth_required(username)
                return True

            # Check for "Try again" link
            if self.driver.is_element_present("//a[contains(text(), 'Try again')]", by=By.XPATH):
                self.deal_auth_required(username)
                return True

        except Exception as e:
            log_error(f"Error checking auth required: {e}")
            return False

        return False

    def login(self, email, username, password):
        try:
            # Navigate to Twitter login page
            self.driver.open("https://x.com/i/flow/login")
            self.random_delay()

            # Enter email and proceed
            if self.is_element_present("input[name='text']"):
                self.driver.type("input[name='text']", email)
                self.driver.click("//span[contains(text(), 'Next')]", by=By.XPATH)
                self.random_delay()
            else:
                log_error("Email input field not found.")
                return False

            # Handle username or password input
            if self.driver.is_element_present("input[name='text']"):
                self.driver.type("input[name='text']", username)
                self.driver.click("//span[contains(text(), 'Next')]", by=By.XPATH)
                self.random_delay()

            if self.driver.is_element_present("input[name='password']"):
                self.driver.type("input[name='password']", password)
                self.driver.click("//span[contains(text(), 'Log in')]", by=By.XPATH)
                self.random_delay()
                self.driver.save_cookies(username)
                return True

            # If neither username nor password worked, deal with auth-required flow
            self.check_auth_required(username)
            return False

        except:
            return False
        
    def check_suspended(self, username):
        try:
            if self.driver.is_text_visible("Your account is suspended", "span"):
                log_error(f"SUSPENDED - {username}")
                move_account_to_suspended(username)
                return True
            return False
        except Exception as e:
            log_error(f"Error checking suspension for {username}: {e}")
            return False

    def verify_login(self, username, tweet_url):
        try:
            self.random_delay()
            self.driver.open(tweet_url)

            # Check if the "login" element is present
            if self.driver.is_element_visible('[data-testid="login"]', timeout=10):
                log_error(f"COOKIES FAILED - {username}")
                self.driver.sleep(1)
                return False
            return True
        except:
            return False

    def post_tweet(self, message, picture):
        try:
            self.random_delay()
            tweet_box_selector = "[data-testid='tweetTextarea_0']"
            
            # Type the tweet message
            if self.driver.is_element_visible(tweet_box_selector, timeout=10):
                self.driver.type(tweet_box_selector, message)
            else:
                return False

            self.random_delay()
            self.add_emojis(get_random_emojis())

            self.random_delay()
            self.send_picture(picture)

            self.random_delay()

            # Submit the tweet
            submit_button_selector = "[data-testid='tweetButtonInline']"
            if self.driver.is_element_visible(submit_button_selector, timeout=10):
                self.driver.click(submit_button_selector)
                self.random_delay()
                return True
            else:
                return False

        except:
            return False

    def get_tweet(self, tweet_url):
        try:
            self.driver.open(tweet_url)
            self.random_delay()

            tweet_selector_with_tabindex = "//article[@data-testid='tweet'][@tabindex='-1']"
            tweet_selector = "//article[@data-testid='tweet']"

            # Try to find the tweet with tabindex="-1"
            if self.driver.is_element_present(tweet_selector_with_tabindex, timeout=10):
                self.tweet = self.driver.find_element(tweet_selector_with_tabindex)
                self.random_delay()
                return True

            # Fall back to finding the tweet without tabindex
            elif self.driver.is_element_present(tweet_selector, timeout=10):
                self.tweet = self.driver.find_element(tweet_selector)
                self.random_delay()
                return True
            else:
                return False

        except:
            return False

    def like(self):
        try:
            # Check if the tweet is already liked
            unlike_button = self.driver.safe_find_element(By.CSS_SELECTOR, "[data-testid='unlike']")
            if unlike_button:
                self.driver.sleep(0.5)  # Optional small delay for natural behavior
                return True  # Already liked

            # Attempt to like the tweet
            like_button = self.driver.safe_find_element(By.CSS_SELECTOR, "[data-testid='like']")
            if like_button:
                self.driver.execute_script("arguments[0].click();", like_button)
                self.driver.sleep(1)
                return True  # Like successful

        except:
            return False

    def repost(self):
        try:
            # Check if already reposted
            try:
                if self.driver.is_element_visible('[data-testid="unretweet"]'):
                    self.driver.sleep(0.5)  # Optional short delay for realism
                    return True
            except:
                pass  # If unretweet button is not present, proceed to retweet

            # Retweet the post
            if self.driver.is_element_visible('[data-testid="retweet"]'):
                self.driver.click('[data-testid="retweet"]')
                self.driver.sleep(0.5)

                # Confirm the retweet
                self.driver.wait_for_element_visible('[data-testid="retweetConfirm"]', timeout=10)
                self.driver.click('[data-testid="retweetConfirm"]')
                self.driver.sleep(1)  # Delay for confirmation realism

                return True
            return False  # Retweet button not found

        except:
            return False

    def send_picture(self, picture):
        try:
            # Locate the photo input element
            if self.driver.is_element_visible("[data-testid='fileInput']"):
                self.driver.find_element("[data-testid='fileInput']").send_keys(picture)
                self.driver.sleep(1)  # Slight delay for realism
                return True
            return False  # File input not found
        except:
            return False

    def add_emojis(self, emojis):
        try:
            # Click the emoji button
            if self.driver.is_element_visible("[aria-label='Add emoji']"):
                self.driver.click("[aria-label='Add emoji']")
                self.driver.sleep(0.5)

                for emoji in emojis:
                    # Search for the emoji
                    self.driver.wait_for_element_visible("[aria-label='Search emojis']", timeout=10)
                    self.driver.type("[aria-label='Search emojis']", emoji)
                    self.driver.sleep(0.5)  # Small delay for realism

                    # Select the emoji
                    emoji_button_selector = f"[aria-label='{emoji}']"
                    if self.driver.is_element_visible(emoji_button_selector):
                        self.driver.click(emoji_button_selector)
                        self.driver.sleep(0.5)

                    # Clear the search bar
                    if self.driver.is_element_visible("[data-testid='clearButton']"):
                        self.driver.click("[data-testid='clearButton']")
                        self.driver.sleep(0.5)

                # Close the emoji picker (optional)
                self.driver.press_keys("[aria-label='Search emojis']", Keys.ESCAPE)
                self.driver.sleep(1)
                return True
            return False  # Emoji button not found
        except:
            return False

    def comment(self, message):
        try:
            # Click the reply button
            if self.driver.is_element_visible("[data-testid='reply']"):
                self.driver.click("[data-testid='reply']")
                self.driver.sleep(1)  # Slight delay for realism

                # Randomly choose comment type
                comment_type = random.choices(['text', 'picture', 'text_picture', 'emojis'], weights=[0.1, 0.05, 0.8, 0.05])[0]

                if comment_type == 'text':
                    # Type text and add emojis
                    if self.driver.is_element_visible("[data-testid='tweetTextarea_0']"):
                        self.driver.type("[data-testid='tweetTextarea_0']", message)
                        self.add_emojis(get_random_emojis())

                elif comment_type == 'picture':
                    # Attach a picture
                    picture = get_random_picture()
                    self.send_picture(picture)

                elif comment_type == 'text_picture':
                    # Type text, add emojis, and attach a picture
                    if self.is_element_visible("[data-testid='tweetTextarea_0']"):
                        self.driver.type("[data-testid='tweetTextarea_0']", message)
                        self.add_emojis(get_random_emojis())
                    picture = get_random_picture()
                    self.send_picture(picture)

                elif comment_type == 'emojis':
                    # Add only emojis
                    self.add_emojis(get_random_emojis())

                # Click the submit button
                if self.driver.is_element_visible("[data-testid='tweetButton']"):
                    self.driver.click("[data-testid='tweetButton']")
                    self.driver.sleep(2)  # Pause for completion

                return True
            return False  # Reply button not found
        except:
            return False

    def bookmark(self):
        try:
            # Check if already bookmarked
            if self.driver.is_element_visible("[data-testid='unbookmark']"):
                self.driver.sleep(1)  # Short delay for realism
                return True  # Already bookmarked
            
            # Bookmark the tweet
            if self.driver.is_element_visible("[data-testid='bookmark']"):
                self.driver.click("[data-testid='bookmark']")
                self.driver.sleep(1)  # Slight delay after clicking
                return True
            
            return False  # Bookmark element not found
        except:
            return False
        
    def post(self, account, message, picture):
        try:
            email = account['email']
            username = account['username']
            password = account['password']

            # Open the website and clear cookies for a fresh start
            self.driver.open("https://x.com")
            self.driver.sleep(1)

            if self.driver.load_cookies(username):  # Load cookies if available
                self.random_delay()
                
                if not self.verify_login(username, TEST_TWITTER_URL):  # Validate cookies
                    log_error(f"COOKIES EXPIRED - {username}", level="WARNING")
                    self.driver.delete_all_cookies()
                    self.driver.sleep(1)

                    if not self.login(email, username, password):
                        trace_account_status(account, False)
                        return False
            else:
                # Perform login if no cookies are available
                if not self.login(email, username, password):
                    trace_account_status(account, False)
                    return False

            # Check for redirection to an authentication page
            self.driver.open(TEST_TWITTER_URL)
            self.random_delay()
            if self.driver.get_current_url() != TEST_TWITTER_URL:
                if self.check_auth_required(username):
                    return False
                else:
                    self.driver.delete_all_cookies()
                    return False

            # Navigate to home and attempt to post the tweet
            self.driver.open("https://x.com/home")
            self.random_delay()
            if not self.post_tweet(message, picture):
                trace_account_status(account, False)
                return False

            # Mark success
            trace_account_status(account, True)
            self.driver.delete_all_cookies()  # Clean up session
            return True

        except:
            trace_account_status(account, False)
            self.driver.delete_all_cookies()
            return False


    def interact(self, account, tweet_url):
        try:
            email = account['email']
            username = account['username']
            password = account['password']

            # Open X.com and clear session for a fresh start
            self.driver.open("https://x.com")
            self.driver.sleep(1)

            # Load cookies if available
            if self.driver.load_cookies(username):
                self.random_delay()

                # Verify login status with the cookies
                if not self.verify_login(username, tweet_url=tweet_url):
                    log_error(f"COOKIES EXPIRED - {username}", level="WARNING")
                    self.delete_all_cookies()
                    self.driver.sleep(1)

                    if not self.login(email, username, password):
                        trace_account_status(account, False)
                        return False
            else:
                # Perform login if no cookies are found
                if not self.login(email, username, password):
                    trace_account_status(account, False)
                    return False

            # Check if the account is suspended
            if self.check_suspended(username):
                trace_account_status(account, False)
                return False

            # Navigate to the tweet URL
            self.driver.open(tweet_url)
            self.random_delay()

            # Check for redirection to an authentication page
            if self.driver.get_current_url() != tweet_url:
                if self.check_auth_required(username):
                    return False

            # Perform interactions (like, repost, comment, bookmark)
            interaction_success = (
                self.like() and 
                self.repost() and 
                self.comment(get_random_message()) and 
                self.bookmark()
            )

            if not interaction_success:
                trace_account_status(account, False)
                return False

            # Mark account interaction as successful
            trace_account_status(account, True)

            # Clean up session
            self.driver.delete_all_cookies()
            return True

        except:
            self.driver.delete_all_cookies()
            trace_account_status(account, False)
            return False


