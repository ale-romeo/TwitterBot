from anticaptchaofficial.funcaptchaproxyless import funcaptchaProxyless
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import random
import re

# Replace these values with your own
API_KEY = "aac405691061c7841c55612ed7477606"
TEST_URL = "https://www.x.com/"
PUBLIC_KEY = "2F4F0B28-BC94-4271-8AD7-A51662E3C91C"  # Arkose Labs demo public key
site_key_pattern = 'public_key: "(.+?)",'  # Regex pattern to extract site key from the page source

account = {
    "username": "HoldMyCoinsBro",
    "password": "$$ZHOA$$1B",
    "email": "holdmycoinsbro@proton.me"
}

def random_delay():
    time.sleep(random.uniform(1, 3))

def solve_funcaptcha(api_key, website_url, website_key):
    """
    Solves FunCaptcha using Anti-Captcha service.
    
    Args:
        api_key (str): Your Anti-Captcha API key.
        website_url (str): URL where the captcha is present.
        website_key (str): FunCaptcha public key from the website.

    Returns:
        str: Solution token if successful, None otherwise.
    """
    solver = funcaptchaProxyless()
    solver.set_verbose(1)  # Enable verbose mode for debugging
    solver.set_key(api_key)  # Anti-Captcha API key
    solver.set_website_url(website_url)  # URL of the captcha
    solver.set_website_key(website_key)  # FunCaptcha public key

    print("Attempting to solve FunCaptcha...")

    token = solver.solve_and_return_solution()
    if token:
        print("FunCaptcha solved successfully!")
        return token
    else:
        print(f"Failed to solve FunCaptcha. Error: {solver.error_code}")
        return None
    
def manual_funcaptcha_solver(driver):
    # Solve FunCaptcha
    solution_token = solve_funcaptcha(API_KEY, TEST_URL, PUBLIC_KEY)
    # Detect FunCaptcha iframe
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.ID, "arkoseFrame")
        )
    )
    # Detect Verification iframe
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[aria-label='Verification challenge']")
        )
    )
    # Inject the solution token into the response field
    response_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "FunCaptcha-Token"))
    )
    print(solution_token)
    time.sleep(30)
    driver.execute_script(f"arguments[0].value='{solution_token}';", response_field)
    # Detect Visual iframe
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[aria-label='Visual challenge']")
        )
    )
    # Detect Play button
    play_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
    )
    driver.execute_script("arguments[0].click();", play_button)
    random_delay()

    if solution_token:
        # Click the submit button (if required for the form)
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
        )
        driver.execute_script("arguments[0].click();", submit_button)
        print("Captcha solution submitted.")
        random_delay()
        time.sleep(30)
    else:
        print("Captcha solving failed. No solution token obtained.")
        return False
    return True

def login(driver, email, username, password, retries=3):
        try:        
            driver.get("https://x.com/i/flow/login")
            random_delay()

            textbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            textbox.send_keys(email)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            random_delay()

            try:
                try:
                    username_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "text"))
                    )
                except:
                    password_box = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "password"))
                    )
                    password_box.send_keys(password)
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
                    )
                    button.click()
                    random_delay()
                    try:
                        # Detect authentication request
                        start_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Start']"))
                        )
                        driver.execute_script("arguments[0].click();", start_button)
                        random_delay()
                        manual_funcaptcha_solver(driver)
                    except:
                        # Detect 2FA code input
                        send_email_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[value='Send email']"))
                        )
                        driver.execute_script("arguments[0].click();", send_email_button)
                        random_delay()
                        # Enter 2FA code
                        
            except:
                pass
                
            username_box.send_keys(username)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
            )
            button.click()
            random_delay()
            
            password_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_box.send_keys(password)
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
            )
            button.click()
            random_delay()
            manual_funcaptcha_solver(driver)
            return True

        except:
            # Check if arkose iframe is present
            if driver.find_elements(By.ID, "arkoseFrame"):
                print("FunCaptcha detected. Attempting to solve manually...")
                manual_funcaptcha_solver(driver)
                return True
            else:
                print("Login failed. Please check your credentials and try again.")
                return False

def main():
    # Initialize Selenium WebDriver with options
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    driver = uc.Chrome(options=chrome_options)
    driver.get("https://x.com/i/flow/login")

    try:
        login(driver, account["email"], account["username"], account["password"])

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
    