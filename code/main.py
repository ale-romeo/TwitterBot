from bot.telegram_bot import TelegramBot
from config.env import TELEGRAM_TOKEN, VPS, PROJECT

def main():
    if not TELEGRAM_TOKEN or not VPS or not PROJECT:
        raise Exception("Please set the environment variables for the bot")
    
    bot = TelegramBot(TELEGRAM_TOKEN, VPS, PROJECT)
    bot.start()

if __name__ == "__main__":
    main()
