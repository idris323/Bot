import asyncio
import os
import sys
from telegram import Bot
from telegram.error import TelegramError, Conflict

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("❌ خطا: متغیرهای محیطی TOKEN و CHANNEL_ID را تنظیم کنید!")
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

if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات...")
    try:
        asyncio.run(like_new_posts())
    except KeyboardInterrupt:
        print("👋 توقف ربات")
