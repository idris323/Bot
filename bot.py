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

# ========== اجرا ==========
if __name__ == "__main__":
    print("🚀 راه‌اندازی ربات...")
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ ربات روشن شد! برو تلگرام و /start بزن.")
    app.run_polling(allowed_updates=["message"])
