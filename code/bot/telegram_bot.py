import asyncio
from threading import Lock
from queue import Queue
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils.file_handler import (
    get_random_post_text, 
    get_random_picture, 
    get_raid_picture, 
    get_accounts, 
    check_interacted_tweet, 
    erase_logs, 
    get_logs, 
    get_quarantined_accounts, 
    move_account_to_active,
    save_interacted_tweet
)
import random
from utils.logging_handler import log_error
from utils.helpers import extract_tweet_link, random_delay
from automation.selenium_actions import SeleniumActions

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.lock = Lock()  # Shared lock for raid and post
        self.processed_tracker = {}
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("post", self.post))
        self.application.add_handler(CommandHandler("logs", self.logs))
        self.application.add_handler(CommandHandler("quarantined", self.get_quarantined_accounts))
        self.application.add_handler(CommandHandler("move", self.move_account_to_active))
        self.application.add_handler(MessageHandler(filters.TEXT, self.monitor_group_messages))

    async def monitor_group_messages(self, update, context):
        """Monitor group messages for Twitter links."""
        try:
            if not update.message.text:
                return
            message_text = update.message.text
            twitter_url = extract_tweet_link(message_text)

            if twitter_url and not check_interacted_tweet(twitter_url) and twitter_url not in self.processed_tracker:
                if self.token == '8149924758:AAEFdtxS1cm1JYlOtmrZd2yvnC88JcXY7ck':
                    await update.message.reply_animation(
                        animation=get_raid_picture(), 
                        caption=f"ZHOA ARMY!! IT'S TIME TO SHINE 🔥🔥\n{twitter_url}"
                    )
                self.processed_tracker[twitter_url] = set()
                # Run raid in the background with a lock
                asyncio.create_task(self.run_locked(self.raid))
        except Exception as e:
            log_error(f"Error processing group message: {e}")

    async def post(self, update, context):
        """Post a tweet using a random account."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            message = (
                get_random_post_text()
                if len(update.message.text.split(' ')) < 2
                else ' '.join(update.message.text.split(' ')[1:])
            )
            picture = get_random_picture()
            accounts = get_accounts()
            if not accounts:
                log_error("No accounts available for raid.")
                return
            account = random.choice(accounts)

            await update.message.reply_text('Posting your tweet...')
            # Run post in the background with a lock
            selenium_actions = SeleniumActions(None)
            post = asyncio.create_task(self.run_locked(selenium_actions.post, account, message, picture))
            asyncio.create_task(self.wait_post_completion(post, update))

    async def wait_post_completion(self, post, update):
        """Wait for the post task to complete."""
        success = await post
        if success:
            await update.message.reply_text('Tweet posted successfully!')
        else:
            await update.message.reply_text('Failed to post the tweet. Please check the logs.')

    async def raid(self):
        erase_logs()
        accounts = get_accounts()
        if not accounts:
            log_error("No accounts available for raid.")
            return
        random.shuffle(accounts)
        selenium_actions = SeleniumActions(self.processed_tracker)
        for account in accounts:
            selenium_actions.process_account(account)
            self.remove_link_if_interacted_by_all()
            random_delay()
            

    def remove_link_if_interacted_by_all(self):
        """Check if a link in self.processed_tracker has been interacted by all accounts."""
        accounts = get_accounts()
        for link in self.processed_tracker:
            if len(self.processed_tracker[link]) == len(accounts):
                del self.processed_tracker[link]              
                save_interacted_tweet(link)

    async def logs(self, update, context):
        """Retrieve and send the latest logs."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            logs = get_logs()
            await update.message.reply_text(logs)

    async def get_quarantined_accounts(self, update, context):
        """Get and display quarantined accounts."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            quarantined_accounts = get_quarantined_accounts()
            if not quarantined_accounts:
                await update.message.reply_text('No accounts in quarantine.')
                return
            usernames = ', '.join([account['username'] for account in quarantined_accounts])
            await update.message.reply_text(usernames)

    async def move_account_to_active(self, update, context):
        """Move a quarantined account back to active."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            if len(update.message.text.split(' ')) < 2:
                await update.message.reply_text('No username provided.')
                return
            username = update.message.text.split(' ')[1]
            operation_result = move_account_to_active(username)
            if not operation_result:
                await update.message.reply_text(f"Failed to move {username} to active accounts.")
                return
            await update.message.reply_text(f"{username} moved to active accounts.")

    async def run_locked(self, func, *args):
        """Run a function with a shared lock to prevent simultaneous raids/posts."""
        if self.lock.locked():
            log_error("A raid or post is already in progress. Please wait.")
            return False  # Prevent concurrent raids/posts

        with self.lock:
            try:
                # If func is a coroutine (async function), await it
                if asyncio.iscoroutinefunction(func):
                    return await func(*args)
                # Otherwise, run it as a blocking function in a thread
                else:
                    loop = asyncio.get_running_loop()
                    return await loop.run_in_executor(None, func, *args)
            except Exception as e:
                log_error(f"Error running locked function: {e}")
                return False

    def start(self):
        """Start the Telegram bot."""
        self.application.run_polling()
