import asyncio
import os
import sys
from telegram import Bot
from telegram.error import TelegramError, Conflict
from flask import Flask
from threading import Thread

# ========== Web Server for Render ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ========== Bot Configuration ==========
TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("❌ Error: BOT_TOKEN and CHANNEL_ID environment variables are not set!")
    print("💡 Please set them in Render Dashboard -> Environment Variables")
    sys.exit(1)

bot = Bot(token=TOKEN)

# ========== Bot Functions ==========
async def like_new_posts():
    last_post_id = None
    print("✅ Bot started with Python 3.14...")
    print(f"📢 Channel: {CHANNEL_ID}")
    
    try:
        me = await bot.get_me()
        print(f"🤖 Bot: @{me.username}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return

    while True:
        try:
            updates = await bot.get_updates(
                limit=1,
                allowed_updates=["channel_post"],
                timeout=30
            )
            
            if updates:
                post = updates[0].channel_post
                if post:
                    chat_id = post.chat.id
                    post_id = post.message_id
                    
                    if str(chat_id) == str(CHANNEL_ID) or f"@{post.chat.username}" == CHANNEL_ID:
                        if post_id != last_post_id:
                            try:
                                await bot.set_message_reaction(
                                    chat_id=CHANNEL_ID,
                                    message_id=post_id,
                                    reaction=[{"type": "emoji", "emoji": "👍"}]
                                )
                                print(f"👍 Reaction sent to post {post_id}")
                                last_post_id = post_id
                            except TelegramError as e:
                                print(f"❌ Reaction error: {e}")
            
            await asyncio.sleep(2)

        except Conflict:
            print("⚠️ Bot is running elsewhere, waiting 30 seconds...")
            await asyncio.sleep(30)
        except TelegramError as e:
            print(f"❌ Telegram error: {e}")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            await asyncio.sleep(5)

def run_bot():
    asyncio.run(like_new_posts())

# ========== Main Execution ==========
if __name__ == "__main__":
    print("🚀 Starting bot and web server...")
    
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    try:
        run_bot()
    except KeyboardInterrupt:
        print("👋 Bot stopped")
