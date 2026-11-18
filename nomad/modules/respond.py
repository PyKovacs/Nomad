from telegram import Update
from telegram.ext import ContextTypes

from nomad.log_config import get_logger
from nomad.session import BOT_SUSPENDED, OBJECT_COUNT_AWARENESS, SNAPSHOTS_PATH
from nomad.settings import TelegramBotSettings

logger = get_logger(__name__)
bot_settings = TelegramBotSettings()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    logger.info(f"Bot received command: {text}")

    if text in ("report", "status", "r", "s"):
        logger.info("Responding to status report with latest snapshot.")
        with open(SNAPSHOTS_PATH / "current.png", "rb") as img:
            await update.message.reply_photo(photo=img)

    elif text == "stop":
        BOT_SUSPENDED[0] = True
        await update.message.reply_text("ok, suspended")
        logger.info("Bot notifications suspended.")

    elif text == "start":
        BOT_SUSPENDED[0] = False
        await update.message.reply_text("ok, activated")
        logger.info("Bot notifications activated.")

    elif text == "set counter":
        OBJECT_COUNT_AWARENESS[0] = True
        await update.message.reply_text("object count awareness enabled")
        logger.info("Object count awareness enabled")

    else:
        await update.message.reply_text("what?")
