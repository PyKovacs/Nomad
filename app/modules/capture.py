import os

import ffmpeg
from log_config import get_logger
from settings import get_rtsp_settings

logger = get_logger(__name__)

settings = get_rtsp_settings()
streaming = ffmpeg.input(settings.url, rtsp_transport="tcp")


def capture_frame(file_path: str):
    try:
        logger.info(f"Capturing a frame to {file_path}")

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Remove the snapshot if exists
        os.remove(file_path)

        # Capture a single frame with '-update 1'
        stream = streaming.output(
            file_path, vframes=1, format="image2", pix_fmt="rgb24"
        )
        stream.run(capture_stdout=True, capture_stderr=True)

    except ffmpeg._run.Error as err:
        logger.error(f"FFmpeg error: {err.stderr.decode()}")
        raise
