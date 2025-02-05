from enum import Enum
from time import sleep

from log_config import get_logger
from modules import capture, detect, notify
from ultralytics import YOLO

logger = get_logger(__name__)

FILE_PATH = "snapshots/current.png"
OD_MODEL = YOLO("models/yolov8n.pt")
DETECTION_DELAY_SECONDS = 0


class DetectionType(Enum):
    CAR = 2
    # Add more detection types here if needed


def main(active_detection_type):
    logger.info("")
    logger.info("################################## NOMAD ##################################")
    logger.info(f"# Snapshot will be saved to: {FILE_PATH:>43}  #")
    logger.info(f"# Object detection model: {OD_MODEL.model_name:>46}  #")
    logger.info(f"# Frame capture delay: {DETECTION_DELAY_SECONDS:>41} seconds  #")
    logger.info(f"# Active detection type: {active_detection_type.name:>47}  #")
    logger.info("###########################################################################")
    logger.info("")

    previous_detected_objects_count = 0
    while True:
        logger.info("----->  Main loop iteration started")
        capture.capture_frame(FILE_PATH)
        detected_objects_count = detect.detect_objects(FILE_PATH, OD_MODEL, active_detection_type.value)
        if detected_objects_count != previous_detected_objects_count:
            notify.send_notification(detected_objects_count, active_detection_type.name, FILE_PATH)
        previous_detected_objects_count = detected_objects_count
        sleep(DETECTION_DELAY_SECONDS)
        logger.info("----->  Main loop iteration completed")


if __name__ == "__main__":
    main(active_detection_type=DetectionType.CAR)
