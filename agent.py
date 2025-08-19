# agent.py
import time
from enum import Enum
import config
from vision import VisionSystem
from navigation import NavigationPlanner
from llm_interface import get_plan_from_command

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

    def __init__(self):
        self.state = AgentState.IDLE
        self.vision = VisionSystem()
        self.nav_planner = NavigationPlanner()
        self.current_plan = {}

    def run(self):
        """The main loop of the agent's state machine."""
        print("[AGENT] - ATLAS is online. Awaiting commands.")
        while True:
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
            
            time.sleep(1)

    def _idle_state(self):
        # In a real system, this would be triggered by a wake word.
        # For now, we simulate it with a text input.
        command = input("\n[AGENT] - I am IDLE. Enter a command to start: ")
        self.current_command = command
        self.state = AgentState.PLANNING

    def _planning_state(self):
        print(f"[AGENT] - Planning task for command: '{self.current_command}'")
        self.current_plan = get_plan_from_command(self.current_command)
        if self.current_plan:
            self.state = AgentState.SEARCHING
        else:
            print("[AGENT] - Planning failed. Returning to IDLE.")
            self.state = AgentState.IDLE
            
    def _searching_state(self):
        print(f"[AGENT] - SEARCHING for '{self.current_plan.get('object_description')}'...")
        waypoints = self.nav_planner.generate_lawnmower_path(5, 3, 0.5)
        
        for i, point in enumerate(waypoints):
            print(f"[MOCK HARDWARE] - Commanding motors to navigate to waypoint {i+1}: {point}")
            # Simulate finding the object after a few waypoints
            if i > 2:
                print(f"[AGENT] - VISION SYSTEM DETECTED OBJECT!")
                self.state = AgentState.APPROACHING
                return
            time.sleep(0.5) # Simulate travel time
        
        print("[AGENT] - Search complete, object not found.")
        self.state = AgentState.IDLE
            
    def _approaching_state(self):
        print("[AGENT] - APPROACHING object using visual servoing.")
        # Simulate visual servoing loop
        for i in range(3):
            # In reality, you'd get these from vision.py
            error_x = 50 - (i * 20) 
            print(f"[MOCK HARDWARE] - Object is off-center by {error_x} pixels. Commanding turn.")
            time.sleep(0.5)
        
        print("[MOCK HARDWARE] - Object is centered. Commanding move forward.")
        print("[AGENT] - Object is close enough for grasping.")
        self.state = AgentState.GRASPING
        
    def _grasping_state(self):
        print("[AGENT] - Executing GRASP sequence.")
        print("[MOCK HARDWARE] - Commanding robotic arm to pick up object.")
        time.sleep(1)
        print("[AGENT] - Grasp successful.")
        self.state = AgentState.RETURNING

    def _returning_state(self):
        print("[AGENT] - RETURNING to home position.")
        print("[MOCK HARDWARE] - Following breadcrumb trail back to start.")
        time.sleep(2) # Simulate return travel time
        self.state = AgentState.TASK_COMPLETE

    def _task_complete_state(self):
        print("\n[AGENT] - Task complete! Returning to IDLE state.")
        self.current_plan = {}
        self.state = AgentState.IDLE

# --- To run the main agent simulation ---
if __name__ == "__main__":
    atlas_agent = Agent()
    atlas_agent.run()