import asyncio
from enum import Enum
from pathlib import Path

import ffmpeg
from ultralytics import YOLO

from nomad.log_config import get_logger
from nomad.modules import capture, detect, notify
from nomad.settings import RTSPSettings, YOLOModelSettings

rtsp_settings = RTSPSettings()
yolo_settings = YOLOModelSettings()


class DetectionType(Enum):
    CAR = 2
    # Add more detection types here if needed


# BOT_SUSPENDED enables or disables the notifications
BOT_SUSPENDED = [False]
# OBJECT_COUNT_AWARENESS enables or disables notifications on CHANGED count of detected objects
OBJECT_COUNT_AWARENESS = [False]
# IGNORE_COUNT sets the threshold for notifications, if set to 1, detections of 1 object will not trigger a notification
IGNORE_COUNT = [0]
ACTIVE_DETECTION_TYPE = DetectionType.CAR
APP_DIR = Path.home() / "nomad"
SNAPSHOTS_PATH = APP_DIR / "snapshots"
MODEL_PATH = APP_DIR / "models" / yolo_settings.model_name

logger = get_logger(__name__)


def log_init_info() -> None:
    logger.info("")
    logger.info("################################## NOMAD ##################################")
    logger.info(f"# Snapshot path: {str(SNAPSHOTS_PATH):>55}  #")
    logger.info(f"# OD model path: {str(MODEL_PATH):>55}  #")
    logger.info(f"# Frame capture delay: {rtsp_settings.detection_delay_seconds:>41} seconds  #")
    logger.info(f"# Active detection type: {ACTIVE_DETECTION_TYPE.name:>47}  #")
    logger.info("###########################################################################")
    logger.info("")


def get_streaming():
    return ffmpeg.input(
        rtsp_settings.url,
        rtsp_transport="tcp",
        probesize="5000000",
        analyzeduration="10000000",
    )


async def run_session():
    log_init_info()

    objects_detected_before = 0
    frame_capture_failures = 0
    od_model = YOLO(MODEL_PATH)

    ### main loop
    while True:
        frame_captured = await asyncio.to_thread(capture.capture_frame, SNAPSHOTS_PATH, get_streaming())

        ### frame capture failure handling
        if not frame_captured:
            if frame_capture_failures > 20:
                logger.error("Failed to capture a frame too many times, exiting...")
                break
            frame_capture_failures += 1
            logger.error("Failed to capture a frame, sleeping for 30 seconds...")
            await asyncio.sleep(30)
            continue
        frame_capture_failures = 0

        objects_detected_now = detect.detect_objects(
            SNAPSHOTS_PATH / "current.png", od_model, ACTIVE_DETECTION_TYPE.value
        )
        if objects_detected_now >= IGNORE_COUNT[0]:
            objects_detected_now -= IGNORE_COUNT[0]

        if OBJECT_COUNT_AWARENESS[0] and objects_detected_now != objects_detected_before and not BOT_SUSPENDED[0]:
            await notify.send_notification(
                detection_positive=objects_detected_now,
                snapshot_file=SNAPSHOTS_PATH / "current.png",
                message=f"{objects_detected_now} {ACTIVE_DETECTION_TYPE.name}(s) detected!",
            )

        elif bool(objects_detected_now) is not bool(objects_detected_before) and not BOT_SUSPENDED[0]:
            await notify.send_notification(
                detection_positive=objects_detected_now,
                snapshot_file=SNAPSHOTS_PATH / "current.png",
                message=f"{ACTIVE_DETECTION_TYPE.name}(s) detected!",
            )

        objects_detected_before = objects_detected_now
        await asyncio.sleep(rtsp_settings.detection_delay_seconds)
