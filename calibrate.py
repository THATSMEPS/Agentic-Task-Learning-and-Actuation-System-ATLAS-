# calibrate.py
import cv2

# --- 1. SET THESE VALUES ---
KNOWN_REAL_WIDTH_CM = 6.5  # (e.g., width of a standard soda can)
KNOWN_DISTANCE_CM = 30.0   # (e.g., place the can 60cm from your camera)
# ---------------------------

# Use YOLOv8 'n' model to find the object
from ultralytics import YOLO
model = YOLO('yolov8n.pt')

# Find the class ID for 'bottle' (or 'cup' if soda can isn't detected well)
# 'bottle' is class 39, 'cup' is class 41
TARGET_CLASS_ID = 66 # 39 = bottle

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot open camera")
    exit()

print("\n--- Camera Calibration ---")
print(f"Point your camera at the object (Known Width: {KNOWN_REAL_WIDTH_CM} cm)")
print(f"Place it exactly {KNOWN_DISTANCE_CM} cm away.")
print("A 'pixel_width' will be shown. Wait for it to be stable.")
print("Press 'c' to calculate focal length. Press 'q' to quit.")
print("-" * 30)

focal_length_avg = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Flip the frame
    frame = cv2.flip(frame, 1)
    
    # Run YOLO detection
    results = model(frame, verbose=False, conf=0.5)
    
    found = False
    for res in results:
        boxes = res.boxes
        for box in boxes:
            if int(box.cls[0]) == TARGET_CLASS_ID:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # We found our object
                pixel_width = x2 - x1
                
                # Draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"Pixel Width: {pixel_width}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Display instructions
                cv2.putText(frame, f"Known Dist: {KNOWN_DISTANCE_CM} cm", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Known Width: {KNOWN_REAL_WIDTH_CM} cm", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                found = True
                
                key = cv2.waitKey(30) & 0xFF
                if key == ord('c'):
                    # Calculate focal length
                    focal_length = (pixel_width * KNOWN_DISTANCE_CM) / KNOWN_REAL_WIDTH_CM
                    focal_length_avg.append(focal_length)
                    avg = sum(focal_length_avg) / len(focal_length_avg)
                    print(f"  -> Measured Pixel Width: {pixel_width}")
                    print(f"  -> Calculated Focal Length: {focal_length:.2f}")
                    print(f"  -> Average Focal Length: {avg:.2f}")
                elif key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()
                break
        if found:
            break

    if not found:
        cv2.putText(frame, "Looking for object...", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Calibration - Press 'c' to capture, 'q' to quit", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()