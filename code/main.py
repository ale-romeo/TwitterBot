from bot.telegram_bot import TelegramBot
from config.env import TELEGRAM_TOKEN

def main():
    if not TELEGRAM_TOKEN:
        raise ValueError("Telegram token not found in environment variables.")
    
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.start()

if __name__ == "__main__":
    main()
