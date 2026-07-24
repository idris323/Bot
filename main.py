from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


# توکن ربات را اینجا قرار بده
TOKEN = "8913309887:AAGsD6Ye9EnD1MH9xQHaPPgssTgiZTDSC4w"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ربات روشن است!\nسلام، تست موفق بود."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot Started...")

app.run_polling()