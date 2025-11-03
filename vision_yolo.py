import cv2
import numpy as np
from ultralytics import YOLO
import config

class YOLOVisionSystem:
    """
    Robust vision system using YOLOv8 for object detection and HSV for color filtering.
    """
    def __init__(self, use_laptop_camera=True, model_path='yolov8n.pt'):
        self.use_laptop_camera = use_laptop_camera
        self.camera = None
        self.target_object = None
        self.target_color = None
        self.model = YOLO(model_path)
        self.model.overrides['verbose'] = False  # Disable YOLO logging spam
        self.focal_length = 700  # pixels (calibrated for better distance)
        self.default_object_width = 10  # cm, fallback if unknown
        print("[YOLOVISION] - Initialized with YOLOv8 model")

    def initialize_camera(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            print("[YOLOVISION] - ERROR: Could not open camera!")
            return False
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        print(f"[YOLOVISION] - Camera {camera_index} initialized successfully")
        return True

    def release_camera(self):
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
            print("[YOLOVISION] - Camera released")

    def set_target(self, object_name, color=None):
        self.target_object = object_name.lower()
        self.target_color = color.lower() if color else None
        print(f"[YOLOVISION] - Target set: object='{self.target_object}', color='{self.target_color}'")

    def get_real_width(self, class_name):
        # You can expand this dictionary for more accurate sizes
        known_sizes = {
            'phone': 15, 'book': 20, 'pen': 1.5, 'bottle': 7, 'cup': 8, 'laptop': 35,
            'mouse': 10, 'keyboard': 40, 'pillow': 40, 'remote': 15, 'wallet': 10
        }
        return known_sizes.get(class_name, self.default_object_width)

    def estimate_distance(self, pixel_width, class_name):
        real_width = self.get_real_width(class_name)
        if pixel_width > 0:
            return (real_width * self.focal_length) / pixel_width
        return None

    def color_match(self, frame, box, color_name):
        """Check if object matches the requested color."""
        if not color_name:
            return True  # No color specified, match any
        
        x1, y1, x2, y2 = map(int, box)
        # Ensure coordinates are within frame bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
        
        if x2 <= x1 or y2 <= y1:
            return False
            
        roi = frame[y1:y2, x1:x2]
        if roi.size == 0:
            return False
            
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # More lenient HSV ranges for better color detection
        color_hsv = {
            'red': [(0, 50, 50, 10, 255, 255), (170, 50, 50, 180, 255, 255)],
            'blue': [(90, 50, 50, 130, 255, 255)],  # Wider blue range
            'green': [(35, 40, 40, 85, 255, 255)],
            'yellow': [(20, 80, 80, 35, 255, 255)],
            'orange': [(8, 80, 80, 25, 255, 255)],
            'purple': [(125, 50, 50, 165, 255, 255)],
            'pink': [(140, 50, 50, 175, 255, 255)],
            'white': [(0, 0, 180, 180, 40, 255)],
            'black': [(0, 0, 0, 180, 255, 40)]
        }
        
        masks = []
        for rng in color_hsv.get(color_name, []):
            lower = np.array(rng[:3])
            upper = np.array(rng[3:])
            masks.append(cv2.inRange(hsv_roi, lower, upper))
        
        if masks:
            mask = masks[0]
            for m in masks[1:]:
                mask = cv2.bitwise_or(mask, m)
            ratio = np.sum(mask > 0) / mask.size
            # Lower threshold to 15% for more lenient matching
            return ratio > 0.15
        return True

    def detect_and_annotate(self, frame):
        results = self.model(frame, verbose=False)[0]  # Disable verbose logging
        annotated = frame.copy()
        found = False
        frame_h, frame_w = frame.shape[:2]
        
        # Draw blue plus sign at center
        center_x, center_y = frame_w // 2, frame_h // 2
        cv2.drawMarker(annotated, (center_x, center_y), (255, 0, 0), cv2.MARKER_CROSS, 30, 3)
        cv2.putText(annotated, "CENTER", (center_x - 40, center_y - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        for box, conf, cls in zip(results.boxes.xyxy.cpu().numpy(),
                                  results.boxes.conf.cpu().numpy(),
                                  results.boxes.cls.cpu().numpy()):
            class_name = self.model.names[int(cls)]
            
            # Match class name (e.g., "cell phone" contains "phone")
            if self.target_object and self.target_object not in class_name.lower():
                continue
            
            # Match color if specified
            if self.target_color and not self.color_match(frame, box, self.target_color):
                continue
            
            x1, y1, x2, y2 = map(int, box)
            pixel_width = x2 - x1
            distance = self.estimate_distance(pixel_width, class_name)
            
            # Draw green bounding box (THICK)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 5)
            
            # Draw centroid (red dot)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(annotated, (cx, cy), 8, (0, 0, 255), -1)
            
            # Draw line from center to object (yellow)
            cv2.line(annotated, (center_x, center_y), (cx, cy), (0, 255, 255), 3)
            
            # LARGE distance text above box (GREEN)
            if distance:
                dist_text = f"{distance:.1f} cm"
                text_size = cv2.getTextSize(dist_text, cv2.FONT_HERSHEY_DUPLEX, 1.8, 4)[0]
                text_x = x1
                text_y = max(y1 - 15, 50)
                # Background rectangle for better visibility
                cv2.rectangle(annotated, (text_x - 5, text_y - text_size[1] - 5), 
                            (text_x + text_size[0] + 5, text_y + 5), (0, 0, 0), -1)
                cv2.putText(annotated, dist_text, (text_x, text_y), 
                           cv2.FONT_HERSHEY_DUPLEX, 1.8, (0, 255, 0), 4)
            
            # Guidance text at top
            error_x = cx - center_x
            if abs(error_x) < 50:
                guidance = "CENTERED - MOVE FORWARD"
                color = (0, 255, 0)
            elif error_x < -50:
                guidance = "<<< TURN LEFT"
                color = (0, 165, 255)
            else:
                guidance = "TURN RIGHT >>>"
                color = (0, 165, 255)
            
            cv2.putText(annotated, guidance, (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, color, 3)
            found = True
            break  # Only show first match
        
        if not found:
            search_text = f"SEARCHING FOR: {self.target_object}"
            if self.target_color:
                search_text += f" ({self.target_color})"
            cv2.putText(annotated, search_text, (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 2)
        
        return annotated, found

    def run_live(self):
        print("=== YOLOv8 Vision System Test ===")
        if not self.initialize_camera(0):
            print("Failed to initialize camera!")
            return
        print("Enter target object (e.g., 'phone', 'cup', 'laptop') and optional color (e.g., 'red'):")
        obj = input("Object: ")
        color = input("Color (or leave blank): ")
        self.set_target(obj, color if color else None)
        print("\nStarting live video. Press 'q' to quit.")
        while True:
            frame = self.capture_frame()
            if frame is None:
                break
            annotated, found = self.detect_and_annotate(frame)
            cv2.imshow("YOLOv8 Vision - Live", annotated)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        self.release_camera()
        print("=== YOLOv8 Vision Test Complete ===")

    def capture_frame(self):
        if not self.camera or not self.camera.isOpened():
            print("[YOLOVISION] - ERROR: Camera not initialized!")
            return None
        ret, frame = self.camera.read()
        if not ret:
            print("[YOLOVISION] - ERROR: Failed to capture frame!")
            return None
        return frame

if __name__ == "__main__":
    vision = YOLOVisionSystem()
    vision.run_live()
