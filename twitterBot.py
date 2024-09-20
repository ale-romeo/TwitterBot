from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class xActions():
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
    
    def teardown_method(self):
        self.driver.quit()
    
    def login(self):
        self.driver.get("https://x.com/i/flow/login")
        time.sleep(2)
        self.driver.find_element(By.NAME, "text").send_keys("alexhaxtv@gmail.com")
        # Wait for the "Next" button to be clickable
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
        )
        button.click()
        time.sleep(5)


        self.driver.find_element(By.NAME, "text").send_keys("ZHOAMaster")
        # Wait for the "Next" button to be clickable
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
        )
        button.click()
        time.sleep(5)


        self.driver.find_element(By.NAME, "password").send_keys("$$ZHOA$$1B")
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Log in')]"))
        )
        button.click()
        time.sleep(5)


class tgActions():
    def setup_method(self):
        self.token = '7948740096:AAHksBdIMs9h3hFM-YgIkbwvNrsZ_KgT7o0'
        self.updater = Updater(token=self.token, use_context=True)
        self.dp = self.updater.dispatcher
        self.vars = {}

    def start(self, update, context):
        update.message.reply_text('Hi! I am your Twitter Raid bot! I will monitor for Twitter links.')

    def handle_message(self, update, context):
        text = update.message.text
        twitter_link = self.extract_twitter_link(text)
        if twitter_link:
            update.message.reply_text(f'Twitter link found: {twitter_link}')
        else:
            update.message.reply_text('No Twitter link detected.')

    def extract_twitter_link(self, text):
        twitter_regex = r'https?://(www\.)?twitter\.com/[a-zA-Z0-9_]+/status/\d+'
        match = re.search(twitter_regex, text)
        if match:
            return match.group(0)
        return None
    


def main():
    x = xActions()
    x.setup_method()
    x.login()

if __name__ == '__main__':
    main()