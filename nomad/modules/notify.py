import asyncio
from pathlib import Path

from telegram import Bot

from nomad.log_config import get_logger
from nomad.settings import TelegramBotSettings

logger = get_logger(__name__)

bot_settings = TelegramBotSettings()
bot = Bot(token=bot_settings.token)


def anti_flood() -> bool:
    """
    Check the number of messages sent in the n most recent lines of the log file.
    Returns True if the number of messages is more than 2, otherwise False.
    """
    most_recent_lines = 120  # new line every approx. 5 seconds; 5 * 120 = 600 seconds = 10 minutes
    log_file = logger.handlers[0].baseFilename  # type: ignore
    with open(log_file, "r") as f:
        lines = f.readlines()[-most_recent_lines:]
    messages = [line for line in lines if "Sending notifications to chat ids" in line]
    return len(messages) >= 2


async def send_message_and_snapshot(chat_id: int, text: str, snapshot_file: str | Path) -> None:
    """
    Send a snapshot to a chat.
    """
    await bot.send_photo(chat_id=chat_id, photo=snapshot_file, caption=text)


def send_notification(
    detection_positive: bool,
    active_detection_type_name: str,
    snapshot_file: str | Path,
    event_loop: asyncio.AbstractEventLoop,
) -> None:
    """
    Send a notification with the number of detected objects and a snapshot to all chat ids.
    """
    if anti_flood():
        logger.warning("ANTI-FLOOD triggered, skipping notification")
        return

    message = f"{active_detection_type_name} DETECTED!"
    if not detection_positive:
        message = "aaaand is gone..."
    logger.info(f"Sending notifications to chat ids: {bot_settings.chat_ids}")
    for chat_id in bot_settings.chat_ids:
        event_loop.run_until_complete(send_message_and_snapshot(chat_id, message, snapshot_file))
