from ultralytics import YOLO

model = YOLO("yolov8n.pt")


while True:
    snapshot_path = input("Enter the path of the snapshot: ")
    results = model(snapshot_path)  # YOLO inference
    detections = results[0].boxes
    car_detected = [obj for obj in detections if obj.cls == 2]

    if car_detected:
        print(f"{len(car_detected)} car(s) detected")
    else:
        print("NO car detected")
