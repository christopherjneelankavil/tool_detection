import cv2
from ultralytics import YOLO

# Load model on CPU
model = YOLO("best.pt")
model.to('cpu')

# Class colors
COLORS = {
    "Hammer": (0, 0, 255),
    "Wrench": (0, 255, 0),
    "Plier":  (255, 165, 0),
    "Socket": (255, 0, 255),
    "Bit":    (0, 255, 255),
}

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # lower resolution = faster on CPU
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✅ Tool Detector Running on CPU! Press 'Q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection on CPU with smaller image size (faster)
    results = model(frame, conf=0.4, imgsz=320, device='cpu', verbose=False)

    # Draw detections
    for box in results[0].boxes:
        cls_id = int(box.cls)
        label  = model.names[cls_id]
        conf   = float(box.conf)
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        color = COLORS.get(label, (255, 255, 255))

        # Bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Label background
        text = f"{label} {conf:.0%}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)

        # Label text
        cv2.putText(frame, text, (x1 + 3, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show detection count
    count = len(results[0].boxes)
    cv2.putText(frame, f"Tools: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show running device
    cv2.putText(frame, "Device: CPU", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("Tool Detector - CPU", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
