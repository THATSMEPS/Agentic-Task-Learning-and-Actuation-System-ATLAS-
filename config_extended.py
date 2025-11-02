# config_extended.py
"""
Extended Configuration file for ATLAS Robot
Contains all adjustable parameters for the robot's subsystems
"""

import os

# --- API Keys ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# --- Camera Configuration ---
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_INDEX = 0

# --- Distance Estimation ---
CAMERA_FOCAL_LENGTH = 600  # pixels

KNOWN_OBJECT_SIZES = {
    'phone': 15,
    'book': 20,
    'pen': 1.5,
    'ball': 10,
    'cup': 8,
    'bottle': 7,
    'tool': 15,
    'box': 20,
}

# --- Navigation Configuration ---
SEARCH_AREA_WIDTH = 5.0
SEARCH_AREA_HEIGHT = 3.0
SEARCH_STEP_SIZE = 0.5

# --- Motor Control Configuration ---
BASE_SPEED = 0.5
TURN_RATE = 45
MIN_SAFE_DISTANCE = 0.3

# --- Visual Servoing Configuration ---
CENTER_TOLERANCE_PX = 50
TARGET_DISTANCE_CM = 30
VISUAL_SERVO_TURN_GAIN = 0.1

# --- Speech Configuration ---
WAKE_WORD = "atlas"
SPEECH_TIMEOUT = 10
TTS_RATE = 150
TTS_VOLUME = 0.9

# --- Display Configuration ---
SHOW_VISUAL_FEEDBACK = True
DEBUG_MODE = True
