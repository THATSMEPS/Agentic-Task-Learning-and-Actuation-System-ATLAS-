# config.py

# --- API Keys ---
# IMPORTANT: Set the GEMINI_API_KEY environment variable to your actual Google AI Studio API key.
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- Vision System Configuration ---
# These are example HSV color ranges for detecting the color RED.
# You will need to fine-tune these values for your specific object and lighting.
# To do this, you can run the vision.py script and adjust the values in the trackbar window.
RED_LOWER = [0, 120, 70]
RED_UPPER = [10, 255, 255]

# A second range is needed for red as it wraps around the HSV color circle.
RED_LOWER_2 = [170, 120, 70]
RED_UPPER_2 = [180, 255, 255]

# --- Robot Physical Parameters (for simulation) ---
FRAME_WIDTH = 640
FRAME_HEIGHT = 480