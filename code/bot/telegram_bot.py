from telegram.ext import Application, CommandHandler, MessageHandler, filters
from automation.selenium_actions import SeleniumActions
from utils.file_handler import get_random_post_text, get_random_picture, get_raid_picture, get_accounts, save_interacted_tweet, check_interacted_tweet, erase_logs, get_logs, get_quarantined_accounts, move_account_to_active
import random
from utils.logging_handler import log_error
from utils.helpers import extract_tweet_link

class TelegramBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("post", self.post))
        self.application.add_handler(CommandHandler("logs", self.logs))
        self.application.add_handler(CommandHandler("quarantined", self.get_quarantined_accounts))
        self.application.add_handler(CommandHandler("move", self.move_account_to_active))
        self.application.add_handler(MessageHandler(filters.TEXT, self.monitor_group_messages))

    async def monitor_group_messages(self, update, context):
        try:
            if not update.message.text:
                return
            message_text = update.message.text
            twitter_link = extract_tweet_link(message_text)

            if twitter_link and not check_interacted_tweet(twitter_link):
                await update.message.reply_animation(animation=get_raid_picture(), caption=f"ZHOA ARMY!! IT'S TIME TO SHINE 🔥🔥\n{twitter_link}")
                self.raid(tweet_url=twitter_link)
                save_interacted_tweet(twitter_link)
        except Exception as e:
            log_error(f"Error processing group message: {e}")

    async def post(self, update, context):
        chat_type = update.effective_chat.type

        if chat_type == 'private':
            if len(update.message.text.split(' ')) < 2:
                await update.message.reply_text('No message provided. Random message will be used.')
                message = get_random_post_text()
            else:
                message = ' '.join(update.message.text.split(' ')[1:])
            picture = get_random_picture()

            xactions = SeleniumActions()
            account = random.choice(get_accounts())
            post_success = xactions.post(account, message, picture)
            xactions.teardown()
            if post_success:
                await update.message.reply_text('Tweet posted successfully!')
            else:
                await update.message.reply_text('Failed to post the tweet.\nPlease check the logs for more details.')

    def raid(self, tweet_url):
        raid_result = True
        erase_logs()
        sel_actions = SeleniumActions()
        accounts = get_accounts()
        for account in accounts:
            interaction_result = sel_actions.interact(account, tweet_url)
            sel_actions.restart()
            raid_result = raid_result and interaction_result
        sel_actions.teardown()
        return raid_result

    async def logs(self, update, context):
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            logs = get_logs()
            await update.message.reply_text(logs)

    async def get_quarantined_accounts(self, update, context):
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            quarantined_accounts = get_quarantined_accounts()
            if not quarantined_accounts:
                await update.message.reply_text('No accounts in quarantine.')
                return
            usernames = ', '.join(quarantined_accounts.keys())
            await update.message.reply_text(usernames)

    async def move_account_to_active(self, update, context):
        chat_type = update.effective_chat.type
        if chat_type == 'private':
            username = update.message.text.split(' ')[1]
            if not username:
                await update.message.reply_text('No username provided.')
                return
            move_account_to_active(username)
            await update.message.reply_text(f"{username} moved to active accounts.")    

    def start(self):
        self.application.run_polling()
