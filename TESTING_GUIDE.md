# 🎮 ATLAS Complete Testing Guide - Step by Step

## 📋 **What You Need Before Starting**

- ✅ Python installed
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ A webcam/laptop camera
- ✅ Colored objects (red, blue, or green work best)
- ✅ Good lighting in your room

---

## 🎯 **STEP-BY-STEP TESTING SEQUENCE**

---

### **TEST 1: Vision System (MOST IMPORTANT - START HERE!)**

This validates your camera works and can detect objects.

#### **Run Command:**
```powershell
python vision.py
```

#### **What You'll See in Terminal:**
```
=== Testing Vision System ===
This test will use your laptop camera.
Commands:
  'q' - Quit
  's' - Set new target object

Enter target object (e.g., 'blue phone', 'red cup', 'green book'):
```

#### **What To Do:**

1. **Type a target object with color**, for example:
   - `blue phone`
   - `red cup`
   - `green book`
   - `yellow bottle`

2. **Press Enter**

3. **A VIDEO WINDOW WILL OPEN** showing your camera feed

#### **What You'll See in the Video Window:**

**When NO object detected:**
- Your live camera feed
- Blue crosshair in center labeled "CENTER"
- Red text at top: "SEARCHING FOR: blue phone"

**When object IS detected:**
- Live camera feed
- **GREEN BOUNDING BOX** around the detected object
- **LARGE GREEN TEXT above box**: Distance in cm (e.g., "87.5 cm")
- Red dot at object center
- Yellow line from center to object
- Text below box: "Target: blue phone"
- Orange/Green guidance text at top:
  - "<<< TURN LEFT" (if object is left)
  - "TURN RIGHT >>>" (if object is right)
  - "CENTERED - GO FORWARD" (if centered)

#### **What You'll See in Terminal (Once per second):**
```
[VISION] Object: CENTERED  | Distance:  87.5 cm
[VISION] Object: RIGHT     | Distance:  92.3 cm
[VISION] Object: LEFT      | Distance:  45.1 cm
```

#### **Controls:**
- Press **'s'** to change target object
- Press **'q'** to quit

#### **Tips for Success:**
- Use **solid colored objects** (blue phone, red cup, green book)
- Ensure **good lighting** (daylight or bright room light)
- Hold object **50cm - 2 meters** from camera
- **Plain background** helps (white wall, desk surface)

#### **Example Session:**
```
Enter target object: blue phone
[VISION] - Target set: 'blue phone' with primary color 'blue'
[VISION] - Camera 0 initialized successfully

Starting camera feed. Point camera at target object...
============================================================
CONTROLS:
  'q' - Quit
  's' - Change target object
============================================================

** WATCH THE VIDEO WINDOW - Distance shows on green box **

[VISION] Searching for target object...
[VISION] Object: RIGHT     | Distance:  95.2 cm
[VISION] Object: CENTERED  | Distance:  87.5 cm
[VISION] Object: CENTERED  | Distance:  85.3 cm

[Press 'q' to quit]
[VISION] - Camera released

=== Vision System Test Complete ===
```

---

### **TEST 2: Motor Control Simulation**

This shows what the motors would do (simulation only).

#### **Run Command:**
```powershell
python motor_control.py
```

#### **What You'll See:**
```
=== Testing Motor Control System ===

--- Test 1: Basic Movement ---
[MOCK HARDWARE] - MOVING FORWARD for 2.00s
[MOCK HARDWARE] - MOTORS STOPPED
[MOCK HARDWARE] - TURNING RIGHT 90° (duration: 2.00s)
[MOCK HARDWARE] - MOTORS STOPPED
[MOCK HARDWARE] - MOVING FORWARD for 1.00s
[MOCK HARDWARE] - MOTORS STOPPED
[MOCK HARDWARE] - TURNING LEFT 45° (duration: 1.00s)
[MOCK HARDWARE] - MOTORS STOPPED

--- Current Position: [2.0, 1.414], Heading: 45° ---

--- Test 2: Obstacle Detection ---
[MOCK HARDWARE] - FRONT ultrasonic sensor reads: 1.23m
[OBSTACLE] - WARNING: Obstacle detected 0.25m away on front sensor!
[OBSTACLE] - Executing obstacle avoidance maneuver...
[MOCK HARDWARE] - MOTORS STOPPED
[MOCK HARDWARE] - MOVING BACKWARD for 0.50s
...

=== Motor Control Test Complete ===
```

