from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from nomad.log_config import get_logger

logger = get_logger(__name__)


class TelegramBotSettings(BaseSettings):
    token: str
    chat_ids: list[int]

    model_config = SettingsConfigDict(env_file=".env", extra="allow", env_prefix="TELEGRAM_BOT_")


class RTSPSettings(BaseSettings):
    url: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow", env_prefix="RTSP_")


@cache
def get_telegram_bot_settings() -> TelegramBotSettings:
    logger.info("Loading Telegram bot settings")
    return TelegramBotSettings()


@cache
def get_rtsp_settings() -> RTSPSettings:
    logger.info("Loading RTSP settings")
    return RTSPSettings()
