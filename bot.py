import asyncio
import os
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not TOKEN or not CHANNEL_ID:
    print("❌ TOKEN or CHANNEL_ID not set!")
    exit(1)

# ========== دستور /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ربات فعال است!\n"
        f"📢 کانال: {CHANNEL_ID}\n"
        "🔄 منتظر پست‌های جدید هستم..."
    )

# ========== تابع بررسی کانال ==========
async def check_channel():
    bot = Bot(token=TOKEN)
    last_post_id = None
    print("✅ ربات فعال است و در حال اجرا...")
    print(f"📢 کانال: {CHANNEL_ID}")
    
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
                    
                    print(f"📩 پست جدید دریافت شد! ID: {post_id}")
                    print(f"📢 Chat ID: {chat_id}")
                    
                    if str(chat_id) == str(CHANNEL_ID) or f"@{post.chat.username}" == CHANNEL_ID:
                        print("✅ این پست از کانال شماست!")
                        if post_id != last_post_id:
                            try:
                                await bot.set_message_reaction(
                                    chat_id=CHANNEL_ID,
                                    message_id=post_id,
                                    reaction=[{"type": "emoji", "emoji": "👍"}]
                                )
                                print(f"👍 واکنش ارسال شد برای پست {post_id}")
                                last_post_id = post_id
                            except Exception as e:
                                print(f"❌ خطا در ارسال واکنش: {e}")
                    else:
                        print("⚠️ این پست از کانال شما نیست.")
            
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"⚠️ خطا: {e}")
            await asyncio.sleep(5)

# ========== تابع اصلی ==========
async def main():
    print("🚀 راه‌اندازی ربات و وب سرور...")
    
    # راه‌اندازی اپلیکیشن برای دستور /start
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ ربات روشن شد! برو تلگرام و /start بزن.")
    
    # اجرای اپلیکیشن در پس‌زمینه
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=["message"])
    
    # اجرای تابع بررسی کانال
    await check_channel()

# ========== اجرا ==========
if __name__ == "__main__":
    asyncio.run(main())
