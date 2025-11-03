# ATLAS - Agentic Task Learning and Actuation System

**A voice-commanded mobile robot assistant that can locate, fetch, and deliver objects**

---

## 🤖 Project Overview

ATLAS is a knee-high, voice-commanded mobile robot designed to act as a "fetch-bot" in workshop or desk environments. Using computer vision and LLM-powered task planning, ATLAS can:

- Understand natural language commands
- Search for and locate requested objects
- Navigate autonomously with obstacle avoidance
- Pick up objects with a robotic arm
- Deliver items to the user

## 📋 Current Status

**Phase: Software Development & Testing (Hardware Simulation Mode)**

All code is complete with hardware commands written as comments and print statements showing what the hardware would do. Currently using laptop camera for vision testing.

## 🏗️ System Architecture

### Core Modules

1. **agent.py** - Main orchestration and state machine
2. **vision_yolo.py** - YOLOv8-based object detection with color filtering
3. **navigation.py** - Path planning and visual servoing
4. **motor_control.py** - 4-wheel drive control and obstacle avoidance
5. **arm_control.py** - 4-DOF robotic arm control
6. **llm_interface.py** - Natural language understanding (Gemini API)
7. **speech_interface.py** - Voice recognition and text-to-speech
8. **config.py** - System configuration parameters

### State Machine Flow

```
IDLE → PLANNING → SEARCHING → APPROACHING → GRASPING → RETURNING → TASK_COMPLETE → IDLE
```

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

### Setup

1. **Get a Gemini API Key** (optional for testing)
   - Visit https://makersuite.google.com/app/apikey
   - Set environment variable:
   ```bash
   # Windows PowerShell
   $env:GEMINI_API_KEY="your-api-key-here"
   
   # Linux/Mac
   export GEMINI_API_KEY="your-api-key-here"
   ```

2. **Test Individual Modules**
   ```bash
   # Test YOLOv8 vision system (uses laptop camera)
   python vision_yolo.py
   
   # Test motor control simulation
   python motor_control.py
   
   # Test robotic arm simulation
   python arm_control.py
   
   # Test navigation and visual servoing
   python navigation.py
   
   # Test LLM interface
   python llm_interface.py
   
   # Test speech interface
   python speech_interface.py
   ```

3. **Run the Complete System**
   ```bash
   # Text input mode (recommended for testing)
   python main.py
   
   # Voice control mode (requires microphone)
   python main.py --voice
   ```

## 💻 Testing Without Hardware

### Vision System Testing (YOLOv8)

The vision system uses YOLOv8 for robust object detection with your laptop camera:

1. Run `python vision_yolo.py`
2. Enter target object (e.g., "phone", "cup", "laptop")
3. Optionally enter color (e.g., "blue", "red") for color filtering
4. Point camera at objects
5. System will detect, track, and show live distance

**What You'll See:**
- Green bounding box around detected object
- Live distance in cm above the box
- Blue center crosshair
- Direction guidance ("TURN LEFT", "TURN RIGHT", "MOVE FORWARD")
- Yellow line from center to object

**Features:**
- Detects 80+ object classes (COCO dataset)
- Optional color filtering for specific colored objects
- Live distance calculation using calibrated focal length
- No infinite logging spam
- Smooth 30fps video feed

**Commands:**
- Press 'q' to quit

### Example Commands

When running `main.py`, try these commands:

```
"ATLAS, bring me the red pen"
"Find my blue phone"
"Get the green book"
"Fetch the yellow cup"
```

## 🔧 Features Implemented

### ✅ Month 1 Goals (Hardware Simulation)
- [x] Motor control simulation with 4-wheel drive
- [x] Robotic arm control with 4-DOF + gripper
- [x] Basic movement commands (forward, backward, turn)
- [x] Arm pose sequences and grasping

### ✅ Month 2 Goals (Autonomy)
- [x] Obstacle avoidance with ultrasonic sensors (simulated)
- [x] Camera integration (laptop camera for testing)
- [x] YOLOv8 object detection (80+ classes, robust recognition)
- [x] Optional color filtering for specific colored objects
- [x] Visual servoing for approach control
- [x] Live distance estimation with calibrated focal length
- [x] Lawnmower search pattern

### ✅ Month 3 Goals (AI Integration)
- [x] LLM integration for command understanding (Gemini API)
- [x] Speech recognition interface (structure ready)
- [x] Text-to-speech responses (structure ready)
- [x] Complete fetch-and-deliver task pipeline
- [x] State machine orchestration

## 📐 Technical Details

### Visual Servoing Approach

ATLAS uses a simple but effective visual servoing algorithm:

1. **Detect Object**: Use color-based detection to find target
2. **Calculate Error**: Measure pixel offset from image center
3. **Turn to Center**: Rotate robot until object is centered
4. **Move Forward**: Advance when object is centered
5. **Repeat**: Continue until at target distance

**Key Parameters:**
- Center tolerance: ±50 pixels
- Target distance: 30 cm
- Turn gain: 0.1 degrees per pixel error

