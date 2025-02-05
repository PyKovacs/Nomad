import asyncio

from settings import get_telegram_bot_settings
from telegram import Bot

bot_settings = get_telegram_bot_settings()
bot = Bot(token=bot_settings.token)


async def send_message_and_snapshot(
    chat_id: int, text: str, snapshot_file: str
) -> None:
    """
    Send a message and snapshot to a chat.
    """
    await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_photo(chat_id=chat_id, photo=snapshot_file)


def send_notification(
    detected_objects_count: int, active_detection_type_name: str, snapshot_file: str
) -> None:
    """
    Send a notification with the number of detected objects and a snapshot to all chat ids.
    """
    message = f"DETECTION: {detected_objects_count} {active_detection_type_name.lower()}{'' if detected_objects_count == 1 else 's'}"
    for chat_id in bot_settings.chat_ids:
        asyncio.run(send_message_and_snapshot(chat_id, message, snapshot_file))
