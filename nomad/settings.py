from pydantic_settings import BaseSettings, SettingsConfigDict

from nomad.log_config import get_logger

logger = get_logger(__name__)


class TelegramBotSettings(BaseSettings):
    token: str
    chat_ids: list[int]

    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", env_prefix="TELEGRAM_BOT_"
    )


class RTSPSettings(BaseSettings):
    url: str
    detection_delay_seconds: int = 5

    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", env_prefix="RTSP_"
    )


class YOLOModelSettings(BaseSettings):
    model_name: str = "yolov8m.pt"
    confidence: float = 0.7
    model_config = SettingsConfigDict(
        env_file=".env", extra="allow", env_prefix="YOLO_"
    )