### Distance Estimation

Distance is estimated using the pinhole camera model:

```
Distance = (Real Object Width × Focal Length) / Pixel Width
```

**YOLOv8 Integration:**
- Detects 80+ object classes automatically
- Uses bounding box width for distance calculation
- Focal length calibrated for your camera (700 pixels)

**Calibrated Object Sizes:**
- Phone: 15 cm
- Book: 20 cm
- Cup: 8 cm
- Laptop: 35 cm
- Mouse: 10 cm
- Keyboard: 40 cm
- Bottle: 7 cm
- And more...

**Color Filtering (Optional):**
- If you specify a color (e.g., "blue phone"), the system filters detections by color
- Uses HSV color space for robust color matching
- Works in various lighting conditions

### Search Pattern

Lawnmower pattern systematically covers the search area:
- Width: 5 meters
- Height: 3 meters
- Step size: 0.5 meters

Robot doesn't need to see object from starting point - it moves until the object is within detection range (2-3 meters).

## 🛠️ Hardware Integration (Future)

### Required Hardware

**Mobility:**
- 4-wheel drive chassis with DC motors
- L298N motor driver (x2)
- 3x HC-SR04 ultrasonic sensors
- Power supply for motors

**Manipulation:**
- 4-DOF robotic arm
- 5x servo motors (MG996R or similar)
- PCA9685 16-channel PWM servo controller
- Gripper mechanism

**Vision:**
- Raspberry Pi Camera Module v2 (or USB webcam)
- Wide-angle lens recommended

**Compute:**
- Raspberry Pi 4 (4GB+ RAM recommended)
- MicroSD card (32GB+)

**Audio:**
- USB microphone
- Speaker or headphones

### Connecting Hardware

When hardware is available, uncomment the hardware-specific code marked with `TODO: Uncomment when hardware is connected` in:

- `motor_control.py` - GPIO setup for motors
- `arm_control.py` - PCA9685 initialization
- `speech_interface.py` - Speech recognition libraries

Then install hardware-specific dependencies:

```bash
pip install RPi.GPIO Adafruit-PCA9685
pip install SpeechRecognition pyttsx3 pyaudio
```

## 📊 Project Structure

```
The Atlas Robot/
├── main.py                 # Main entry point
├── agent.py                # Main orchestration & state machine
├── vision_yolo.py          # YOLOv8 object detection & color filtering
├── navigation.py           # Path planning & visual servoing
├── motor_control.py        # Mobility control
├── arm_control.py          # Manipulation control
├── llm_interface.py        # Natural language processing
├── speech_interface.py     # Voice I/O
├── config.py               # Configuration parameters
├── requirements.txt        # Python dependencies
├── yolov8n.pt              # YOLOv8 nano model (auto-downloads)
└── test_videos/            # Test videos for vision (optional)
```

## 🎯 Next Steps

### Immediate (Testing Phase)
1. Test all modules individually
2. Test complete fetch sequence with laptop camera
3. Refine color detection for various lighting conditions
4. Calibrate distance estimation for your camera

### When Hardware Arrives
1. Connect and test motors individually
2. Integrate motor control with navigation
3. Mount and test camera
4. Calibrate servo positions for arm
5. Test grab sequences
6. Full system integration

### Future Enhancements
- IMU sensor for precise odometry
- SLAM for mapping and localization
- Multiple object tracking
- Object recognition with deep learning
- Improved path planning (A*, RRT)
- Battery monitoring
- Web interface for monitoring

## 🐛 Troubleshooting

### Camera Not Working
- Check camera index in `config.py` (try 0, 1, 2)
- Ensure no other app is using the camera
- On Windows, check camera permissions

### Object Not Detected
- Adjust lighting conditions
- YOLOv8 works best with clear, unobstructed objects
- If using color filter, ensure object has significant visible color
- Try without color filter first (leave color blank)
- Lower HSV threshold is set to 15% for better matching
- Check that object class is in COCO dataset (80 common objects)

### API Errors
- Verify GEMINI_API_KEY is set correctly
- Check internet connection
- Can use fallback extraction (no API needed)

## 📝 Notes

- All hardware commands are currently simulated with print statements
- Visual servoing uses laptop camera for testing
- Distance estimation requires camera calibration
- LLM requires API key but has fallback parser

## 👥 Development Team

This is designed as a 2-person, 3-month project:
- **Person 1**: Mobility, navigation, obstacle avoidance
- **Person 2**: Manipulation, vision, grasping

## 📄 License

Educational project - feel free to use and modify for learning purposes.

## 🙏 Acknowledgments

- Built for robotics education and demonstration
- Uses Google Gemini for natural language understanding
- YOLOv8 by Ultralytics for robust object detection
- OpenCV for computer vision
- Designed for Raspberry Pi deployment

---

**Remember**: This is currently in simulation mode. All hardware interactions are printed to console for verification before actual hardware connection.

For questions or issues, review the individual module test scripts to verify each subsystem works correctly.
