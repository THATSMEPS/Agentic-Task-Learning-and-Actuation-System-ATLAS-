# navigation.py

class NavigationPlanner:
    """Generates high-level navigation plans and paths."""

    def __init__(self):
        self.breadcrumb_trail = []

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

    def get_return_path(self) -> list:
        """Returns the recorded path in reverse for homing."""
        if not self.breadcrumb_trail:
            return []
        
        return self.breadcrumb_trail[::-1]

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