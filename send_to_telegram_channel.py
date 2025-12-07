import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv
from xiaomi_eu_new_thread_checker import telegram_message, fix_title

load_dotenv()
message = telegram_message()
title = message[0]
bot_is_existing = True
try: 
    bot = Bot(os.getenv('TOKEN'))
except Exception as e:
    bot_is_existing = False
    print(f"Error initializing bot: {e}")
message[0] = f"#{fix_title(title)}"

async def send_telegram_message():
    if not bot_is_existing:
        print("Bot is not initialized. Exiting.")
        return
    for m in message:
        await bot.send_message(
            chat_id="@%s" % os.getenv('CHANNEL_NAME'),
            text=m
        )

asyncio.run(send_telegram_message())