#### **What This Tests:**
- ✅ Forward/backward movement
- ✅ Left/right turning
- ✅ Navigation to waypoints
- ✅ Obstacle detection and avoidance
- ✅ Position tracking

**Duration:** ~10 seconds

---

### **TEST 3: Robotic Arm Simulation**

This shows what the robotic arm would do (simulation only).

#### **Run Command:**
```powershell
python arm_control.py
```

#### **What You'll See:**
```
=== Testing Robotic Arm Control System ===

--- Test 1: Basic Servo Control ---
[MOCK HARDWARE] - Moving BASE servo to 45°
[MOCK HARDWARE] - Moving SHOULDER servo to 60°
[MOCK HARDWARE] - Moving ELBOW servo to 90°

--- Test 2: Pre-defined Poses ---
[ARM] - Moving to 'home' pose
[MOCK HARDWARE] - Moving BASE servo to 90°
[MOCK HARDWARE] - Moving SHOULDER servo to 90°
...

--- Test 3: Grab Sequence ---
[ARM] - Executing GRAB sequence...
[ARM] - Step 1: Positioning for grab
[ARM] - Moving to 'ready_to_grab' pose
[ARM] - Step 2: Closing gripper
[MOCK HARDWARE] - Moving GRIPPER servo to 180°
[ARM] - Step 3: Lifting object
[ARM] - ✓ GRAB sequence complete!

--- Test 4: Present and Release ---
[ARM] - Presenting object to user...
[ARM] - Moving to 'present' pose
[GRIPPER] - Opening gripper

=== Robotic Arm Test Complete ===
```

#### **What This Tests:**
- ✅ Individual servo movements
- ✅ Pre-defined poses
- ✅ Complete grab sequence
- ✅ Object presentation
- ✅ Gripper control

**Duration:** ~8 seconds

---

### **TEST 4: LLM Command Understanding**

This tests how the system understands natural language commands.

#### **Run Command:**
```powershell
python llm_interface.py
```

#### **What You'll See:**
```
=== Testing LLM Interface ===

--- Test 1 ---
Command: "Hey ATLAS, I need you to retrieve the red toolbox from across the room."
[LLM] - Extracted info: {'action': 'fetch', 'object_description': 'red toolbox', 'object_color': 'red', 'object_type': 'tool'}
✓ Success!
  Action: fetch
  Object: red toolbox
  Color: red
  Type: tool

--- Test 2 ---
Command: "ATLAS, can you find my phone?"
[LLM] - Extracted info: {'action': 'fetch', 'object_description': 'phone', 'object_color': 'unknown', 'object_type': 'phone'}
✓ Success!
  Action: fetch
  Object: phone
  Color: unknown
  Type: phone

[Tests 3-5 continue...]

=== LLM Interface Test Complete ===
```

#### **What This Tests:**
- ✅ Command parsing
- ✅ Object extraction
- ✅ Color identification
- ✅ Action determination
- ✅ Fallback parser (works without API key)

**Duration:** 5-10 seconds

---

### **TEST 5: Navigation System**

This tests path planning and visual servoing calculations.

#### **Run Command:**
```powershell
python navigation.py
```

#### **What You'll See:**
```
=== Testing Navigation System ===

--- Test 1: Lawnmower Path Generation ---
[NAV] - Generated 14 waypoints for lawnmower search.

Generated Path:
  Waypoint 1: (0.0, 0.0)
  Waypoint 2: (5.0, 0.0)
  Waypoint 3: (5.0, 0.5)
  Waypoint 4: (0.0, 0.5)
  ...

--- Test 2: Breadcrumb Trail ---
Recorded Path: [(0, 0), (1, 0), (1, 1), (2, 1)]
Return Path: [(2, 1), (1, 1), (1, 0), (0, 0)]

--- Test 3: Visual Servoing (Simulation) ---
  Error: +200px → Turn: +20.0° | Status: RIGHT
  Error: +150px → Turn: +15.0° | Status: RIGHT
  Error: +100px → Turn: +10.0° | Status: RIGHT
  Error:  +50px → Turn:  +5.0° | Status: CENTERED
  Error:  +20px → Turn:  +2.0° | Status: CENTERED
  Error:   +0px → Turn:  +0.0° | Status: CENTERED
  Error:  -30px → Turn:  -3.0° | Status: CENTERED
  Error: -100px → Turn: -10.0° | Status: LEFT
  Error: -150px → Turn: -15.0° | Status: LEFT

=== Navigation System Test Complete ===
```

#### **What This Tests:**
- ✅ Search pattern generation
- ✅ Breadcrumb trail recording
- ✅ Return path calculation
- ✅ Visual servoing turn calculations

