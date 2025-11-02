# navigation.py
import time

class NavigationPlanner:
    """Generates high-level navigation plans and paths."""

    def __init__(self):
        self.breadcrumb_trail = []
        self.current_position = [0, 0]  # (x, y) in meters

    def generate_lawnmower_path(self, width_m: float, height_m: float, step_m: float) -> list:
        """
        Generates a list of (x, y) waypoints for a lawnmower search pattern.
        
        Args:
            width_m: The width of the search area in meters.
            height_m: The height of the search area in meters.
            step_m: The distance between parallel paths in meters.
        
        Returns:
            A list of (x, y) tuples representing the path.
        """
        waypoints = []
        y = 0
        direction = 1  # 1 for right, -1 for left

        while y <= height_m:
            if direction == 1:
                waypoints.append((0, y))
                waypoints.append((width_m, y))
            else:
                waypoints.append((width_m, y))
                waypoints.append((0, y))
            
            y += step_m
            direction *= -1
            
        print(f"[NAV] - Generated {len(waypoints)} waypoints for lawnmower search.")
        return waypoints

    def record_breadcrumb(self, position: tuple):
        """Records the robot's current position."""
        self.breadcrumb_trail.append(position)
        self.current_position = list(position)

    def get_return_path(self) -> list:
        """Returns the recorded path in reverse for homing."""
        if not self.breadcrumb_trail:
            return []
        
        return self.breadcrumb_trail[::-1]


class VisualServoing:
    """Handles visual servoing - using vision feedback to control robot movement."""
    
    def __init__(self, motor_controller=None):
        """
        Initialize visual servoing controller.
        
        Args:
            motor_controller: Instance of MotorController for movement
        """
        self.motor_controller = motor_controller
        
        # Control parameters
        self.center_tolerance_px = 50  # Pixel error tolerance for "centered"
        self.target_distance_cm = 30   # Stop when this close to object
        self.approach_speed = 0.3      # Speed when approaching (m/s)
        
        # PID-like gains for smooth control
        self.turn_gain = 0.1  # Degrees per pixel error
        
        print("[VISUAL_SERVO] - Visual Servoing controller initialized")
        
    def calculate_turn_angle(self, error_x_px):
        """
        Calculate how much to turn based on horizontal pixel error.
        
        Args:
            error_x_px: Horizontal error in pixels (positive = object is right)
            
        Returns:
            Turn angle in degrees (positive = turn right)
        """
        # Simple proportional control
        turn_angle = error_x_px * self.turn_gain
        
        # Limit maximum turn angle
        max_turn = 45
        turn_angle = max(-max_turn, min(max_turn, turn_angle))
        
        return turn_angle
        
    def is_centered(self, error_x_px):
        """
        Check if object is centered in frame.
        
        Args:
            error_x_px: Horizontal error in pixels
            
        Returns:
            True if centered within tolerance
        """
        return abs(error_x_px) < self.center_tolerance_px
        
    def is_at_target_distance(self, distance_cm):
        """
        Check if robot is at target distance from object.
        
        Args:
            distance_cm: Current distance to object in cm
            
        Returns:
            True if at target distance
        """
        if distance_cm is None:
            return False
        return distance_cm <= self.target_distance_cm
        
    def servo_to_target(self, vision_system, display=True):
        """
        Use visual servoing to approach the target object.
        This is the main control loop that centers and approaches the object.
        
        Args:
            vision_system: VisionSystem instance with camera initialized
            display: If True, show visual feedback window
            
        Returns:
            True if successfully reached target, False otherwise
        """
        print("[VISUAL_SERVO] - Starting visual servoing approach...")
        
        import cv2
        max_iterations = 100
        iteration = 0
        
        while iteration < max_iterations:
            # Capture frame
            frame = vision_system.capture_frame()
            if frame is None:
                print("[VISUAL_SERVO] - ERROR: Failed to capture frame!")
                return False
            
            # Detect object
            detection = vision_system.find_target_object(frame)
            
            if detection is None:
                print("[VISUAL_SERVO] - Lost sight of target! Stopping.")
                if self.motor_controller:
                    self.motor_controller.stop()
                return False
            
            # Calculate servoing error
            servo_error = vision_system.calculate_visual_servoing_error(frame, detection)
            
            error_x = servo_error['error_x']
            distance = servo_error.get('distance')
            
            # Display feedback
            if display:
                overlay = vision_system.draw_detection_overlay(frame, detection, servo_error)
                cv2.imshow("Visual Servoing", overlay)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            # Print status
            print(f"[VISUAL_SERVO] - Error: {error_x:+4d}px | Distance: {distance:.1f}cm" if distance else f"[VISUAL_SERVO] - Error: {error_x:+4d}px")
            
            # Check if we've reached the target
            if distance and self.is_at_target_distance(distance):
                print("[VISUAL_SERVO] - ✓ Reached target distance!")
                if self.motor_controller:
                    self.motor_controller.stop()
                if display:
                    cv2.destroyAllWindows()
                return True
            
            # Control logic
            if not self.is_centered(error_x):
                # Object is not centered - turn towards it
                turn_angle = self.calculate_turn_angle(error_x)
                
                if turn_angle > 0:
                    print(f"[VISUAL_SERVO] - Object RIGHT by {error_x}px → Turn RIGHT {abs(turn_angle):.1f}°")
                    if self.motor_controller:
                        self.motor_controller.turn_right(abs(turn_angle))
                    else:
                        print("[MOCK HARDWARE] - TURNING RIGHT")
                else:
                    print(f"[VISUAL_SERVO] - Object LEFT by {error_x}px → Turn LEFT {abs(turn_angle):.1f}°")
                    if self.motor_controller:
                        self.motor_controller.turn_left(abs(turn_angle))
                    else:
                        print("[MOCK HARDWARE] - TURNING LEFT")
            else:
                # Object is centered - move forward
                print(f"[VISUAL_SERVO] - Object CENTERED → Move FORWARD")
                if self.motor_controller:
                    self.motor_controller.move_forward(duration_s=0.5)
                else:
                    print("[MOCK HARDWARE] - MOVING FORWARD")
                    time.sleep(0.5)
            
            iteration += 1
            time.sleep(0.1)  # Small delay between control updates
        
        print("[VISUAL_SERVO] - Max iterations reached without reaching target")
        if display:
            cv2.destroyAllWindows()
        return False

# --- To test this script directly ---
if __name__ == "__main__":
    print("--- Testing Navigation Planner ---")
    planner = NavigationPlanner()
    
    # Test lawnmower path generation
    path = planner.generate_lawnmower_path(width_m=5, height_m=3, step_m=0.5)
    print("\nGenerated Path:")
    for point in path:
        print(f"  Go to: ({point[0]:.1f}, {point[1]:.1f})")
    
    # Test breadcrumb recording and reversal
    print("\n--- Testing Breadcrumb Trail ---")
    planner.record_breadcrumb((0,0))
    planner.record_breadcrumb((1,0))
    planner.record_breadcrumb((1,1))
    return_path = planner.get_return_path()
    print(f"Recorded Path: {planner.breadcrumb_trail}")
    print(f"Return Path: {return_path}")