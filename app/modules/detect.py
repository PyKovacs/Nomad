from ultralytics import YOLO


def detect_objects(snapshot_filename: str, model: YOLO, object_class: int) -> int:
    """
    Detect objects in a snapshot and return the number of detected objects of a certain class.

    object_class: 2 for cars
    """
    results = model(snapshot_filename)  # YOLO inference
    detections = results[0].boxes
    detected_objects_count = len([obj for obj in detections if obj.cls == object_class])
    print(f"{detected_objects_count} object(s) detected")
    return detected_objects_count
