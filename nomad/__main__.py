import asyncio
from enum import Enum
from pathlib import Path
from time import sleep

import ffmpeg
from ultralytics import YOLO

from nomad.log_config import get_logger
from nomad.modules import capture, detect, notify
from nomad.settings import get_rtsp_settings

settings = get_rtsp_settings()

logger = get_logger(__name__)

APP_DIR = Path.home() / "nomad"
SNAPSHOTS_PATH = APP_DIR / "snapshots" / "current.png"
MODEL_PATH = APP_DIR / "models" / "yolov8n.pt"


class DetectionType(Enum):
    CAR = 2
    # Add more detection types here if needed


ACTIVE_DETECTION_TYPE = DetectionType.CAR


def main():
    logger.info("")
    logger.info("################################## NOMAD ##################################")
    logger.info(f"# Snapshot path: {str(SNAPSHOTS_PATH):>55}  #")
    logger.info(f"# OD model path: {str(MODEL_PATH):>55}  #")
    logger.info(f"# Frame capture delay: {settings.detection_delay_seconds:>41} seconds  #")
    logger.info(f"# Active detection type: {ACTIVE_DETECTION_TYPE.name:>47}  #")
    logger.info("###########################################################################")
    logger.info("")

    ### loading variables
    objects_detected_before = False
    frame_capture_failures = 0
    streaming = ffmpeg.input(settings.url, rtsp_transport="tcp", probesize="5000000", analyzeduration="10000000")
    od_model = YOLO(MODEL_PATH)
    loop = asyncio.get_event_loop()

    ### main loop
    while True:
        frame_captured = capture.capture_frame(SNAPSHOTS_PATH, streaming)

        ### frame capture failure handling
        if not frame_captured:
            if frame_capture_failures > 20:
                logger.error("Failed to capture a frame too many times, exiting...")
                break
            frame_capture_failures += 1
            logger.error("Failed to capture a frame, sleeping for 30 seconds...")
            sleep(30)
            del streaming
            streaming = ffmpeg.input(
                settings.url,
                rtsp_transport="tcp",
                probesize="5000000",
                analyzeduration="10000000",
            )
            continue
        frame_capture_failures = 0

        objects_detected_now = detect.detect_objects(SNAPSHOTS_PATH, od_model, ACTIVE_DETECTION_TYPE.value)
        if objects_detected_now is not objects_detected_before:
            notify.send_notification(
                detection_positive=objects_detected_now,
                active_detection_type_name=ACTIVE_DETECTION_TYPE.name,
                snapshot_file=SNAPSHOTS_PATH,
                event_loop=loop,
            )
        objects_detected_before = objects_detected_now
        sleep(settings.detection_delay_seconds)


if __name__ == "__main__":
    main()
