import asyncio

from telegram import Bot

from settings import get_telegram_bot_settings

bot_settings = get_telegram_bot_settings()
bot = Bot(token=bot_settings.token)

for chat_id in bot_settings.chat_ids:
    asyncio.run(bot.send_message(chat_id=chat_id, text="Hello, world!"))
