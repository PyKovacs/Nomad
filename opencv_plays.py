import cv2
from time import sleep
from settings import get_rtsp_settings

settings = get_rtsp_settings()

# Open the RTSP stream
cap = cv2.VideoCapture(settings.url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Display the frame
    cv2.imshow("RTSP Stream", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    sleep(5)

cap.release()
cv2.destroyAllWindows()
