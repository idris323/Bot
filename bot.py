import asyncio
import os
import sys
from telegram import Bot
from telegram.error import TelegramError, Conflict
from flask import Flask
from threading import Thread

# ========== بخش وب سرور (برای Render Web Service) ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ ربات تلگرام فعال است!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# ========== بخش ربات تلگرام ==========
TOKEN = os.environ.get("8913309887:AAGsD6Ye9EnD1MH9xQHaPPgssTgiZTDSC4w")
CHANNEL_ID = os.environ.get("https://t.me/test222222_3333")

if not TOKEN or not CHANNEL_ID:
    print("❌ خطا: متغیرهای محیطی TOKEN و CHANNEL_ID را تنظیم کنید!")
    print("💡 برای تست محلی، می‌تونی مستقیم تو کد هم بدی:")
    print('TOKEN = "8913309887:AAGsD6Ye9EnD1MH9xQHaPPgssTgiZTDSC4w"')
    print('CHANNEL_ID = "https://t.me/test222222_3333"')
    sys.exit(1)

bot = Bot(token=TOKEN)

async def like_new_posts():
    last_post_id = None
    print("✅ ربات با پایتون ۳.۱۴ فعال شد...")
    print(f"📢 کانال: {CHANNEL_ID}")
    
    # تست اتصال
    try:
        me = await bot.get_me()
        print(f"🤖 ربات: @{me.username}")
    except Exception as e:
        print(f"❌ خطا در اتصال: {e}")
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
                    
                    # چک کردن کانال
                    if str(chat_id) == str(CHANNEL_ID) or f"@{post.chat.username}" == CHANNEL_ID:
                        if post_id != last_post_id:
                            try:
                                await bot.set_message_reaction(
                                    chat_id=CHANNEL_ID,
                                    message_id=post_id,
                                    reaction=[{"type": "emoji", "emoji": "👍"}]
                                )
                                print(f"👍 واکنش به پست {post_id} ارسال شد.")
                                last_post_id = post_id
                            except TelegramError as e:
                                print(f"❌ خطا در واکنش: {e}")
            
            await asyncio.sleep(2)

        except Conflict:
            print("⚠️ ربات در جای دیگر اجرا شده، ۳۰ ثانیه صبر...")
            await asyncio.sleep(30)
        except TelegramError as e:
            print(f"❌ خطای تلگرام: {e}")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"⚠️ خطا: {e}")
            await asyncio.sleep(5)

# ========== اجرای همزمان وب سرور و ربات ==========
def run_bot():
    asyncio.run(like_new_posts())

if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات و وب سرور...")
    
    # اجرای وب سرور در یک ترد جداگانه
    web_thread = Thread(target=run_web)
    web_thread.daemon = True
    web_thread.start()
    
    # اجرای ربات در ترد اصلی
    try:
        run_bot()
    except KeyboardInterrupt:
        print("👋 توقف ربات")
