import asyncio
from threading import Lock
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils.file_handler import (
    get_random_post_text, 
    get_random_picture, 
    get_raid_picture, 
    get_accounts, 
    save_interacted_tweet, 
    check_interacted_tweet, 
    erase_logs, 
    get_logs, 
    get_quarantined_accounts, 
    move_account_to_active
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

            if twitter_url and not check_interacted_tweet(twitter_url):
                if self.token == '8149924758:AAEFdtxS1cm1JYlOtmrZd2yvnC88JcXY7ck':
                    await update.message.reply_animation(
                        animation=get_raid_picture(), 
                        caption=f"ZHOA ARMY!! IT'S TIME TO SHINE 🔥🔥\n{twitter_url}"
                    )
                # Run raid in the background with a lock
                asyncio.create_task(self.run_locked(self.raid, twitter_url))
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
            account = random.choice(get_accounts())

            await update.message.reply_text('Posting your tweet...')
            # Run post in the background with a lock
            selenium_actions = SeleniumActions()
            success = await self.run_locked(selenium_actions.post, account, message, picture)
            selenium_actions.teardown()  # Clean up after SeleniumActions
            if success:
                await update.message.reply_text('Tweet posted successfully!')
            else:
                await update.message.reply_text('Failed to post the tweet. Please check the logs.')

    async def raid(self, tweet_url):
        """Perform a raid using all available accounts."""
        erase_logs()  # Clear logs before starting a new raid
        selenium_actions = SeleniumActions()
        accounts = get_accounts()
        random.shuffle(accounts)
        raid_result = True

        async with self.lock:
            for account in accounts:
                comment = random.choice([True, False])
                interaction_result = selenium_actions.interact(account, tweet_url, comment)
                raid_result = raid_result and interaction_result
                random_delay()
            selenium_actions.tearDown()  # Clean up after SeleniumActions
        
        save_interacted_tweet(tweet_url)
        return raid_result

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
