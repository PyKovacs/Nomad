import os
import shutil
import socket
from pathlib import Path
from typing import Any

import ffmpeg

from nomad.log_config import get_logger
from nomad.settings import RTSPSettings

logger = get_logger(__name__)

settings = RTSPSettings()


def get_hostname(url: str) -> str:
    """
    Get the hostname from a URL.
    """
    return url.split("@")[1].split(":")[0]


def check_url(host: str, port: int = 554, timeout: int = 5) -> bool:
    """
    Check if an RTSP connection can be established to the given host and port.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False


def capture_frame(file_path: str | Path, streaming: Any) -> bool:
    """
    Check RTSP stream connection, then capture
    a single frame from an RTSP stream and save it to a file.
    """
    if not check_url(get_hostname(settings.url)):
        logger.error("Failed to connect to the RTSP stream")
        return False
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Remove the snapshot if exists
        # IMPORTANT : must be preserved, otherwise snapshot capture wont work
        if os.path.exists(file_path / "0.png"):
            os.remove(file_path / "0.png")

        # Capture a single frame with '-update 1'
        stream = streaming.output(
            str(file_path / "0.png"),
            vframes=1,
            format="image2",
            pix_fmt="rgb24",
            update=1,
            vf="crop=640:250:220:270",
        )

        stream.run(capture_stdout=True, capture_stderr=True)

        # Copy the snapshot
        if os.path.exists(file_path / "0.png"):
            shutil.copy(file_path / "0.png", file_path / "current.png")

        return True

    except ffmpeg._run.Error as err:
        logger.error(f"FFmpeg error: {err.stderr.decode()}")
        return False
