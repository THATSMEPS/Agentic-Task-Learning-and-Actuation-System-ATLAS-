# ATLAS Project Structure

```
The Atlas(Agentic Task Learning and Actuation System) Robot/
│
├── 📄 README.md                      # Main project documentation
├── 📄 QUICK_START.md                 # Quick start testing guide
├── 📄 IMPLEMENTATION_SUMMARY.md      # Detailed implementation summary
│
├── 🚀 main.py                        # Main entry point - START HERE
│
├── 🤖 Core Robot Modules
│   ├── agent.py                      # Main orchestration & state machine
│   ├── vision.py                     # Computer vision & object detection
│   ├── navigation.py                 # Path planning & visual servoing
│   ├── motor_control.py              # 4-wheel drive control
│   ├── arm_control.py                # Robotic arm control
│   ├── llm_interface.py              # Natural language processing (Gemini)
│   └── speech_interface.py           # Voice input/output
│
├── ⚙️ Configuration
│   ├── config.py                     # Main configuration (original)
│   ├── config_extended.py            # Extended configuration options
│   └── requirements.txt              # Python dependencies
│
├── 📁 test_videos/                   # Optional test videos for vision
│
└── 🔧 Development Files
    ├── .env                          # Environment variables (API keys)
    ├── .gitignore                    # Git ignore rules
    ├── .venv/                        # Python virtual environment
    └── .git/                         # Git repository
```

---

## 📄 File Descriptions

### Main Entry Points

| File | Purpose | Run Command |
|------|---------|-------------|
| `main.py` | Start the complete ATLAS system | `python main.py` |
| `agent.py` | Can also run directly | `python agent.py` |

### Core Modules (Can Test Individually)

| Module | Purpose | Test Command | What It Does |
|--------|---------|--------------|--------------|
| `vision.py` | Computer vision | `python vision.py` | Detect objects with laptop camera |
| `motor_control.py` | Mobility | `python motor_control.py` | Simulate robot movement |
| `arm_control.py` | Manipulation | `python arm_control.py` | Simulate arm movements |
| `navigation.py` | Path planning | `python navigation.py` | Test navigation algorithms |
| `llm_interface.py` | NLP | `python llm_interface.py` | Test command understanding |
| `speech_interface.py` | Voice I/O | `python speech_interface.py` | Test voice interface |

### Documentation

| File | Contents |
|------|----------|
| `README.md` | Project overview, features, setup instructions |
| `QUICK_START.md` | Step-by-step testing guide |
| `IMPLEMENTATION_SUMMARY.md` | Detailed technical documentation |

### Configuration

| File | Purpose |
|------|---------|
| `config.py` | Basic configuration (camera, colors) |
| `config_extended.py` | Extended parameters (speeds, thresholds) |
| `requirements.txt` | Python package dependencies |
| `.env` | API keys (create this file) |

---

## 🎯 Quick Navigation

### Want to...

**Test the complete system?**
→ `python main.py`

**Test vision with your camera?**
→ `python vision.py`

**Understand how it works?**
→ Read `IMPLEMENTATION_SUMMARY.md`

**Get started quickly?**
→ Read `QUICK_START.md`

**Learn about the project?**
→ Read `README.md`

**Test individual components?**
→ Run any module file directly

---

## 📊 Module Dependencies

```
main.py
  └─→ agent.py
       ├─→ vision.py
       │    └─→ config.py
       │    └─→ opencv, numpy
       │
       ├─→ navigation.py
       │    └─→ vision.py (for visual servoing)
       │
       ├─→ motor_control.py
       │
       ├─→ arm_control.py
       │
       ├─→ llm_interface.py
       │    └─→ config.py (for API key)
       │    └─→ google.generativeai
       │
       └─→ speech_interface.py
```

---

## 🔄 Data Flow

```
User Command (Voice/Text)
    ↓
[LLM Interface] → Parse command
    ↓
[Agent: PLANNING] → Create task plan
    ↓
[Vision] → Set target object
    ↓
[Agent: SEARCHING] → Lawnmower pattern
    ↓
[Motor Control] → Navigate waypoints
    ↓
[Vision] → Detect object
    ↓
[Agent: APPROACHING] → Visual servoing
    ↓
[Navigation: Visual Servo] → Center & approach
    ↓
[Motor Control] → Execute movements
    ↓
[Agent: GRASPING] → Grab object
    ↓
[Arm Control] → Execute grab sequence
    ↓
[Agent: RETURNING] → Navigate home
    ↓
[Motor Control] → Follow breadcrumbs
    ↓
[Arm Control] → Present object
    ↓
[Agent: TASK_COMPLETE] → Release & reset
```

---

## 🧪 Testing Order (Recommended)

1. **Vision System** (`python vision.py`)
   - Most important!
   - Validates camera and object detection
   - Tests with real hardware (your webcam)

2. **LLM Interface** (`python llm_interface.py`)
   - Tests command understanding
   - Can work without API key

3. **Motor Control** (`python motor_control.py`)
   - Simulates movement
   - Tests navigation logic

4. **Arm Control** (`python arm_control.py`)
   - Simulates manipulation
   - Tests grab sequences

5. **Navigation** (`python navigation.py`)
   - Tests path planning
   - Visual servoing calculations

