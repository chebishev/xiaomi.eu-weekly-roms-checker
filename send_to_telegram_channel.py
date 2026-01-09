import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv
from xiaomi_eu_new_thread_checker import telegram_message

load_dotenv()
message = telegram_message()
bot_is_existing = True
try: 
    bot = Bot(os.getenv('TOKEN'))
except Exception as e:
    bot_is_existing = False
    print(f"Error initializing bot: {e}")

async def send_telegram_message():
    if not bot_is_existing:
        for key,value in message.items():
            if value:
                print(value)
        print("Bot is not initialized. Exiting.")
        return
    for key,value in message.items():
        if value:
            await bot.send_message(
                chat_id="@%s" % os.getenv('CHANNEL_NAME'),
                text=m
            )

asyncio.run(send_telegram_message())
