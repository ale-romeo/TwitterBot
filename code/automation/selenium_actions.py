import random
import pyperclip
from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.logging_handler import trace_account_status, log_error
from utils.file_handler import get_random_emojis, get_random_picture, get_random_message, move_account_to_quarantine, move_account_to_suspended, save_interacted_tweet
from config.settings import TEST_TWITTER_URL
#from config.env import PROXY_STRING

class SeleniumActions:
    def __init__(self, link_queue, processed_tracker):
        self.tweet = None  # Store the tweet element
        self.link_queue = link_queue
        self.processed_tracker = processed_tracker


    def random_delay(self, sb):
        sb.sleep(random.uniform(1, 3))

    def safe_find_element(self, sb, selector, timeout=10):
        try:
            return sb.wait_for_element_visible(selector, timeout=timeout)
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
            input_selector = "input[name='text']"
            password_selector = "input[name='password']"
            next_button_selector = "//span[contains(text(), 'Next')]"

            # Enter email and proceed
            try:
                sb.update_text(input_selector, email, timeout=10, retry=1)
                sb.click(next_button_selector, by=By.XPATH)
                self.random_delay(sb)
            except:
                return False

            # Handle username or password input
            try:
                sb.update_text(input_selector, username, timeout=10, retry=1)
                sb.click(next_button_selector, by=By.XPATH)
                self.random_delay(sb)
            except:
                pass

            try:
                sb.update_text(password_selector, password, timeout=10, retry=1)
                sb.click("//span[contains(text(), 'Log in')]", by=By.XPATH)
                self.random_delay(sb)
                sb.save_cookies(username)
                return True
            except:
                self.check_suspended(sb, username)
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
            try:
                sb.assert_element("[data-testid='login']", timeout=5)
                log_error(f"COOKIES FAILED - {username}")
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

        # Submit the tweet
        try:
            sb.click(submit_button_selector, timeout=10, delay=1)
            self.random_delay(sb)
            return True
        except:
            return False

    def get_tweet(self, sb, tweet_url):
        try:
            sb.open(tweet_url)
            self.random_delay(sb)

            tweet_selector_with_tabindex = "//article[@data-testid='tweet'][@tabindex='-1']"
            tweet_selector = "//article[@data-testid='tweet']"

            # Try to find the tweet with tabindex="-1"
            try:
                self.tweet = sb.find_element(tweet_selector_with_tabindex)
                self.random_delay(sb)
                return True
            except:
                pass

            # Fall back to finding the tweet without tabindex
            try:
                self.tweet = sb.find_element(tweet_selector)
                self.random_delay(sb)
                return True
            except:
                return False

        except:
            return False

    def like(self, sb):
        try:
            unlike_selector = "[data-testid='unlike']"
            like_selector = "[data-testid='like']"
            # Check if the tweet is already liked
            try:
                sb.assert_element(unlike_selector, timeout=5)
                return True  # Already liked
            except:
                pass

            try:
                sb.click(like_selector, timeout=5, delay=1)
                sb.sleep(0.5)  # Optional small delay for realism
                return True
            except:
                return False

        except:
            return False

    def repost(self, sb):
        try:
            unretweet_selector = "[data-testid='unretweet']"
            retweet_selector = "[data-testid='retweet']"
            retweet_confirm_selector = "[data-testid='retweetConfirm']"
            # Check if already reposted
            try:
                sb.assert_element(unretweet_selector, timeout=5)
                return True
            except:
                pass  # If unretweet button is not present, proceed to retweet

            try:
                sb.click(retweet_selector, timeout=5, delay=1)
                sb.sleep(0.5)  # Optional small delay for realism
                try:
                    sb.click(retweet_confirm_selector, timeout=5, delay=1)
                    sb.sleep(1)  # Delay for confirmation realism
                    return True
                except:
                    return False
            except:
                return False

        except:
            return False

    def send_picture(self, sb, picture):
        # Locate and upload the picture using the file input element
        file_input_selector = "[data-testid='fileInput']"
        try:
            file_input = sb.find_element(file_input_selector)
            file_input.send_keys(picture)
            return True  # Picture upload successful
        except:
            return False  # File input element not found
     
    def add_emojis(self, sb, text_box, emojis):
        try:
            for emoji in emojis:
                # Copy the emoji to the clipboard
                if emoji == 'Clapping hands sign':
                    pyperclip.copy("👏")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Crown':
                    pyperclip.copy("👑")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Sparkles':
                    pyperclip.copy("✨")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Rocket':
                    pyperclip.copy("🚀")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Full moon symbol':
                    pyperclip.copy("🌕")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Fire':
                    pyperclip.copy("🔥")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Money bag':
                    pyperclip.copy("💰")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Gem stone':
                    pyperclip.copy("💎")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
                elif emoji == 'Small orange diamond':
                    pyperclip.copy("🔸")
                    sb.send_keys(text_box, Keys.CONTROL + 'v', timeout=5)
                    sb.sleep(1)  # Delay for realism
            return True
        except:
            return False
    '''
    def add_emojis(self, sb, emojis):
        # Click the "Add emoji" button
        emoji_button_selector = "[aria-label='Add emoji']"
        emoji_search_selector = "[aria-label='Search emojis']"
        clear_button_selector = "[data-testid='clearButton']"
        try:
            sb.click(emoji_button_selector, timeout=10)
            sb.sleep(0.5)
            sb.wait_for_element_visible(emoji_search_selector, timeout=10)

            for emoji in emojis:
                emoji_button_selector = f"[aria-label='{emoji}']"
                # Type the emoji name in the search bar
                try:
                    # Use JavaScript to type the emoji name in the search bar input
                    sb.execute_script("arguments[0].value = arguments[1];", emoji_search_selector, emoji)
                    sb.sleep(0.5)  # Wait for results to load

                    # Select the emoji from the search results
                    try:
                        sb.click(emoji_button_selector, timeout=10, delay=1)
                        sb.sleep(0.5)
                        try:
                            sb.click(clear_button_selector, timeout=10, delay=1)
                            sb.sleep(0.5)  # Delay for realism
                        except:
                            continue
                    except:
                        continue
                except:
                    continue

            # Close the emoji picker
            sb.press_keys(emoji_search_selector, Keys.ESCAPE, timeout=5)
            sb.sleep(1)  # Delay for realism
            return True
        except:
            return False
    ''' 
    def comment(self, sb, message):
        # Click the reply button
        reply_button_selector = "[data-testid='reply']"
        textarea_selector = "[data-testid='tweetTextarea_0']"
        submit_button_selector = "[data-testid='tweetButton']"
        try:
            sb.click(reply_button_selector, timeout=10, delay=1)
            sb.sleep(1)  # Slight delay for realism
        except:
            return False
        
        # Randomly choose comment type
        comment_type = random.choices(
            ['text', 'picture', 'text_picture', 'emojis'],
            weights=[0.1, 0.05, 0.8, 0.05]
        )[0]

        # Comment logic based on the type
        if comment_type in ['text', 'text_picture']:
            try:
                sb.update_text(textarea_selector, message, timeout=10, retry=1)
                if comment_type == 'text_picture' or comment_type == 'text':
                    self.add_emojis(sb, get_random_emojis())
                sb.sleep(1)  # Pause for realism
            except:
                return False

        if comment_type in ['picture', 'text_picture']:
            try:
                # Attach a picture
                picture = get_random_picture()
                self.send_picture(sb, picture)
            except:
                return False

        if comment_type == 'emojis':
            try:
                # Add only emojis
                self.add_emojis(sb, get_random_emojis())
            except:
                return False

        # Submit the comment
        try:
            sb.click(submit_button_selector, timeout=10, delay=1)
            sb.sleep(2)  # Pause for completion
            return True
        except:
            return False

    def bookmark(self, sb):
        try:
            unbookmark_selector = "[data-testid='unbookmark']"
            bookmark_selector = "[data-testid='bookmark']"
            # Selector for the "unbookmark" button
            try:
                sb.assert_element(unbookmark_selector, timeout=10)
                return True  # Tweet is already bookmarked
            except:
                pass

            # Selector for the "bookmark" button
            try:
                sb.click(bookmark_selector, timeout=10, delay=1)
                sb.sleep(1)  # Slight delay after clicking
                return True  # Bookmark operation successful
            except:
                return False
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
                #proxy=PROXY_STRING,  # Assign proxy if needed
                window_size="800,800"  # Set window size for the browser
            ) as sb:
                # Open the website and clear cookies for a fresh start
                sb.uc_open("https://x.com")
                self.random_delay(sb)
                
                if sb.load_cookies(username, -1):  # Load cookies if available
                    self.random_delay(sb)
                    
                    if not self.verify_login(sb, username, TEST_TWITTER_URL):  # Validate cookies
                        sb.delete_all_cookies()  # Attempt to clear cookies
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
                #proxy=PROXY_STRING,  # Assign proxy if needed
                window_size="800,800"  # Set window size for the browser
            ) as sb:
                # Open X.com and clear session for a fresh start
                sb.open("https://x.com")
                sb.sleep(1)

                # Load cookies if available
                if sb.load_cookies(name=username):
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