**Duration:** ~5 seconds

---

### **TEST 6: Complete ATLAS System** 🚀

This runs the **COMPLETE ROBOT SIMULATION** with all systems integrated!

#### **Run Command:**
```powershell
python main.py
```

#### **What You'll See (Complete Example):**

```
============================================================
   ATLAS Robot Assistant - Initialization
============================================================

Configuration:
  - Voice Control: DISABLED (text input)
  - Camera: LAPTOP WEBCAM
  - Hardware: SIMULATION MODE

Tip: Use '--voice' argument to enable voice control
Example: python main.py --voice

[MOTOR] - Motor Controller initialized (Hardware simulation mode)
[OBSTACLE] - Obstacle Avoidance initialized (Hardware simulation mode)
[ARM] - Robotic Arm initialized (Hardware simulation mode)
[VISUAL_SERVO] - Visual Servoing controller initialized
[AGENT] - ✓ ATLAS subsystems initialized

============================================================
   ATLAS - Agentic Task Learning and Actuation System
              Robot Assistant v1.0
============================================================

[AGENT] - ATLAS is online and awaiting commands.

Enter a command (or 'quit' to exit):
```

#### **Now Type a Command, for example:**
```
bring me the blue phone
```

#### **What Happens Next:**

**1. PLANNING Phase:**
```
[AGENT] - Planning task for command: 'bring me the blue phone'
[LLM] - Extracted info: {'action': 'fetch', 'object_description': 'blue phone', 'object_color': 'blue', 'object_type': 'phone'}
[AGENT] - ✓ Plan created:
          Action: fetch
          Target: blue phone
          Color: blue
[VISION] - Target set: 'blue phone' with primary color 'blue'
[VISION] - Camera 0 initialized successfully
```

**2. SEARCHING Phase:**
```
[AGENT] - SEARCHING for 'blue phone'...
[NAV] - Generated 14 waypoints for lawnmower search.
[AGENT] - Moving to search waypoint 1/14: (0, 0)
[MOCK HARDWARE] - FRONT ultrasonic sensor reads: 1.45m
[MOTOR] - Navigating from [0, 0] to (0, 0)
```

**3. OBJECT DETECTED:**
```
[AGENT] - ✓ OBJECT DETECTED!
[AGENT] - Estimated distance: 87.5 cm
```

**4. APPROACHING Phase (Visual Servoing):**

A **VIDEO WINDOW OPENS** showing:
- Your camera feed
- Green bounding box around blue phone
- Large distance display
- Direction guidance

Terminal shows:
```
[AGENT] - APPROACHING object using visual servoing...
[VISUAL_SERVO] - Starting visual servoing approach...
[VISUAL_SERVO] - Error: +115px | Distance: 87.5cm
[VISUAL_SERVO] - Object RIGHT by 115px → Turn RIGHT 11.5°
[MOCK HARDWARE] - TURNING RIGHT 11.5° (duration: 0.26s)
[MOCK HARDWARE] - MOTORS STOPPED

[VISUAL_SERVO] - Error: +45px | Distance: 78.2cm
[VISUAL_SERVO] - Object CENTERED → Move FORWARD
[MOCK HARDWARE] - MOVING FORWARD for 0.50s
[MOCK HARDWARE] - MOTORS STOPPED

[VISUAL_SERVO] - Error: +3px | Distance: 28.7cm
[VISUAL_SERVO] - ✓ Reached target distance!
[AGENT] - ✓ Successfully reached target position!
```

**5. GRASPING Phase:**
```
[AGENT] - Executing GRASP sequence...
[ARM] - Moving to 'ready_to_grab' pose
[MOCK HARDWARE] - Moving BASE servo to 90°
[MOCK HARDWARE] - Moving SHOULDER servo to 45°
[MOCK HARDWARE] - Moving ELBOW servo to 45°
[MOCK HARDWARE] - Moving WRIST servo to 0°
[MOCK HARDWARE] - Moving GRIPPER servo to 0°
[ARM] - Reached 'ready_to_grab' pose

[ARM] - Step 2: Closing gripper
[MOCK HARDWARE] - Moving GRIPPER servo to 180°
[GRIPPER] - Closing gripper with medium force (150°)

[ARM] - Step 3: Lifting object
[ARM] - Moving to 'lift' pose
[ARM] - ✓ GRAB sequence complete!

[MOCK HARDWARE] - Checking grip status via current sensing
[AGENT] - ✓ Grasp successful! Object secured.
```

