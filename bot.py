import asyncio
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("❌ TOKEN not set!")
    exit(1)

# ========== دستور /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات فعال است!")

# ========== تابع اصلی ==========
async def main():
    print("🚀 راه‌اندازی ربات...")
    
    # ساختن اپلیکیشن
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ ربات روشن شد! برو تلگرام و /start بزن.")
    
    # شروع به دریافت آپدیت‌ها
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=["message"])
    
    # نگه داشتن ربات در حالت اجرا
    try:
        while True:
            await asyncio.sleep(3600)  # یک ساعت صبر کن
    except (KeyboardInterrupt, SystemExit):
        print("🛑 ربات در حال توقف...")
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()

# ========== اجرا ==========
if __name__ == "__main__":
    asyncio.run(main())
