import ffmpeg
from log_config import get_logger
from settings import get_rtsp_settings

logger = get_logger(__name__)

settings = get_rtsp_settings()
stream = ffmpeg.input(settings.url, ss=0)


def capture_frame(file_path: str):
    logger.info(f"Capturing a frame to {file_path}")
    file = stream.output(file_path, vframes=1)
    file.run(capture_stdout=True, capture_stderr=True)
