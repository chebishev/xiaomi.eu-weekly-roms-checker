import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv
from xiaomi_eu_new_thread_checker import telegram_message, fix_title

load_dotenv()
message = telegram_message()
title = message[0]
bot = Bot(os.getenv('TOKEN'))
message[0] = f"#{fix_title(title)}"


async def send_telegram_message():
    for m in message:
        await bot.send_message(
            chat_id="@%s" % os.getenv('CHANNEL_NAME'),
            text=m
        )


asyncio.run(send_telegram_message())
