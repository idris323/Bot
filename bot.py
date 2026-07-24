import asyncio
from telegram import Bot
from telegram.error import TelegramError
import os

TOKEN = os.environ.get("BOT_TOKEN")  # 🔐 از محیط بخوان
CHANNEL_ID = os.environ.get("CHANNEL_ID")

bot = Bot(token=TOKEN)

async def like_new_posts():
    last_post_id = None
    print("✅ ربات فعال شد...")

    while True:
        try:
            updates = await bot.get_updates(limit=1, allowed_updates=["channel_post"])
            
            if updates:
                post = updates[0].channel_post
                post_id = post.message_id

                if post_id != last_post_id:
                    await bot.set_message_reaction(
                        chat_id=CHANNEL_ID,
                        message_id=post_id,
                        reaction=[{"type": "emoji", "emoji": "👍"}]
                    )
                    print(f"👍 واکنش به پست {post_id} ارسال شد.")
                    last_post_id = post_id

            await asyncio.sleep(2)

        except TelegramError as e:
            print(f"❌ خطا: {e}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(like_new_posts())