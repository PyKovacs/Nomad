from ultralytics import YOLO

model = YOLO("yolov8n.pt")


while True:
    snapshot_path = input("Enter the path of the snapshot: ")
    results = model(snapshot_path)  # YOLO inference
    detections = results[0].boxes
    car_detected = any(obj.cls == 2 for obj in detections)

    if car_detected:
        print("Car detected")
    else:
        print("NO car detected")
