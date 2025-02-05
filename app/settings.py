from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramBotSettings(BaseSettings):
    token: str
    chat_ids: list[int]

    model_config = SettingsConfigDict(env_file=".env", extra="allow", env_prefix="TELEGRAM_BOT_")


class RTSPSettings(BaseSettings):
    url: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow", env_prefix="RTSP_")


@cache
def get_telegram_bot_settings() -> TelegramBotSettings:
    return TelegramBotSettings()


@cache
def get_rtsp_settings() -> RTSPSettings:
    return RTSPSettings()
