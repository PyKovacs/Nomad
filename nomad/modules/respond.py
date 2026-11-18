from telegram import Update
from telegram.ext import ContextTypes

from nomad.log_config import get_logger
from nomad.session import BOT_SUSPENDED, IGNORE_COUNT, OBJECT_COUNT_AWARENESS, SNAPSHOTS_PATH
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

    elif text == "unset counter":
        OBJECT_COUNT_AWARENESS[0] = False
        await update.message.reply_text("object count awareness disabled")
        logger.info("Object count awareness disabled")

    elif "set ignore" in text:
        ignore_value = text[-1]
        if not ignore_value.isdigit():
            await update.message.reply_text("Ignore value invalid.")
            logger.info(f"Ignore value invalid: {ignore_value}")
            return
        IGNORE_COUNT[0] = ignore_value
        await update.message.reply_text(f"ignore value set to {ignore_value}")
        logger.info(f"Ignore value set to {ignore_value}")

    else:
        await update.message.reply_text("what?")
