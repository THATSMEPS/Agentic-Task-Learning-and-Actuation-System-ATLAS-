# vision.py
import cv2
import numpy as np
import config

class VisionSystem:
    """Handles all computer vision tasks for ATLAS."""

    def __init__(self, use_laptop_camera=True):
        """
        Initialize vision system.
        
        Args:
            use_laptop_camera: If True, uses laptop camera (index 0), else uses Pi camera
        """
        self.use_laptop_camera = use_laptop_camera
        self.camera = None
        self.target_object_description = None
        self.target_color = None
        
        # HSV color ranges for various colors
        self.color_ranges = {
            'red': [
                ([0, 120, 70], [10, 255, 255]),
                ([170, 120, 70], [180, 255, 255])
            ],
            'blue': [
                ([100, 150, 0], [140, 255, 255])
            ],
            'green': [
                ([40, 40, 40], [80, 255, 255])
            ],
            'yellow': [
                ([20, 100, 100], [30, 255, 255])
            ],
            'orange': [
                ([10, 100, 20], [25, 255, 255])
            ],
            'purple': [
                ([130, 50, 50], [160, 255, 255])
            ],
            'white': [
                ([0, 0, 200], [180, 30, 255])
            ],
            'black': [
                ([0, 0, 0], [180, 255, 30])
            ]
        }
        
        # Distance estimation calibration
        # These values need calibration with actual objects
        self.known_object_sizes = {
            'phone': 15,  # cm width
            'book': 20,   # cm width
            'pen': 1.5,   # cm width
            'ball': 10,   # cm diameter
            'cup': 8,     # cm diameter
            'bottle': 7,  # cm diameter
            'tool': 15,   # cm average width
            'box': 20,    # cm average width
        }
        
        # Camera focal length (needs calibration for your specific camera)
        # This is an approximation - measure with a known object at known distance
        self.focal_length = 600  # pixels
        
        print("[VISION] - Vision System initialized")
        if use_laptop_camera:
            print("[VISION] - Using laptop camera for testing")

    def initialize_camera(self, camera_index=0):
        """
        Initialize the camera.
        
        Args:
            camera_index: Camera index (0 for laptop webcam, varies for USB cameras)
        """
        self.camera = cv2.VideoCapture(camera_index)
        
        if not self.camera.isOpened():
            print("[VISION] - ERROR: Could not open camera!")
            return False
            
        # Set camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        
        print(f"[VISION] - Camera {camera_index} initialized successfully")
        return True
        
    def release_camera(self):
        """Release the camera resource."""
        if self.camera:
            self.camera.release()
            cv2.destroyAllWindows()
            print("[VISION] - Camera released")
            
    def capture_frame(self):
        """
        Capture a single frame from the camera.
        
        Returns:
            Frame as numpy array, or None if failed
        """
        if not self.camera or not self.camera.isOpened():
            print("[VISION] - ERROR: Camera not initialized!")
            return None
            
        ret, frame = self.camera.read()
        if not ret:
            print("[VISION] - ERROR: Failed to capture frame!")
            return None
            
        return frame
        
    def set_target_object(self, object_description, object_color=None):
        """
        Set the target object to search for.
        
        Args:
            object_description: Description of the object (e.g., "blue phone", "red book")
            object_color: Primary color of the object (extracted from description if not provided)
        """
        self.target_object_description = object_description.lower()
        
        # Extract color from description if not provided
        if object_color is None:
            for color in self.color_ranges.keys():
                if color in self.target_object_description:
                    self.target_color = color
                    break
        else:
            self.target_color = object_color.lower()
            
        print(f"[VISION] - Target set: '{object_description}' with primary color '{self.target_color}'")

    def find_target_object(self, frame):
        """
        Finds the target object in a given frame using color detection.
        
        Args:
            frame: A single video frame from OpenCV.
            
        Returns:
            A dictionary {'centroid': (x, y), 'area': area, 'distance': distance_cm} 
            if the object is found, otherwise None.
        """
        if self.target_color is None:
            print("[VISION] - ERROR: No target color set! Call set_target_object() first.")
            return None
            
        # Convert the frame to the HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get color ranges for target color
        color_masks = self.color_ranges.get(self.target_color, [])
        
        if not color_masks:
            print(f"[VISION] - WARNING: Unknown color '{self.target_color}', using default red")
            color_masks = self.color_ranges['red']
        
        # Create combined mask for all ranges of this color
        mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
        for lower, upper in color_masks:
            mask_part = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))
            mask = cv2.bitwise_or(mask, mask_part)
        
        # Apply morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour by area
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)

            # Only consider contours with a reasonably large area to filter out noise
            if area > 500:
                # Calculate the centroid (center) of the contour
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Estimate distance
                    distance_cm = self.estimate_distance(largest_contour)
                    
                    return {
                        'centroid': (cx, cy), 
                        'area': area, 
                        'contour': largest_contour,
                        'distance': distance_cm
                    }
        
        return None
        
    def estimate_distance(self, contour):
        """
        Estimate distance to object using pixel size.
        
        Args:
            contour: The contour of the detected object
            
        Returns:
            Estimated distance in centimeters
        """
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        pixel_width = w
        
        # Estimate real-world width based on object type
        real_width = 10  # default 10cm
        
        # Try to match object type from description
        if self.target_object_description:
            for obj_type, size in self.known_object_sizes.items():
                if obj_type in self.target_object_description:
                    real_width = size
                    break
        
        # Distance = (Real Width × Focal Length) / Pixel Width
        if pixel_width > 0:
            distance = (real_width * self.focal_length) / pixel_width
            return distance
        
        return None
        
    def calculate_visual_servoing_error(self, frame, detection_result):
        """
        Calculate the error for visual servoing control.
        
        Args:
            frame: Current video frame
            detection_result: Result from find_target_object()
            
        Returns:
            Dictionary with error_x, error_y, and distance
        """
        if detection_result is None:
            return None
            
        # Image center
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        
        # Object center
        obj_x, obj_y = detection_result['centroid']
        
        # Calculate errors (positive = object is to the right/down)
        error_x = obj_x - center_x
        error_y = obj_y - center_y
        
        # Calculate distance
        distance = detection_result.get('distance', None)
        
        return {
            'error_x': error_x,
            'error_y': error_y,
            'distance': distance,
            'frame_center': (center_x, center_y),
            'object_center': (obj_x, obj_y)
        }
        
    def draw_detection_overlay(self, frame, detection_result, servoing_error=None):
        """
        Draw visual feedback on the frame.
        
        Args:
            frame: Video frame to draw on
            detection_result: Result from find_target_object()
            servoing_error: Result from calculate_visual_servoing_error()
            
        Returns:
            Frame with overlay
        """
        overlay = frame.copy()
        
        # Draw frame center crosshair (blue)
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        cv2.drawMarker(overlay, (center_x, center_y), (255, 0, 0), 
                      cv2.MARKER_CROSS, 20, 2)
        cv2.putText(overlay, "CENTER", (center_x - 30, center_y - 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        if detection_result:
            # Draw bounding box (green)
            x, y, w, h = cv2.boundingRect(detection_result['contour'])
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Draw centroid (red dot)
            cx, cy = detection_result['centroid']
            cv2.circle(overlay, (cx, cy), 7, (0, 0, 255), -1)
            
            # Draw line from center to object (yellow)
            cv2.line(overlay, (center_x, center_y), (cx, cy), (255, 255, 0), 2)
            
            # === DISTANCE - Make it LARGE and PROMINENT ===
            if detection_result.get('distance'):
                distance_text = f"{detection_result['distance']:.1f} cm"
                # Large text on the bounding box
                cv2.putText(overlay, distance_text, (x, y - 15), 
                           cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 3)
            
            # Other information (smaller text)
            info_y = y + h + 25
            cv2.putText(overlay, f"Target: {self.target_object_description}", 
                       (x, info_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            if servoing_error:
                # Show direction guidance
                error_x = servoing_error['error_x']
                if error_x < -50:
                    direction = "<<< TURN LEFT"
                    color = (0, 165, 255)  # Orange
                elif error_x > 50:
                    direction = "TURN RIGHT >>>"
                    color = (0, 165, 255)  # Orange
                else:
                    direction = "CENTERED - GO FORWARD"
                    color = (0, 255, 0)  # Green
                    
                cv2.putText(overlay, direction, (10, 30), 
                           cv2.FONT_HERSHEY_DUPLEX, 0.8, color, 2)
        else:
            # Show searching message
            cv2.putText(overlay, f"SEARCHING FOR: {self.target_object_description}", 
                       (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255), 2)
        
        return overlay


# --- To test this script directly ---
if __name__ == "__main__":
    print("=== Testing Vision System ===")
    print("This test will use your laptop camera.")
    print("Commands:")
    print("  'q' - Quit")
    print("  's' - Set new target object")
    print()
    
    vision = VisionSystem(use_laptop_camera=True)
    
    # Initialize laptop camera
    if not vision.initialize_camera(0):
        print("Failed to initialize camera!")
        exit(1)
    
    # Set initial target
    target = input("Enter target object (e.g., 'blue phone', 'red cup', 'green book'): ")
    vision.set_target_object(target)
    
    print("\nStarting camera feed. Point camera at target object...")
    print("=" * 60)
    print("CONTROLS:")
    print("  'q' - Quit")
    print("  's' - Change target object")
    print("=" * 60)
    print("\n** WATCH THE VIDEO WINDOW - Distance shows on green box **\n")
    
    frame_count = 0
    while True:
        frame = vision.capture_frame()
        
        if frame is None:
            print("[ERROR] Failed to capture frame!")
            break
        
        # Find the object
        result = vision.find_target_object(frame)
        
        # Calculate servoing error if object found
        servoing_error = None
        if result:
            servoing_error = vision.calculate_visual_servoing_error(frame, result)
            
            # Print status every 30 frames (once per second) to avoid spam
            if frame_count % 30 == 0:
                direction = "CENTERED"
                if servoing_error['error_x'] < -50:
                    direction = "LEFT"
                elif servoing_error['error_x'] > 50:
                    direction = "RIGHT"
                    
                if servoing_error['distance']:
                    print(f"[VISION] Object: {direction:8s} | Distance: {servoing_error['distance']:5.1f} cm")
                else:
                    print(f"[VISION] Object: {direction:8s} | Distance: Unknown")
        else:
            # Only print "searching" message occasionally
            if frame_count % 90 == 0:  # Every 3 seconds
                print("[VISION] Searching for target object...")
        
        # Draw overlay with distance on bounding box
        display_frame = vision.draw_detection_overlay(frame, result, servoing_error)
        
        # Show the video feed
        cv2.imshow("ATLAS Vision System - Press 'q' to quit, 's' to change target", display_frame)
        
        frame_count += 1
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            vision.release_camera()
            cv2.destroyAllWindows()
            target = input("\nEnter new target object: ")
            vision.set_target_object(target)
            vision.initialize_camera(0)
            print("Camera feed resumed...")
    
    vision.release_camera()
    print("\n=== Vision System Test Complete ===")
