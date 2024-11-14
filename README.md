# 🚀 Twitter Engagement Bot

> An automated Twitter bot designed to maximize interactions with your posts, leveraging a mix of reactions, comments, and reposts for increased engagement. Whether you're promoting a brand, joining a meme wave, or diving into the crypto world, this bot has you covered.

## 📌 Features

- **Automated Reactions**: Likes, retweets, and bookmarks on specified posts.
- **Randomized Comments**: Predefined and customizable comments for varied engagement.
- **Media Attachments**: Supports images, GIFs, and video attachments for posts and comments.
- **Multiple Account Support**: Seamlessly switch between multiple Twitter accounts.
- **Telegram Bot Integration**: Control the bot directly from Telegram for instant actions.

## 💡 How It Works

This bot uses **Selenium** to interact with Twitter and perform tasks such as liking, retweeting, commenting, and bookmarking tweets automatically. With pre-loaded cookies, it securely logs into each account without re-authentication, offering a smooth, uninterrupted experience. Integration with Telegram means you can send commands and receive live updates right from your chat app!

## 🛠️ Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/twitter-engagement-bot.git
   cd twitter-engagement-bot
2. **Install Dependencies**
   This bot requires Python 3.9 or higher. Install dependencies with:

  ```bash
  pip install -r requirements.txt
  ```
3. **Set Environment Variables**
   Set your Telegram API token in an environment variable for secure access:
   ```bash
   export TELEGRAM_BOT_TOKEN='your-telegram-bot-token'
   ```
4. Configure Accounts and Settings
   - Update the accounts.json file with your Twitter account credentials and cookies.
   - Customize your engagement messages in messages.txt and media in media/.

## 📲 Usage

### Telegram Commands

You can control the bot directly from Telegram with these commands:

- **`/start`** - Initializes the bot and starts listening for commands.
- **`/raid <tweet_url>`** - Launches an engagement campaign on the specified tweet, including actions like likes, retweets, comments, and bookmarks.
- **`/post <message>`** - Posts a new tweet with the specified message. Optionally includes media attachments.
- **`/logs`** - Retrieves the latest activity logs, giving insights into the bot's actions and engagement metrics.

### Customizable Options

Personalize the bot’s behavior to enhance engagement:

- **Random Message Pools**: Pulls from a customizable list of comments to keep interactions varied and natural.
- **Emoji and Media Attachments**: Adds emojis and media files to comments for richer engagement.
- **Timing Intervals**: Set randomized delays between actions to mimic human behavior and reduce the chance of detection.

To adjust these options, edit the configuration files such as `messages.txt` for comments and `media/` for images, videos, or GIFs to be attached.

---

**Note:** Make sure to verify your environment setup and configuration files before running the bot to ensure it functions as expected.
