import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8913309887:AAGsD6Ye9EnD1MH9xQHaPPgssTgiZTDSC4w"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ربات روشن است!"
    )


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("Bot Started...")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())