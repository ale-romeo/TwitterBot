import random
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.logging_handler import trace_account_status, log_error
from utils.file_handler import get_random_emojis, get_random_picture, get_random_message, move_account_to_quarantine, move_account_to_suspended, save_interacted_tweet
from config.settings import TEST_TWITTER_URL
from config.env import PROXY_STRING

class SeleniumActions:
    def __init__(self, link_queue, processed_tracker):
        self.tweet = None  # Store the tweet element
        self.link_queue = link_queue
        self.processed_tracker = processed_tracker


    def random_delay(self, sb):
        sb.sleep(random.uniform(1, 3))

    def safe_find_element(self, sb, by, value, timeout=10):
        try:
            return sb.wait_for_element_visible(by=by, value=value, timeout=timeout)
        except:
            return None

    def deal_auth_required(self, username):
        log_error(f"AUTH REQUIRED - {username}")
        quarantine_op = move_account_to_quarantine(username)
        if not quarantine_op:
            log_error(f"NOT FOUND - {username}")
        return True

    def check_auth_required(self, sb, username):
        try:
            # Check if redirected to access page
            if sb.get_current_url() == "https://x.com/account/access":
                self.deal_auth_required(username)
                return True

            # Check for Arkose iframe (common for FunCaptcha)
            if sb.is_element_present("iframe#arkose_iframe"):
                sb.switch_to_frame("arkose_iframe")
                self.deal_auth_required(username)
                return True

            # Check for ArkoseFrame
            if sb.is_element_present("iframe#arkoseFrame"):
                sb.switch_to_frame("arkoseFrame")
                self.deal_auth_required(username)
                return True

            # Check for submit button
            if sb.is_element_present("input[type='submit']"):
                self.deal_auth_required(username)
                return True

            # Check for email button
            if sb.is_element_present("button:contains('email')"):
                self.deal_auth_required(username)
                return True

            # Check for "Try again" link
            if sb.is_element_present("//a[contains(text(), 'Try again')]", by=By.XPATH):
                self.deal_auth_required(username)
                return True

        except Exception as e:
            log_error(f"Error checking auth required: {e}")
            return False

        return False

    def login(self, sb, email, username, password):
        try:
            # Navigate to Twitter login page
            sb.open("https://x.com/i/flow/login")
            self.random_delay(sb)

            # Enter email and proceed
            if sb.is_element_present("input[name='text']"):
                sb.type("input[name='text']", email)
                sb.click("//span[contains(text(), 'Next')]", by=By.XPATH)
                self.random_delay(sb)
            else:
                log_error("Email input field not found.")
                return False

            # Handle username or password input
            if sb.is_element_present("input[name='text']"):
                sb.type("input[name='text']", username)
                sb.click("//span[contains(text(), 'Next')]", by=By.XPATH)
                self.random_delay(sb)

            if sb.is_element_present("input[name='password']"):
                sb.type("input[name='password']", password)
                sb.click("//span[contains(text(), 'Log in')]", by=By.XPATH)
                self.random_delay(sb)
                sb.save_cookies(username)
                return True

            # If neither username nor password worked, deal with auth-required flow
            self.check_auth_required(username)
            return False

        except:
            return False
        
    def check_suspended(self, sb, username):
        try:
            if sb.is_text_visible("Your account is suspended", "span"):
                log_error(f"SUSPENDED - {username}")
                move_account_to_suspended(username)
                return True
            return False
        except Exception as e:
            log_error(f"Error checking suspension for {username}: {e}")
            return False

    def verify_login(self, sb, username, tweet_url):
        try:
            self.random_delay(sb)
            sb.open(tweet_url)

            # Check if the "login" element is present
            if sb.is_element_visible('[data-testid="login"]', timeout=10):
                log_error(f"COOKIES FAILED - {username}")
                sb.sleep(1)
                return False
            return True
        except:
            return False

    def post_tweet(self, sb, message, picture):
        try:
            self.random_delay(sb)
            tweet_box_selector = "[data-testid='tweetTextarea_0']"
            
            # Type the tweet message
            if sb.is_element_visible(tweet_box_selector, timeout=10):
                sb.type(tweet_box_selector, message)
            else:
                return False

            self.random_delay(sb)
            self.add_emojis(get_random_emojis())

            self.random_delay(sb)
            self.send_picture(sb, picture)

            self.random_delay(sb)

            # Submit the tweet
            submit_button_selector = "[data-testid='tweetButtonInline']"
            if sb.is_element_visible(submit_button_selector, timeout=10):
                sb.click(submit_button_selector)
                self.random_delay(sb)
                return True
            else:
                return False

        except:
            return False

    def get_tweet(self, sb, tweet_url):
        try:
            sb.open(tweet_url)
            self.random_delay(sb)

            tweet_selector_with_tabindex = "//article[@data-testid='tweet'][@tabindex='-1']"
            tweet_selector = "//article[@data-testid='tweet']"

            # Try to find the tweet with tabindex="-1"
            if sb.is_element_present(tweet_selector_with_tabindex, timeout=10):
                self.tweet = sb.find_element(tweet_selector_with_tabindex)
                self.random_delay(sb)
                return True

            # Fall back to finding the tweet without tabindex
            elif sb.is_element_present(tweet_selector, timeout=10):
                self.tweet = sb.find_element(tweet_selector)
                self.random_delay(sb)
                return True
            else:
                return False

        except:
            return False

    def like(self, sb):
        try:
            # Check if the tweet is already liked
            unlike_button = sb.safe_find_element(By.CSS_SELECTOR, "[data-testid='unlike']")
            if unlike_button:
                sb.sleep(0.5)  # Optional small delay for natural behavior
                return True  # Already liked

            # Attempt to like the tweet
            like_button = sb.safe_find_element(By.CSS_SELECTOR, "[data-testid='like']")
            if like_button:
                sb.execute_script("arguments[0].click();", like_button)
                sb.sleep(1)
                return True  # Like successful

        except:
            return False

    def repost(self, sb):
        try:
            # Check if already reposted
            try:
                if sb.is_element_visible('[data-testid="unretweet"]'):
                    sb.sleep(0.5)  # Optional short delay for realism
                    return True
            except:
                pass  # If unretweet button is not present, proceed to retweet

            # Retweet the post
            if sb.is_element_visible('[data-testid="retweet"]'):
                sb.click('[data-testid="retweet"]')
                sb.sleep(0.5)

                # Confirm the retweet
                sb.wait_for_element_visible('[data-testid="retweetConfirm"]', timeout=10)
                sb.click('[data-testid="retweetConfirm"]')
                sb.sleep(1)  # Delay for confirmation realism

                return True
            return False  # Retweet button not found

        except:
            return False

    def send_picture(self, sb, picture):
        try:
            # Locate the photo input element
            if sb.is_element_visible("[data-testid='fileInput']"):
                sb.find_element("[data-testid='fileInput']").send_keys(picture)
                sb.sleep(1)  # Slight delay for realism
                return True
            return False  # File input not found
        except:
            return False

    def add_emojis(self, sb, emojis):
        try:
            # Click the emoji button
            if sb.is_element_visible("[aria-label='Add emoji']"):
                sb.click("[aria-label='Add emoji']")
                sb.sleep(0.5)

                for emoji in emojis:
                    # Search for the emoji
                    sb.wait_for_element_visible("[aria-label='Search emojis']", timeout=10)
                    sb.type("[aria-label='Search emojis']", emoji)
                    sb.sleep(0.5)  # Small delay for realism

                    # Select the emoji
                    emoji_button_selector = f"[aria-label='{emoji}']"
                    if sb.is_element_visible(emoji_button_selector):
                        sb.click(emoji_button_selector)
                        sb.sleep(0.5)

                    # Clear the search bar
                    if sb.is_element_visible("[data-testid='clearButton']"):
                        sb.click("[data-testid='clearButton']")
                        sb.sleep(0.5)

                # Close the emoji picker (optional)
                sb.press_keys("[aria-label='Search emojis']", Keys.ESCAPE)
                sb.sleep(1)
                return True
            return False  # Emoji button not found
        except:
            return False

    def comment(self, sb, message):
        try:
            # Click the reply button
            if sb.is_element_visible("[data-testid='reply']"):
                sb.click("[data-testid='reply']")
                sb.sleep(1)  # Slight delay for realism

                # Randomly choose comment type
                comment_type = random.choices(['text', 'picture', 'text_picture', 'emojis'], weights=[0.1, 0.05, 0.8, 0.05])[0]

                if comment_type == 'text':
                    # Type text and add emojis
                    if sb.is_element_visible("[data-testid='tweetTextarea_0']"):
                        sb.type("[data-testid='tweetTextarea_0']", message)
                        self.add_emojis(sb, get_random_emojis())

                elif comment_type == 'picture':
                    # Attach a picture
                    picture = get_random_picture()
                    self.send_picture(sb, picture)

                elif comment_type == 'text_picture':
                    # Type text, add emojis, and attach a picture
                    if self.is_element_visible("[data-testid='tweetTextarea_0']"):
                        sb.type("[data-testid='tweetTextarea_0']", message)
                        self.add_emojis(sb, get_random_emojis())
                    picture = get_random_picture()
                    self.send_picture(sb, picture)

                elif comment_type == 'emojis':
                    # Add only emojis
                    self.add_emojis(sb, get_random_emojis())

                # Click the submit button
                if sb.is_element_visible("[data-testid='tweetButton']"):
                    sb.click("[data-testid='tweetButton']")
                    sb.sleep(2)  # Pause for completion

                return True
            return False  # Reply button not found
        except:
            return False

    def bookmark(self, sb):
        try:
            # Check if already bookmarked
            if sb.is_element_visible("[data-testid='unbookmark']"):
                sb.sleep(1)  # Short delay for realism
                return True  # Already bookmarked
            
            # Bookmark the tweet
            if sb.is_element_visible("[data-testid='bookmark']"):
                sb.click("[data-testid='bookmark']")
                sb.sleep(1)  # Slight delay after clicking
                return True
            
            return False  # Bookmark element not found
        except:
            return False
        
    def post(self, account, message, picture):
        try:
            email = account['email']
            username = account['username']
            password = account['password']
            with SB(
                uc=True,  # Enable undetected-chromedriver mode
                headless=False,  # Optional: Set True for headless mode
                incognito=True,  # Enable incognito mode for stealth
                proxy=PROXY_STRING,  # Assign proxy if needed
                window_size="800,800"  # Set window size for the browser
            ) as sb:
                # Open the website and clear cookies for a fresh start
                sb.uc_open("https://x.com")
                self.random_delay(sb)
                
                if sb.load_cookies(username):  # Load cookies if available
                    self.random_delay(sb)
                    
                    if not self.verify_login(sb, username, TEST_TWITTER_URL):  # Validate cookies
                        log_error(f"COOKIES EXPIRED - {username}", level="WARNING")
                        sb.delete_all_cookies()
                        sb.sleep(1)

                        if not self.login(sb, email, username, password):
                            trace_account_status(account, False)
                            return False
                else:
                    # Perform login if no cookies are available
                    if not self.login(sb, email, username, password):
                        trace_account_status(account, False)
                        return False

                # Check for redirection to an authentication page
                sb.open(TEST_TWITTER_URL)
                self.random_delay(sb)
                if sb.get_current_url() != TEST_TWITTER_URL:
                    if self.check_auth_required(sb, username):
                        return False
                    else:
                        sb.delete_all_cookies()
                        return False

                # Navigate to home and attempt to post the tweet
                sb.open("https://x.com/home")
                self.random_delay(sb)
                if not self.post_tweet(sb, message, picture):
                    trace_account_status(account, False)
                    return False

                # Mark success
                trace_account_status(account, True)
                sb.delete_all_cookies()  # Clean up session
                return True

        except:
            trace_account_status(account, False)
            sb.delete_all_cookies()
            return False

    def interact(self, sb, account, tweet_url, comment=True):
        # Navigate to the tweet URL
        sb.open(tweet_url)
        self.random_delay(sb)

        # Check for redirection to an authentication page
        if sb.get_current_url() != tweet_url:
            if self.check_auth_required(sb, account['username']):
                return False

        # Perform interactions (like, repost, comment, bookmark)
        interaction_success = (
            self.like(sb) and 
            self.repost(sb) and 
            self.bookmark(sb)
        )

        if comment:
            interaction_success = interaction_success and self.comment(sb, get_random_message())

        if not interaction_success:
            trace_account_status(account, False)
            return False

        # Mark account interaction as successful
        trace_account_status(account, True)

        # Clean up session
        sb.delete_all_cookies()
        return True

    def process_account(self, account):
        try:
            email = account['email']
            username = account['username']
            password = account['password']
            with SB(
                uc=True,  # Enable undetected-chromedriver mode
                headless=False,  # Optional: Set True for headless mode
                incognito=True,  # Enable incognito mode for stealth
                proxy=PROXY_STRING,  # Assign proxy if needed
                window_size="800,800"  # Set window size for the browser
            ) as sb:
                # Open X.com and clear session for a fresh start
                sb.open("https://x.com")
                sb.sleep(1)

                # Load cookies if available
                if sb.load_cookies(username):
                    self.random_delay(sb)

                    # Verify login status with the cookies
                    if not self.verify_login(username, TEST_TWITTER_URL):
                        log_error(f"COOKIES EXPIRED - {username}", level="WARNING")
                        sb.delete_all_cookies()
                        sb.sleep(1)

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

                for link in list(self.link_queue.queue):
                    if username in self.processed_tracker[link]:
                        continue

                    success = self.interact(account, link, comment=random.choice([True, False]))
            
                    if success:
                        self.processed_tracker[link].add(username)
                        if len(self.processed_tracker[link]) == len(self.link_queue):
                            self.link_queue.get()
                            del self.processed_tracker[link]
                            save_interacted_tweet(link)
                
                return True

        except:
            trace_account_status(account, False)
            return False
