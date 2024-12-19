import asyncio
from threading import Lock
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils.file_handler import (
    get_project_raid_message,
    get_random_post_text, 
    get_random_picture, 
    get_raid_picture,
    get_proxy,
    get_accounts, 
    check_interacted_tweet, 
    erase_logs, 
    get_logs, 
    get_locked_accounts,
    get_suspended_accounts,
    unlock_account,
    save_interacted_tweet,
    remove_interacted_tweets
)
import random
from utils.logging_handler import log_error
from utils.helpers import extract_tweet_link, random_delay
from automation.selenium_actions import SeleniumActions

class TelegramBot:
    def __init__(self, token, vps, project):
        self.token = token
        self.vps = vps
        self.project = project
        self.proxy = get_proxy(project=project, vps=vps)
        self.raid_running = False
        self.application = Application.builder().token(token).build()
        self.queue = asyncio.Queue()
        self.task_running = False 
        self.processed_tracker = {}
        asyncio.get_event_loop().create_task(self.task_worker())
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("post", self.post))
        self.application.add_handler(CommandHandler("logs", self.logs))
        self.application.add_handler(CommandHandler("locked", self.get_locked_accounts))
        self.application.add_handler(CommandHandler("suspended", self.get_suspended_accounts))
        self.application.add_handler(CommandHandler("unlock", self.unlock_account))
        self.application.add_handler(CommandHandler("clear_logs", self.clear_logs))
        self.application.add_handler(CommandHandler("remove_link", self.remove_link_from_interacted))
        self.application.add_handler(CommandHandler("empty_tracker", self.empty_processed_tracker))
        self.application.add_handler(MessageHandler(filters.TEXT, self.monitor_group_messages))

    async def task_worker(self):
        """Background worker to process raid/post tasks sequentially."""
        while True:
            task, args = await self.queue.get()
            try:
                await task(*args)  # Execute the function
            except Exception as e:
                log_error(f"Error processing task: {e}")
            finally:
                self.task_running = False
                self.queue.task_done()

    async def monitor_group_messages(self, update, context):
        """Monitor group messages for Twitter links."""
        try:
            if update.message is None or not update.message.text:
                return
            message_text = update.message.text
            twitter_url = extract_tweet_link(message_text)

            if twitter_url and not check_interacted_tweet(twitter_url) and twitter_url not in self.processed_tracker.keys():
                if self.vps == 1:
                    await update.message.reply_animation(
                        animation=get_raid_picture(), 
                        caption=f"{get_project_raid_message}{twitter_url}"
                    )
                self.processed_tracker[twitter_url] = set()
                
                if self.raid_running:
                    return
                else:
                    self.raid_running = True
                    await self.queue.put((self.raid, ()))
        except Exception as e:
            log_error(f"Error processing group message: {e}")

    async def post(self, update, context):
        """Post a tweet using a random account."""
        picture = get_random_picture()
        accounts = get_accounts(self.vps, self.project)
        if not accounts:
            log_error("No accounts available for raid.")
            return
        account = random.choice(accounts)

        chat_type = update.effective_chat.type
        if chat_type == 'private':
            message = (
                get_random_post_text(project=self.project)
                if len(update.message.text.split(' ')) < 2
                else ' '.join(update.message.text.split(' ')[1:])
            )

            await update.message.reply_text('Posting your tweet...')
            await self.queue.put((self.execute_post, (account, message, picture, update)))

    async def execute_post(self, account, message, picture, update):
        """Actual function to post the tweet."""
        selenium_actions = SeleniumActions(self.proxy, None)
        success = await asyncio.to_thread(selenium_actions.post, account, message, picture)
        if success:
            await update.message.reply_text("Tweet posted successfully!")
        else:
            await update.message.reply_text("Failed to post the tweet.")

    async def raid(self):
        """Raid a tweet with a random number of accounts."""
        erase_logs()
        accounts = get_accounts(vps=self.vps, project=self.project)
        if not accounts:
            log_error("No accounts available for raid.")
            return
        random.shuffle(accounts)
        selenium_actions = SeleniumActions(self.proxy, self.processed_tracker)
        for account in accounts:
            selenium_actions.process_account(account)
            self.remove_link_if_interacted_by_all()
            random_delay()
        self.raid_running = False
        
    def remove_link_if_interacted_by_all(self):
        """Check if a link in self.processed_tracker has been interacted with by all accounts."""
        accounts = get_accounts(vps=self.vps, project=self.project)
        links_to_remove = []

        for link in list(self.processed_tracker.keys()):
            if len(self.processed_tracker[link]) == (len(accounts) - 2):
                links_to_remove.append(link)

        for link in links_to_remove:
            del self.processed_tracker[link]
            save_interacted_tweet(link)

    async def logs(self, update, context):
        """Retrieve and send the latest logs."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            logs = get_logs()
            await update.message.reply_text(logs)

    async def clear_logs(self, update, context):
        """Clear the logs."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            erase_logs()
            await update.message.reply_text('Logs cleared.')

    async def get_locked_accounts(self, update, context):
        """Get and display quarantined accounts."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            quarantined_accounts = get_locked_accounts(vps=self.vps, project=self.project)
            if not quarantined_accounts:
                await update.message.reply_text('No locked accounts.')
                return
            usernames = ', '.join([account['username'] for account in quarantined_accounts])
            await update.message.reply_text(usernames)

    async def get_suspended_accounts(self, update, context):
        """Get and display suspended accounts."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            suspended_accounts = get_suspended_accounts(vps=self.vps, project=self.project)
            if not suspended_accounts:
                await update.message.reply_text('No suspended accounts.')
                return
            usernames = ', '.join([account['username'] for account in suspended_accounts])
            await update.message.reply_text(usernames)

    async def unlock_account(self, update, context):
        """Move a quarantined account back to active."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            if len(update.message.text.split(' ')) < 2:
                await update.message.reply_text('No username provided.')
                return
            username = update.message.text.split(' ')[1]
            operation_result = unlock_account(username)
            if not operation_result:
                await update.message.reply_text(f"Failed to move {username} to active accounts.")
                return
            await update.message.reply_text(f"{username} moved to active accounts.")

    async def remove_link_from_interacted(self, update, context):
        """Remove a link from the interacted tracker."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            if len(update.message.text.split(' ')) < 2:
                await update.message.reply_text('No link provided.')
                return
            link = update.message.text.split(' ')[1]
            if remove_interacted_tweets(link):
                await update.message.reply_text(f"{link} removed.")
                return
            await update.message.reply_text(f"{link} not found.")

    async def empty_processed_tracker(self, update, context):
        """Empty the processed tracker."""
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            self.processed_tracker = {}
            await update.message.reply_text('Processed tracker emptied.')

    def start(self):
        """Start the Telegram bot."""
        self.application.run_polling()
