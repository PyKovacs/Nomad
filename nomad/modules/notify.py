import asyncio

from telegram import Bot

from nomad.log_config import get_logger
from nomad.settings import get_telegram_bot_settings

logger = get_logger(__name__)

bot_settings = get_telegram_bot_settings()
bot = Bot(token=bot_settings.token)

### TODO - resolve Event loop is closed error (https://docs.python.org/3.11/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(bot.set_webhook(url="https://example.com/"))


async def send_message_and_snapshot(chat_id: int, text: str, snapshot_file: str) -> None:
    """
    Send a message and snapshot to a chat.
    """
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_photo(chat_id=chat_id, photo=snapshot_file)


def send_notification(detected_objects_count: int, active_detection_type_name: str, snapshot_file: str) -> None:
    """
    Send a notification with the number of detected objects and a snapshot to all chat ids.
    """
    logger.info(f"Sending a notification with {detected_objects_count} detected objects")
    message = f"DETECTION: {detected_objects_count} {active_detection_type_name.lower()}{'' if detected_objects_count == 1 else 's'}"
    for chat_id in bot_settings.chat_ids:
        logger.info(f"Sending a notification to chat ID: {chat_id}")
        asyncio.run(send_message_and_snapshot(chat_id, message, snapshot_file))
