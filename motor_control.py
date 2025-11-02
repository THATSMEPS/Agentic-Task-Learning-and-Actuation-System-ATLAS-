# motor_control.py
"""
Motor Control Module for ATLAS Robot
Handles 4-wheel drive chassis movement and obstacle avoidance
"""

import time

class MotorController:
    """Controls the 4-wheel drive system for ATLAS."""
    
    def __init__(self):
        """
        Initialize motor controller.
        
        Hardware Setup (when connected):
        - 4 DC motors connected to L298N motor driver
        - L298N connected to Raspberry Pi GPIO pins:
          * Motor 1 (Front Left): IN1, IN2, ENA
          * Motor 2 (Front Right): IN3, IN4, ENB
          * Motor 3 (Back Left): IN1, IN2, ENA (second L298N if needed)
          * Motor 4 (Back Right): IN3, IN4, ENB
        """
        self.is_hardware_connected = False
        self.current_speed = 0
        self.position = [0, 0]  # Track approximate position (x, y) in meters
        self.heading = 0  # Track heading in degrees (0 = North/Forward)
        
        # Simulation parameters
        self.base_speed = 0.5  # meters per second
        self.turn_rate = 45  # degrees per second
        
        print("[MOTOR] - Motor Controller initialized (Hardware simulation mode)")
        
    def initialize_hardware(self):
        """
        Initialize GPIO pins for motor control.
        
        When hardware is connected, this will:
        - Import RPi.GPIO library
        - Set GPIO mode and pin numbers
        - Initialize PWM for speed control
        """
        # TODO: Uncomment when hardware is connected
        # import RPi.GPIO as GPIO
        # GPIO.setmode(GPIO.BCM)
        # # Setup pins for motors...
        print("[MOCK HARDWARE] - GPIO pins configured for motor control")
        
    def move_forward(self, distance_m=None, duration_s=1.0):
        """
        Move the robot forward.
        
        Args:
            distance_m: Distance to move in meters (if None, uses duration)
            duration_s: Time to move in seconds
        """
        print(f"[MOCK HARDWARE] - MOVING FORWARD for {duration_s:.2f}s")
        # TODO: Hardware implementation
        # GPIO.output(MOTOR_IN1, GPIO.HIGH)
        # GPIO.output(MOTOR_IN2, GPIO.LOW)
        # PWM_LEFT.ChangeDutyCycle(75)
        # PWM_RIGHT.ChangeDutyCycle(75)
        
        time.sleep(duration_s)
        
        # Update simulated position
        distance = distance_m if distance_m else (self.base_speed * duration_s)
        self.position[0] += distance * self._cos_deg(self.heading)
        self.position[1] += distance * self._sin_deg(self.heading)
        
        self.stop()
        
    def move_backward(self, distance_m=None, duration_s=1.0):
        """Move the robot backward."""
        print(f"[MOCK HARDWARE] - MOVING BACKWARD for {duration_s:.2f}s")
        # TODO: Hardware implementation
        # GPIO.output(MOTOR_IN1, GPIO.LOW)
        # GPIO.output(MOTOR_IN2, GPIO.HIGH)
        
        time.sleep(duration_s)
        
        distance = distance_m if distance_m else (self.base_speed * duration_s)
        self.position[0] -= distance * self._cos_deg(self.heading)
        self.position[1] -= distance * self._sin_deg(self.heading)
        
        self.stop()
        
    def turn_left(self, degrees=90, duration_s=None):
        """
        Turn the robot left (counter-clockwise).
        
        Args:
            degrees: Angle to turn in degrees
            duration_s: Time to turn (calculated from degrees if None)
        """
        turn_time = duration_s if duration_s else (degrees / self.turn_rate)
        print(f"[MOCK HARDWARE] - TURNING LEFT {degrees}° (duration: {turn_time:.2f}s)")
        
        # TODO: Hardware implementation
        # Left motors backward, right motors forward
        # GPIO.output(LEFT_IN1, GPIO.LOW)
        # GPIO.output(LEFT_IN2, GPIO.HIGH)
        # GPIO.output(RIGHT_IN1, GPIO.HIGH)
        # GPIO.output(RIGHT_IN2, GPIO.LOW)
        
        time.sleep(turn_time)
        self.heading = (self.heading - degrees) % 360
        self.stop()
        
    def turn_right(self, degrees=90, duration_s=None):
        """
        Turn the robot right (clockwise).
        
        Args:
            degrees: Angle to turn in degrees
            duration_s: Time to turn (calculated from degrees if None)
        """
        turn_time = duration_s if duration_s else (degrees / self.turn_rate)
        print(f"[MOCK HARDWARE] - TURNING RIGHT {degrees}° (duration: {turn_time:.2f}s)")
        
        # TODO: Hardware implementation
        # Left motors forward, right motors backward
        
        time.sleep(turn_time)
        self.heading = (self.heading + degrees) % 360
        self.stop()
        
    def stop(self):
        """Stop all motors."""
        print("[MOCK HARDWARE] - MOTORS STOPPED")
        # TODO: Hardware implementation
        # GPIO.output all motor pins to LOW
        # PWM.ChangeDutyCycle(0)
        
        self.current_speed = 0
        
    def navigate_to_point(self, target_x, target_y):
        """
        Navigate to a specific point in the room.
        
        Args:
            target_x: Target X coordinate in meters
            target_y: Target Y coordinate in meters
        """
        print(f"[MOTOR] - Navigating from {self.position} to ({target_x}, {target_y})")
        
        # Calculate angle to target
        dx = target_x - self.position[0]
        dy = target_y - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        target_angle = self._atan2_deg(dy, dx)
        
        # Calculate turn needed
        angle_diff = (target_angle - self.heading + 180) % 360 - 180
        
        # Turn towards target
        if abs(angle_diff) > 5:  # 5 degree threshold
            if angle_diff > 0:
                self.turn_left(abs(angle_diff))
            else:
                self.turn_right(abs(angle_diff))
        
        # Move forward
        move_time = distance / self.base_speed
        self.move_forward(distance_m=distance, duration_s=move_time)
        
        print(f"[MOTOR] - Arrived at destination. Current position: {self.position}")


