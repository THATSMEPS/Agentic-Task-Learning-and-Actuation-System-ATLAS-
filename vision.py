# vision.py
import cv2
import numpy as np
import config

class VisionSystem:
    """Handles all computer vision tasks for ATLAS."""

    def __init__(self):
        # You can initialize any parameters here if needed later
        pass

    def find_target_object(self, frame):
        """
        Finds the target object in a given frame based on configured HSV values.
        
        Args:
            frame: A single video frame from OpenCV.
            
        Returns:
            A dictionary {'centroid': (x, y), 'area': area} if the object is found,
            otherwise None.
        """
        # Convert the frame to the HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create masks for the red color range
        mask1 = cv2.inRange(hsv_frame, np.array(config.RED_LOWER), np.array(config.RED_UPPER))
        mask2 = cv2.inRange(hsv_frame, np.array(config.RED_LOWER_2), np.array(config.RED_UPPER_2))
        
        # Combine the two masks
        mask = mask1 + mask2
        
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
                    return {'centroid': (cx, cy), 'area': area, 'contour': largest_contour}
        
        return None

# --- To test this script directly ---
if __name__ == "__main__":
    print("--- Testing Vision System ---")
    print("Press 'q' to quit.")
    
    # IMPORTANT: Replace with the path to your own test video!
    video_path = 'test_videos/sample1.mp4' 
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        print("Please make sure you have a video file in the '/test_videos/' folder.")
    else:
        vision = VisionSystem()
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # Loop the video
                continue

            frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
            
            # Find the object
            result = vision.find_target_object(frame)
            
            if result:
                # Draw a bounding box and centroid on the frame for visualization
                x, y, w, h = cv2.boundingRect(result['contour'])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, result['centroid'], 5, (0, 0, 255), -1)
                cv2.putText(frame, f"Area: {int(result['area'])}", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Vision System Test", frame)

            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()