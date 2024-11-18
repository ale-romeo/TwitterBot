from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
import random
from automation.selenium_actions import SeleniumActions
from utils.file_handler import load_json, save_interacted_tweet, check_interacted_tweet
from utils.helpers import get_random_post_text, get_random_picture

class TelegramBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("post", self.post))
        self.application.add_handler(CommandHandler("logs", self.logs))
        self.application.add_handler(MessageHandler(filters.TEXT, self.monitor_group_messages))

    async def monitor_group_messages(self, update, context):
        try:
            chat_type = update.effective_chat.type
            if not update.message.text:
                return
            message_text = update.message.text
            twitter_link = self.extract_twitter_link(message_text)

            if twitter_link and not check_interacted_tweet(twitter_link):
                await update.message.reply_animation(animation='img/push.gif', caption=f"ZHOA ARMY!! IT'S TIME TO SHINE 🔥🔥\n{twitter_link}")
                result = self.raid(tweet_url=twitter_link)
                save_interacted_tweet(twitter_link)
        except Exception as e:
            logging.error(f"Error processing group message: {e}")

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
            account = random.choice(accounts)
            post_success = xactions.post(account, message, picture)
            xactions.teardown()
            if post_success:
                await update.message.reply_text('Tweet posted successfully!')
            else:
                await update.message.reply_text('Failed to post the tweet.\nPlease check the logs for more information.')


    async def logs(self, update, context):
        # Add logs retrieval logic
        pass

    def start(self):
        self.application.run_polling()