class ObstacleAvoidance:
    """Handles obstacle detection and avoidance using ultrasonic sensors."""
    
    def __init__(self):
        """
        Initialize obstacle avoidance system.
        
        Hardware Setup (when connected):
        - 3-4 HC-SR04 ultrasonic sensors mounted on front and sides
        - Connected to Raspberry Pi GPIO (TRIG and ECHO pins)
        - Typical range: 2cm - 400cm
        """
        self.sensors = {
            'front': {'trig_pin': 23, 'echo_pin': 24},
            'left': {'trig_pin': 27, 'echo_pin': 22},
            'right': {'trig_pin': 17, 'echo_pin': 18}
        }
        self.min_safe_distance = 0.3  # 30cm minimum safe distance
        
        print("[OBSTACLE] - Obstacle Avoidance initialized (Hardware simulation mode)")
        
    def get_distance(self, sensor_name='front'):
        """
        Get distance reading from ultrasonic sensor.
        
        Args:
            sensor_name: Which sensor to read ('front', 'left', 'right')
            
        Returns:
            Distance in meters
        """
        # TODO: Hardware implementation
        # GPIO.output(TRIG, GPIO.HIGH)
        # time.sleep(0.00001)
        # GPIO.output(TRIG, GPIO.LOW)
        # pulse_duration = echo_time_end - echo_time_start
        # distance = (pulse_duration * 34300) / 2  # Speed of sound
        
        # Simulate random distances for testing
        import random
        distance = random.uniform(0.5, 2.0)
        print(f"[MOCK HARDWARE] - {sensor_name.upper()} ultrasonic sensor reads: {distance:.2f}m")
        return distance
        
    def is_path_clear(self, sensor_name='front'):
        """
        Check if path is clear for movement.
        
        Args:
            sensor_name: Which sensor to check
            
        Returns:
            True if path is clear, False if obstacle detected
        """
        distance = self.get_distance(sensor_name)
        is_clear = distance > self.min_safe_distance
        
        if not is_clear:
            print(f"[OBSTACLE] - WARNING: Obstacle detected {distance:.2f}m away on {sensor_name} sensor!")
        
        return is_clear
        
    def avoid_obstacle(self, motor_controller):
        """
        Execute obstacle avoidance maneuver.
        
        Args:
            motor_controller: MotorController instance
        """
        print("[OBSTACLE] - Executing obstacle avoidance maneuver...")
        
        motor_controller.stop()
        motor_controller.move_backward(duration_s=0.5)
        
        # Check left and right
        left_clear = self.is_path_clear('left')
        right_clear = self.is_path_clear('right')
        
        if left_clear and not right_clear:
            print("[OBSTACLE] - Turning left to avoid obstacle")
            motor_controller.turn_left(45)
        elif right_clear and not left_clear:
            print("[OBSTACLE] - Turning right to avoid obstacle")
            motor_controller.turn_right(45)
        elif left_clear and right_clear:
            print("[OBSTACLE] - Both sides clear, choosing left")
            motor_controller.turn_left(45)
        else:
            print("[OBSTACLE] - No clear path, turning around")
            motor_controller.turn_right(180)


    # Helper methods for angle calculations
    def _cos_deg(self, degrees):
        """Cosine in degrees."""
        import math
        return math.cos(math.radians(degrees))
        
    def _sin_deg(self, degrees):
        """Sine in degrees."""
        import math
        return math.sin(math.radians(degrees))
        
    def _atan2_deg(self, y, x):
        """Atan2 returning degrees."""
        import math
        return math.degrees(math.atan2(y, x))


# Add helper methods to MotorController
MotorController._cos_deg = ObstacleAvoidance._cos_deg
MotorController._sin_deg = ObstacleAvoidance._sin_deg
MotorController._atan2_deg = ObstacleAvoidance._atan2_deg


# --- To test this script directly ---
if __name__ == "__main__":
    print("=== Testing Motor Control System ===\n")
    
    motors = MotorController()
    obstacles = ObstacleAvoidance()
    
    print("\n--- Test 1: Basic Movement ---")
    motors.move_forward(duration_s=2.0)
    motors.turn_right(90)
    motors.move_forward(duration_s=1.0)
    motors.turn_left(45)
    
    print(f"\n--- Current Position: {motors.position}, Heading: {motors.heading}° ---")
    
    print("\n--- Test 2: Obstacle Detection ---")
    if obstacles.is_path_clear('front'):
        motors.move_forward(duration_s=1.0)
    else:
        obstacles.avoid_obstacle(motors)
    
    print("\n--- Test 3: Navigate to Point ---")
    motors.navigate_to_point(2.0, 3.0)
    
    print("\n=== Motor Control Test Complete ===")
