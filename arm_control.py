# arm_control.py
"""
Robotic Arm Control Module for ATLAS Robot
Handles 4-DOF robotic arm with gripper for object manipulation
"""

import time

class RoboticArm:
    """Controls the 4-DOF robotic arm with gripper."""
    
    def __init__(self):
        """
        Initialize robotic arm controller.
        
        Hardware Setup (when connected):
        - 4-DOF robotic arm with 5 servo motors:
          * Base rotation servo (0-180°)
          * Shoulder servo (0-180°)
          * Elbow servo (0-180°)
          * Wrist servo (0-180°)
          * Gripper servo (0-180°, where 0=open, 180=closed)
        - PCA9685 16-channel PWM servo driver
        - Connected to Raspberry Pi via I2C (SDA, SCL pins)
        """
        self.is_hardware_connected = False
        
        # Servo channel assignments on PCA9685
        self.servo_channels = {
            'base': 0,
            'shoulder': 1,
            'elbow': 2,
            'wrist': 3,
            'gripper': 4
        }
        
        # Current servo positions (in degrees)
        self.servo_positions = {
            'base': 90,
            'shoulder': 90,
            'elbow': 90,
            'wrist': 90,
            'gripper': 0  # 0 = open
        }
        
        # Servo limits (min, max in degrees)
        self.servo_limits = {
            'base': (0, 180),
            'shoulder': (0, 180),
            'elbow': (0, 180),
            'wrist': (0, 180),
            'gripper': (0, 180)
        }
        
        # Pre-defined poses for common actions
        self.poses = {
            'home': {'base': 90, 'shoulder': 90, 'elbow': 90, 'wrist': 90, 'gripper': 0},
            'ready_to_grab': {'base': 90, 'shoulder': 45, 'elbow': 45, 'wrist': 0, 'gripper': 0},
            'grab': {'base': 90, 'shoulder': 45, 'elbow': 45, 'wrist': 0, 'gripper': 180},
            'lift': {'base': 90, 'shoulder': 90, 'elbow': 90, 'wrist': 45, 'gripper': 180},
            'present': {'base': 90, 'shoulder': 135, 'elbow': 45, 'wrist': 90, 'gripper': 180}
        }
        
        print("[ARM] - Robotic Arm initialized (Hardware simulation mode)")
        
    def initialize_hardware(self):
        """
        Initialize PCA9685 servo controller.
        
        When hardware is connected, this will:
        - Import Adafruit_PCA9685 library
        - Initialize I2C communication
        - Set PWM frequency (typically 50Hz for servos)
        - Move all servos to home position
        """
        # TODO: Uncomment when hardware is connected
        # import Adafruit_PCA9685
        # self.pwm = Adafruit_PCA9685.PCA9685()
        # self.pwm.set_pwm_freq(50)
        print("[MOCK HARDWARE] - PCA9685 servo controller initialized")
        self.move_to_pose('home')
        
    def _angle_to_pulse(self, angle):
        """
        Convert angle (0-180°) to PWM pulse length.
        
        Args:
            angle: Servo angle in degrees (0-180)
            
        Returns:
            Pulse length for PCA9685 (typically 150-600)
        """
        # Standard servo: 1ms (150) = 0°, 2ms (600) = 180°
        pulse = int(150 + (angle / 180.0) * 450)
        return pulse
        
    def set_servo_angle(self, servo_name, angle, smooth=True):
        """
        Set a single servo to a specific angle.
        
        Args:
            servo_name: Name of servo ('base', 'shoulder', 'elbow', 'wrist', 'gripper')
            angle: Target angle in degrees
            smooth: If True, move smoothly; if False, move directly
        """
        # Validate servo name
        if servo_name not in self.servo_channels:
            print(f"[ARM] - ERROR: Unknown servo '{servo_name}'")
            return
            
        # Clamp angle to limits
        min_angle, max_angle = self.servo_limits[servo_name]
        angle = max(min_angle, min(max_angle, angle))
        
        print(f"[MOCK HARDWARE] - Moving {servo_name.upper()} servo to {angle}°")
        
        # TODO: Hardware implementation
        # channel = self.servo_channels[servo_name]
        # pulse = self._angle_to_pulse(angle)
        # self.pwm.set_pwm(channel, 0, pulse)
        
        if smooth:
            # Simulate smooth movement
            current = self.servo_positions[servo_name]
            step = 5 if angle > current else -5
            
            for pos in range(int(current), int(angle), step):
                # In real hardware, this would send intermediate positions
                time.sleep(0.02)
            
        time.sleep(0.1)  # Wait for servo to reach position
        self.servo_positions[servo_name] = angle
        
    def move_to_pose(self, pose_name, smooth=True):
        """
        Move arm to a pre-defined pose.
        
        Args:
            pose_name: Name of the pose ('home', 'ready_to_grab', 'grab', 'lift', 'present')
            smooth: Move smoothly if True
        """
        if pose_name not in self.poses:
            print(f"[ARM] - ERROR: Unknown pose '{pose_name}'")
            return
            
        print(f"[ARM] - Moving to '{pose_name}' pose")
        pose = self.poses[pose_name]
        
        for servo_name, angle in pose.items():
            self.set_servo_angle(servo_name, angle, smooth=smooth)
            
        print(f"[ARM] - Reached '{pose_name}' pose")
        
    def grab_object(self):
        """Execute a complete grab sequence."""
        print("[ARM] - Executing GRAB sequence...")
        
        # Step 1: Position arm ready to grab
        print("[ARM] - Step 1: Positioning for grab")
        self.move_to_pose('ready_to_grab')
        time.sleep(0.5)
        
        # Step 2: Close gripper
        print("[ARM] - Step 2: Closing gripper")
        self.set_servo_angle('gripper', 180)
        time.sleep(0.5)
        
        # Step 3: Lift object
        print("[ARM] - Step 3: Lifting object")
        self.move_to_pose('lift')
        time.sleep(0.5)
        
        print("[ARM] - GRAB sequence complete!")
        
    def release_object(self):
        """Release the currently held object."""
        print("[ARM] - Releasing object...")
        self.set_servo_angle('gripper', 0)  # Open gripper
        time.sleep(0.5)
        print("[ARM] - Object released")
        
    def present_object(self):
        """Move to present position (offering object to user)."""
        print("[ARM] - Presenting object to user...")
        self.move_to_pose('present')
        
    def return_to_home(self):
        """Return arm to home position."""
        print("[ARM] - Returning to home position...")
        self.move_to_pose('home')
        
    def reach_to_position(self, x, y, z):
        """
        Calculate inverse kinematics and reach to a 3D position.
        This is a simplified version - full IK is complex!
        
        Args:
            x: X coordinate in cm relative to base
            y: Y coordinate in cm relative to base
            z: Z coordinate in cm (height)
        """
        print(f"[ARM] - Calculating reach to position ({x}, {y}, {z})")
        
        # TODO: Implement proper inverse kinematics
        # For now, use a simplified approach
        
        # Calculate base rotation
        import math
        base_angle = math.degrees(math.atan2(y, x))
        base_angle = base_angle + 90  # Adjust for 0° = forward
        
        # Calculate arm extension needed
        horizontal_dist = math.sqrt(x**2 + y**2)
        
        # Simplified arm positioning (would need proper IK in reality)
        shoulder_angle = 45
        elbow_angle = 45
        wrist_angle = 0
        
        print(f"[ARM] - IK Solution: Base={base_angle:.1f}°, Shoulder={shoulder_angle}°, Elbow={elbow_angle}°")
        
        self.set_servo_angle('base', base_angle)
        self.set_servo_angle('shoulder', shoulder_angle)
        self.set_servo_angle('elbow', elbow_angle)
        self.set_servo_angle('wrist', wrist_angle)