6. **Complete System** (`python main.py`)
   - Full integration test
   - Complete fetch-and-deliver pipeline

---

## 💾 File Sizes (Approximate)

| File | Lines | Size |
|------|-------|------|
| `agent.py` | ~330 | 12 KB |
| `vision.py` | ~300 | 11 KB |
| `motor_control.py` | ~300 | 11 KB |
| `arm_control.py` | ~280 | 10 KB |
| `navigation.py` | ~240 | 9 KB |
| `llm_interface.py` | ~150 | 6 KB |
| `speech_interface.py` | ~250 | 9 KB |
| `main.py` | ~40 | 1.5 KB |
| **TOTAL CODE** | ~1,890 | ~70 KB |

---

## 🎨 Code Style

All modules follow consistent patterns:

```python
# module_name.py
"""
Module docstring explaining purpose
"""

# Imports
import standard_lib
import third_party
import local_modules

# Classes
class MainClass:
    """Class docstring"""
    
    def __init__(self):
        """Initialize with hardware simulation"""
        self.hardware_connected = False
        print("[MODULE] - Initialized")
    
    def initialize_hardware(self):
        """Setup real hardware"""
        # TODO: Uncomment when hardware is connected
        pass
    
    def main_functionality(self):
        """Core functionality"""
        print("[MOCK HARDWARE] - What hardware would do")
        # Real logic here
        
# Test harness
if __name__ == "__main__":
    print("=== Testing Module ===")
    # Test code
```

---

## 🏷️ Naming Conventions

### Module Names
- Lowercase with underscores: `motor_control.py`

### Class Names
- PascalCase: `MotorController`, `VisionSystem`

### Function/Method Names
- Lowercase with underscores: `find_target_object()`, `navigate_to_point()`

### Constants
- Uppercase with underscores: `FRAME_WIDTH`, `BASE_SPEED`

### State Enum
- PascalCase: `AgentState.SEARCHING`

---

## 🔐 Configuration Files

### `.env` (Create this)
```bash
GEMINI_API_KEY=your_api_key_here
```

### `config.py` (Existing)
- Camera settings
- Color ranges (legacy)
- Frame dimensions

### `config_extended.py` (New)
- All additional parameters
- Motor speeds
- Servo limits
- Thresholds

---

## 📦 Dependencies

### Required (Installed)
- `opencv-python` - Computer vision
- `numpy` - Numerical operations
- `google-generativeai` - LLM integration

### Optional (Commented in requirements.txt)
- `SpeechRecognition` - Voice input
- `pyttsx3` - Text-to-speech
- `pyaudio` - Audio I/O
- `RPi.GPIO` - Raspberry Pi GPIO (hardware)
- `Adafruit-PCA9685` - Servo controller (hardware)

---

## 🎯 Entry Points Summary

```bash
# Main application
python main.py                  # Text input mode
python main.py --voice          # Voice input mode (simulated)

# Individual module tests
python vision.py                # Test vision with webcam
python motor_control.py         # Test motor simulation
python arm_control.py           # Test arm simulation
python navigation.py            # Test navigation algorithms
python llm_interface.py         # Test command parsing
python speech_interface.py      # Test voice interface

# Python interactive
python
>>> from agent import Agent
>>> robot = Agent(use_laptop_camera=True)
>>> # Manual control
```

---

## 📝 Log Output Format

All modules use consistent logging:

```
[MODULE_NAME] - Message type: Details
```

Examples:
```
[AGENT] - ATLAS is online and awaiting commands.
[VISION] - Target set: 'blue phone' with primary color 'blue'
[MOTOR] - Navigating from [0, 0] to (2.5, 1.5)
[ARM] - Moving to 'grab' pose
[NAV] - Generated 14 waypoints for lawnmower search
[LLM] - Plan received: {'action': 'fetch', ...}
[VISUAL_SERVO] - Error: +120px | Distance: 85.3cm
[MOCK HARDWARE] - TURNING RIGHT 12.0°
```

This makes it easy to track which subsystem is active!

---

## 🚀 Version History

### v1.0 - Complete Implementation
- ✅ All 8 modules implemented
- ✅ Hardware simulation mode working
- ✅ Laptop camera integration
- ✅ Dynamic object detection
- ✅ Visual servoing
- ✅ Distance estimation
- ✅ Complete fetch-and-deliver pipeline
- ✅ LLM integration with fallback
- ✅ Voice interface structure
- ✅ Comprehensive documentation

---

## 📞 Support

**Having issues?**

1. Check `QUICK_START.md` for testing steps
2. Run individual modules to isolate problem
3. Check log output for error messages
4. Verify camera is working (`python vision.py`)
5. Check that all dependencies are installed

**Common Issues:**

| Problem | Solution | File |
|---------|----------|------|
| Camera not found | Change `CAMERA_INDEX` in config | `config.py` |
| Object not detected | Adjust lighting, try red object first | `vision.py` |
| API key error | Set environment variable or use fallback | `llm_interface.py` |
| Import error | Install requirements: `pip install -r requirements.txt` | N/A |

---

**Last Updated:** November 2, 2025
**Status:** ✅ Complete and Ready for Testing
**Hardware:** Currently in simulation mode
