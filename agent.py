# agent.py
import time
from enum import Enum
import cv2
import config
from vision import VisionSystem
from navigation import NavigationPlanner, VisualServoing
from llm_interface import get_plan_from_command, extract_object_info
from motor_control import MotorController, ObstacleAvoidance
from arm_control import RoboticArm, GripperController
from speech_interface import VoiceInterface

class AgentState(Enum):
    """Defines the possible states for our robot agent."""
    IDLE = 1
    LISTENING = 2
    PLANNING = 3
    SEARCHING = 4
    APPROACHING = 5
    GRASPING = 6
    RETURNING = 7
    TASK_COMPLETE = 8

class Agent:
    """The main agent class that orchestrates the robot's behavior."""

    def __init__(self, use_voice=False, use_laptop_camera=True):
        """
        Initialize ATLAS agent.
        
        Args:
            use_voice: If True, use voice interface for commands
            use_laptop_camera: If True, use laptop camera instead of Pi camera
        """
        self.state = AgentState.IDLE
        self.use_voice = use_voice
        
        # Initialize all subsystems
        print("[AGENT] - Initializing ATLAS subsystems...")
        
        self.vision = VisionSystem(use_laptop_camera=use_laptop_camera)
        self.nav_planner = NavigationPlanner()
        self.motors = MotorController()
        self.obstacles = ObstacleAvoidance()
        self.arm = RoboticArm()
        self.gripper = GripperController(self.arm)
        self.visual_servo = VisualServoing(self.motors)
        
        if use_voice:
            self.voice = VoiceInterface()
            self.voice.initialize()
        else:
            self.voice = None
        
        self.current_plan = {}
        self.current_command = ""
        
        print("[AGENT] - ✓ ATLAS subsystems initialized")

    def run(self):
        """The main loop of the agent's state machine."""
        print("\n" + "="*60)
        print("   ATLAS - Agentic Task Learning and Actuation System")
        print("              Robot Assistant v1.0")
        print("="*60)
        print("\n[AGENT] - ATLAS is online and awaiting commands.")
        
        while True:
            try:
                if self.state == AgentState.IDLE:
                    self._idle_state()
                elif self.state == AgentState.PLANNING:
                    self._planning_state()
                elif self.state == AgentState.SEARCHING:
                    self._searching_state()
                elif self.state == AgentState.APPROACHING:
                    self._approaching_state()
                elif self.state == AgentState.GRASPING:
                    self._grasping_state()
                elif self.state == AgentState.RETURNING:
                    self._returning_state()
                elif self.state == AgentState.TASK_COMPLETE:
                    self._task_complete_state()
                
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\n\n[AGENT] - Shutdown signal received. Stopping ATLAS...")
                self._shutdown()
                break
            except Exception as e:
                print(f"\n[AGENT] - ERROR: {e}")
                print("[AGENT] - Returning to IDLE state")
                self.state = AgentState.IDLE

    def _idle_state(self):
        """Idle state - waiting for user command."""
        if self.voice:
            # Voice-activated mode
            print("\n[AGENT] - Say 'ATLAS' followed by your command...")
            command = self.voice.get_voice_command("atlas")
            if command:
                self.current_command = command
                self.state = AgentState.PLANNING
        else:
            # Text input mode
            command = input("\n[AGENT] - Enter a command (or 'quit' to exit): ")
            if command.lower() in ['quit', 'exit', 'q']:
                self._shutdown()
                exit(0)
            self.current_command = command
            self.state = AgentState.PLANNING


    def _planning_state(self):
        """Planning state - analyze command and create execution plan."""
        print(f"\n[AGENT] - Planning task for command: '{self.current_command}'")
        
        if self.voice:
            self.voice.respond("I am analyzing your request")
        
        # Try to get plan from LLM
        try:
            if config.GEMINI_API_KEY:
                self.current_plan = get_plan_from_command(self.current_command)
            else:
                print("[AGENT] - No API key found, using fallback extraction")
                self.current_plan = extract_object_info(self.current_command)
        except Exception as e:
            print(f"[AGENT] - Planning error: {e}")
            self.current_plan = None
        
        if self.current_plan:
            obj_desc = self.current_plan.get('object_description')
            obj_color = self.current_plan.get('object_color')
            action = self.current_plan.get('action')
            
            print(f"[AGENT] - ✓ Plan created:")
            print(f"          Action: {action}")
            print(f"          Target: {obj_desc}")
            print(f"          Color: {obj_color}")
            
            # Set vision system target
            self.vision.set_target_object(obj_desc, obj_color)
            
            if self.voice:
                self.voice.respond(f"I will {action} the {obj_desc}")
            
            # Initialize camera
            if self.vision.initialize_camera(0):
                self.state = AgentState.SEARCHING
            else:
                print("[AGENT] - Failed to initialize camera!")
                self.state = AgentState.IDLE
        else:
            print("[AGENT] - Planning failed. Returning to IDLE.")
            if self.voice:
                self.voice.respond("I didn't understand that command")
            self.state = AgentState.IDLE
            
    def _searching_state(self):
        """Searching state - look for the target object using lawnmower pattern."""
        print(f"\n[AGENT] - SEARCHING for '{self.current_plan.get('object_description')}'...")
        print("[AGENT] - Video feed window will open - point camera at target object!")
        print("[AGENT] - Press 'q' to abort search")
        
        if self.voice:
            self.voice.respond(f"Searching for {self.current_plan.get('object_description')}", async_speech=True)
        
        # In simulation mode, we search by continuously monitoring camera
        # On real robot, this would execute lawnmower pattern
        if self.use_laptop_camera:
            # LAPTOP MODE: Continuous camera monitoring (smooth video)
            print("[AGENT] - SIMULATION MODE: Point camera at object to detect it")
            
            object_found = False
            frame_count = 0
            
            while not object_found:
                # Capture and process frame
                frame = self.vision.capture_frame()
                if frame is not None:
                    detection = self.vision.find_target_object(frame)
                    servoing_error = None
                    
                    if detection:
                        servoing_error = self.vision.calculate_visual_servoing_error(frame, detection)
                        print(f"[AGENT] - ✓ OBJECT DETECTED!")
                        print(f"[AGENT] - Estimated distance: {detection.get('distance', 'unknown')} cm")
                        
                        if self.voice:
                            self.voice.respond("I found it! Approaching now", async_speech=True)
                        
                        object_found = True
                        # Show detection for 1 second before approaching
                        display_frame = self.vision.draw_detection_overlay(frame, detection, servoing_error)
                        cv2.imshow("ATLAS Searching - Object Found!", display_frame)
                        cv2.waitKey(1000)
                        self.state = AgentState.APPROACHING
                        break
                    
                    # Display live feed during search (smooth like vision.py)
                    display_frame = self.vision.draw_detection_overlay(frame, detection, servoing_error)
                    cv2.imshow("ATLAS Searching - Press 'q' to abort", display_frame)
                    
                    # Print searching status occasionally
                    if frame_count % 90 == 0:
                        print("[AGENT] - Searching... (point camera at target)")
                    
                    frame_count += 1
                    
                    # Check if user wants to abort (minimal delay for smooth video)
                    key = cv2.waitKey(30) & 0xFF
                    if key == ord('q'):
                        print("[AGENT] - Search aborted by user")
                        object_found = False
                        break
                else:
                    print("[AGENT] - ERROR: Failed to capture frame")
                    break
            
            if not object_found:
                print("[AGENT] - Search aborted. Returning to IDLE.")
                self.vision.release_camera()
                self.state = AgentState.IDLE
                
        else:
            # REAL ROBOT MODE: Execute lawnmower search pattern
            waypoints = self.nav_planner.generate_lawnmower_path(5, 3, 0.5)
            
            object_found = False
            for i, point in enumerate(waypoints):
                print(f"[AGENT] - Moving to search waypoint {i+1}/{len(waypoints)}: {point}")
                
                # Check for obstacles before moving
                if not self.obstacles.is_path_clear('front'):
                    print("[AGENT] - Obstacle detected during search!")
                    self.obstacles.avoid_obstacle(self.motors)
                
                # Navigate to waypoint
                self.motors.navigate_to_point(point[0], point[1])
                self.nav_planner.record_breadcrumb(point)
                
                # Look for object at this location
                frame = self.vision.capture_frame()
                if frame is not None:
                    detection = self.vision.find_target_object(frame)
                    
                    if detection:
                        print(f"[AGENT] - ✓ OBJECT DETECTED!")
                        print(f"[AGENT] - Estimated distance: {detection.get('distance', 'unknown')} cm")
                        
                        if self.voice:
                            self.voice.respond("I found it! Approaching now", async_speech=True)
                        
                        object_found = True
                        self.state = AgentState.APPROACHING
                        break
                
                # Small delay between waypoints
                time.sleep(0.5)
            
            if not object_found:
                print("[AGENT] - Search complete. Object not found in search area.")
                if self.voice:
                    self.voice.respond("I couldn't find the object in the search area")
                self.vision.release_camera()
                self.state = AgentState.IDLE
            self.vision.release_camera()
            self.state = AgentState.IDLE
            
    def _approaching_state(self):
        """Approaching state - use visual servoing to reach the object."""
        print("\n[AGENT] - APPROACHING object using visual servoing...")
        
        # Use visual servoing to approach
        success = self.visual_servo.servo_to_target(self.vision, display=True)
        
        if success:
            print("[AGENT] - ✓ Successfully reached target position!")
            if self.voice:
                self.voice.respond("I'm in position to grab it", async_speech=True)
            self.state = AgentState.GRASPING
        else:
            print("[AGENT] - Failed to approach target. Returning to search.")
            self.state = AgentState.SEARCHING
        
    def _grasping_state(self):
        """Grasping state - pick up the object with the robotic arm."""
        print("\n[AGENT] - Executing GRASP sequence...")
        
        if self.voice:
            self.voice.respond("Grabbing the object now", async_speech=True)
        
        # Execute grab sequence
        self.arm.grab_object()
        
        # Verify grip
        time.sleep(0.5)
        if self.gripper.check_grip():
            print("[AGENT] - ✓ Grasp successful! Object secured.")
            if self.voice:
                self.voice.respond("Got it! Returning now", async_speech=True)
            self.state = AgentState.RETURNING
        else:
            print("[AGENT] - Grasp failed. Retrying...")
            time.sleep(0.5)
            self.arm.grab_object()
            if self.gripper.check_grip():
                print("[AGENT] - ✓ Grasp successful on retry!")
                self.state = AgentState.RETURNING
            else:
                print("[AGENT] - Failed to grasp object. Aborting mission.")
                if self.voice:
                    self.voice.respond("I couldn't grab it. Sorry.")
                self.state = AgentState.IDLE
    
    def _returning_state(self):
        """Returning state - navigate back to user."""
        print("\n[AGENT] - RETURNING to home position...")
        
        # Release camera (no longer needed)
        self.vision.release_camera()
        
        # Get return path
        return_path = self.nav_planner.get_return_path()
        
        if return_path:
            print(f"[AGENT] - Following breadcrumb trail ({len(return_path)} waypoints)...")
            for i, point in enumerate(return_path):
                print(f"[AGENT] - Returning to waypoint {i+1}/{len(return_path)}: {point}")
                self.motors.navigate_to_point(point[0], point[1])
                time.sleep(0.3)
        else:
            print("[AGENT] - No breadcrumb trail. Moving to origin...")
            self.motors.navigate_to_point(0, 0)
        
        print("[AGENT] - ✓ Arrived at home position")
        
        # Present object to user
        print("[AGENT] - Presenting object to user...")
        self.arm.present_object()
        time.sleep(1)
        
        if self.voice:
            self.voice.respond("Here is your " + self.current_plan.get('object_description'))
        
        self.state = AgentState.TASK_COMPLETE

    def _task_complete_state(self):
        """Task complete state - finish up and return to idle."""
        print("\n[AGENT] - ✓✓✓ Task complete! ✓✓✓")
        
        # Release object
        print("[AGENT] - Releasing object...")
        self.gripper.open_gripper()
        time.sleep(1)
        
        # Return arm to home
        self.arm.return_to_home()
        
        # Clear breadcrumb trail for next mission
        self.nav_planner.breadcrumb_trail.clear()
        
        print("\n[AGENT] - Ready for next command.")
        self.current_plan = {}
        self.state = AgentState.IDLE
        
    def _shutdown(self):
        """Cleanup and shutdown procedure."""
        print("\n[AGENT] - Initiating shutdown sequence...")
        
        # Stop all motors
        self.motors.stop()
        
        # Return arm to safe position
        self.arm.return_to_home()
        
        # Release camera
        self.vision.release_camera()
        
        if self.voice:
            self.voice.respond("Shutting down. Goodbye!")
        
        print("[AGENT] - ✓ ATLAS shutdown complete.")
        print("="*60 + "\n")

# --- To run the main agent simulation ---
if __name__ == "__main__":
    atlas_agent = Agent()
    atlas_agent.run()