**6. RETURNING Phase:**
```
[AGENT] - RETURNING to home position...
[VISION] - Camera released
[AGENT] - Following breadcrumb trail (1 waypoints)...
[AGENT] - Returning to waypoint 1/1: (0, 0)
[MOTOR] - Navigating from [0, 0] to (0, 0)
[AGENT] - ✓ Arrived at home position

[AGENT] - Presenting object to user...
[ARM] - Presenting object to user...
[ARM] - Moving to 'present' pose
[MOCK HARDWARE] - Moving BASE servo to 90°
[MOCK HARDWARE] - Moving SHOULDER servo to 135°
[MOCK HARDWARE] - Moving ELBOW servo to 45°
[MOCK HARDWARE] - Moving WRIST servo to 90°
[ARM] - Reached 'present' pose
```

**7. TASK COMPLETE:**
```
[AGENT] - ✓✓✓ Task complete! ✓✓✓

[AGENT] - Releasing object...
[GRIPPER] - Opening gripper
[MOCK HARDWARE] - Moving GRIPPER servo to 0°

[ARM] - Returning to home position...
[ARM] - Moving to 'home' pose
[MOCK HARDWARE] - Moving all servos to home positions

[AGENT] - Ready for next command.

Enter a command (or 'quit' to exit):
```

#### **You Can Now:**
- Enter another command
- Type `quit` to exit

---

## 🎨 **VISUAL GUIDE - What You'll See in Video Window**

### When Testing vision.py or main.py:

```
┌─────────────────────────────────────────────────────────┐
│  ATLAS Vision System - Press 'q' to quit              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   <<< TURN LEFT           [If object is left]          │
│   TURN RIGHT >>>          [If object is right]         │
│   CENTERED - GO FORWARD   [If object is centered]      │
│                                                         │
│                   ╳ CENTER                              │
│                   ┃    [Blue crosshair]                │
│              ─────┼─────                                │
│                   ┃                                     │
│                   ┃                                     │
│                   ┃ [Yellow line to object]             │
│                   ┃                                     │
│              ┌────┼─────┐                               │
│              │    ●     │  [Green box around object]   │
│              │          │  [Red dot = center]          │
│              └──────────┘                               │
│                                                         │
│              87.5 cm     [Large green text]            │
│                                                         │
│              Target: blue phone                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 **TROUBLESHOOTING**

### Problem: Video window doesn't open
**Solution:** 
- Make sure no other app is using camera
- Try `python vision.py` first to test camera
- On Windows, check camera permissions in Settings

### Problem: No object detected
**Solutions:**
- Use **bright, solid-colored objects** (red, blue, green best)
- Improve **lighting** (add more light)
- Try **closer to camera** (50cm - 1m range)
- Use objects with **plain backgrounds**

### Problem: Distance is wildly inaccurate
**Solution:**
- This is normal! Distance estimation is approximate
- Works best for objects within 50cm - 2m range
- Accuracy improves with camera calibration

### Problem: Console prints too fast
**Solution:**
- That's fixed now! It only prints once per second
- Watch the **video window** for real-time feedback

---

## 📊 **RECOMMENDED TESTING ORDER**

1. ✅ **vision.py** - Test camera and object detection (5 min)
2. ✅ **motor_control.py** - See motor simulation (1 min)
3. ✅ **arm_control.py** - See arm simulation (1 min)
4. ✅ **navigation.py** - See navigation logic (1 min)
5. ✅ **llm_interface.py** - Test command parsing (1 min)
6. ✅ **main.py** - Complete system integration (5 min)

**Total testing time: ~15 minutes**

---

## 🎯 **SUCCESS CRITERIA**

### ✅ Vision Test is Successful When:
- Video window opens and shows live camera feed
- Green bounding box appears around target object
- Distance shows in large green text above box
- Direction guidance appears at top
- Terminal prints distance once per second (not infinitely)

### ✅ Complete System Test is Successful When:
- System understands your command
- Camera initializes and shows video
- Object is detected
- Visual servoing approach works
- All hardware commands print correctly
- Task completes and returns to idle

---

## 🚀 **QUICK START (3 Commands)**

For the impatient:

```powershell
# Test vision (MUST DO FIRST!)
python vision.py

# Type: blue phone
# [Video window opens, show camera a blue object]

# Press 'q' when done
```

```powershell
# Test complete system
python main.py

# Type: bring me the blue phone
# [Watch it work!]

# Type: quit
```

**That's it! You're now ready to build the physical robot!** 🤖✨
