from pathlib import Path

from ultralytics import YOLO

from nomad.log_config import get_logger
from nomad.settings import get_yolo_model_settings

logger = get_logger(__name__)


def detect_objects(snapshot_filename: str | Path, model: YOLO, object_class: int) -> bool:
    """
    Detect objects in a snapshot and return True if the specified object class is detected

    object_class: 2 for cars
    """
    results = model(snapshot_filename, conf=get_yolo_model_settings().confidence)  # YOLO inference
    detections = results[0].boxes
    detected_objects_count = len([obj for obj in detections if obj.cls == object_class])
    logger.info(f"{detected_objects_count} object(s) detected")
    return bool(detected_objects_count)