class GripperController:
    """Specialized controller for gripper operations."""
    
    def __init__(self, arm):
        """
        Initialize gripper controller.
        
        Args:
            arm: RoboticArm instance
        """
        self.arm = arm
        self.is_holding = False
        
    def open_gripper(self):
        """Fully open the gripper."""
        print("[GRIPPER] - Opening gripper")
        self.arm.set_servo_angle('gripper', 0)
        self.is_holding = False
        
    def close_gripper(self, force='medium'):
        """
        Close the gripper with specified force.
        
        Args:
            force: 'light', 'medium', or 'firm'
        """
        force_angles = {
            'light': 120,
            'medium': 150,
            'firm': 180
        }
        
        angle = force_angles.get(force, 150)
        print(f"[GRIPPER] - Closing gripper with {force} force ({angle}°)")
        self.arm.set_servo_angle('gripper', angle)
        self.is_holding = True
        
    def check_grip(self):
        """
        Check if object is securely held.
        In a real system, this could use force sensors or current sensing.
        
        Returns:
            True if object is held, False otherwise
        """
        # TODO: Implement with actual sensors
        # Could use servo current draw to detect if gripper is holding something
        print("[MOCK HARDWARE] - Checking grip status via current sensing")
        return self.is_holding


# --- To test this script directly ---
if __name__ == "__main__":
    print("=== Testing Robotic Arm Control System ===\n")
    
    arm = RoboticArm()
    gripper = GripperController(arm)
    
    print("\n--- Test 1: Basic Servo Control ---")
    arm.set_servo_angle('base', 45)
    arm.set_servo_angle('shoulder', 60)
    arm.set_servo_angle('elbow', 90)
    
    print("\n--- Test 2: Pre-defined Poses ---")
    arm.move_to_pose('home')
    time.sleep(1)
    arm.move_to_pose('ready_to_grab')
    time.sleep(1)
    
    print("\n--- Test 3: Grab Sequence ---")
    arm.grab_object()
    time.sleep(1)
    
    print("\n--- Test 4: Present and Release ---")
    arm.present_object()
    time.sleep(1)
    gripper.open_gripper()
    
    print("\n--- Test 5: Return Home ---")
    arm.return_to_home()
    
    print("\n--- Test 6: Inverse Kinematics Test ---")
    arm.reach_to_position(x=15, y=10, z=5)
    
    print("\n=== Robotic Arm Test Complete ===")
