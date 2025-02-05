from enum import Enum

from log_config import get_logger
from modules import capture, detect, notify
from ultralytics import YOLO

logger = get_logger(__name__)

FILE_PATH = "snapshots/current.png"
OD_MODEL = YOLO("models/yolov8n.pt")


class DetectionType(Enum):
    CAR = 2


def main():
    logger.info("Starting the main loop")
    active_detection_type = DetectionType.CAR
    previous_detected_objects_count = 0
    while True:
        capture.capture_frame(FILE_PATH)
        detected_objects_count = detect.detect_objects(FILE_PATH, OD_MODEL, active_detection_type.value)
        if detected_objects_count != previous_detected_objects_count:
            notify.send_notification(detected_objects_count, active_detection_type.name, FILE_PATH)
        previous_detected_objects_count = detected_objects_count


if __name__ == "__main__":
    main()
