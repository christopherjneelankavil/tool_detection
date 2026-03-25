import cv2
from ultralytics import YOLO

# Load model
model = YOLO("best_medium.pt")
model.to('cpu')
print("✅ Model loaded:", model.ckpt_path)  # verify correct model

COLORS = {
    "Hammer": (0, 0, 255),
    "Wrench": (0, 255, 0),
    "Plier":  (255, 165, 0),
    "Socket": (255, 0, 255),
    "Bit":    (0, 255, 255),
}

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("✅ Running! Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Fix 1: use imgsz=640 for better accuracy
    # Fix 2: lower conf to 0.3
    results = model(frame, conf=0.3, imgsz=640, device='cpu', verbose=False)

    for box in results[0].boxes:
        cls_id = int(box.cls)
        label  = model.names[cls_id]
        conf   = float(box.conf)
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        color = COLORS.get(label, (255, 255, 255))

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        text = f"{label} {conf:.0%}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, text, (x1 + 3, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    count = len(results[0].boxes)
    cv2.putText(frame, f"Tools: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "YOLOv8m | CPU", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("Tool Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
