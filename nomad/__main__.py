import asyncio

from telegram.ext import Application, MessageHandler, filters

from nomad.log_config import get_logger
from nomad.modules.respond import handle_message
from nomad.session import run_session
from nomad.settings import TelegramBotSettings

logger = get_logger(__name__)


async def main_polling():
    bot_settings = TelegramBotSettings()
    app = Application.builder().token(bot_settings.token).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()  # Wait forever
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


async def main():
    await asyncio.gather(
        run_session(),
        main_polling(),
    )


if __name__ == "__main__":
    asyncio.run(main())
