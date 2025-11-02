# main.py
"""
Main entry point for ATLAS Robot Assistant
Run this file to start the robot agent
"""

import sys
from agent import Agent

if __name__ == "__main__":
    print("\n" + "="*60)
    print("   ATLAS Robot Assistant - Initialization")
    print("="*60 + "\n")
    
    # Check for command line arguments
    use_voice = '--voice' in sys.argv
    
    print("Configuration:")
    print(f"  - Voice Control: {'ENABLED' if use_voice else 'DISABLED (text input)'}")
    print(f"  - Camera: LAPTOP WEBCAM")
    print(f"  - Hardware: SIMULATION MODE")
    print()
    
    if not use_voice:
        print("Tip: Use '--voice' argument to enable voice control")
        print("Example: python main.py --voice")
        print()
    
    # Create and run agent
    try:
        atlas_agent = Agent(use_voice=use_voice, use_laptop_camera=True)
        atlas_agent.run()
    except KeyboardInterrupt:
        print("\n\nShutdown complete. Goodbye!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
