# ATLAS Quick Start Guide

## 🎯 Quick Testing Workflow

### 1. Test Vision System First (Most Important!)

This validates that object detection works with your laptop camera:

```bash
python vision.py
```

**What to do:**
1. When prompted, enter a target: `blue phone` or `red cup` or `green book`
2. Point your laptop camera at a colorful object matching that description
3. You should see a green bounding box around the detected object
4. System will show:
   - Object center (red dot)
   - Distance estimate
   - Error from center (for visual servoing)

**Commands:**
- Press `s` to change target object
- Press `q` to quit

**Tips:**
- Use brightly colored objects (solid colors work best)
- Good lighting helps a lot
- Object should be 50cm - 2m away for best results
- If nothing detected, try adjusting lighting or object size

---

### 2. Test Motor Control (Simulation)

```bash
python motor_control.py
```

This prints what the motors would do:
- Forward movement
- Turning (left/right)
- Navigation to waypoints
- Obstacle avoidance logic

---

### 3. Test Robotic Arm (Simulation)

```bash
python arm_control.py
```

This prints arm servo movements:
- Moving to pre-defined poses
- Grab sequences
- Gripper control
- Inverse kinematics

---

### 4. Test LLM Interface

```bash
python llm_interface.py
```

Tests command understanding:
- Extracts object descriptions from natural language
- Identifies colors and object types
- Works with or without API key (has fallback)

---

### 5. Test Navigation & Visual Servoing

```bash
python navigation.py
```

Tests:
- Lawnmower search pattern generation
- Breadcrumb trail for return navigation
- Visual servoing calculations

---

### 6. Run Complete ATLAS Agent

```bash
python main.py
```

**Example Session:**

```
Enter a command: ATLAS, bring me the blue phone

[AGENT] - Planning task...
[LLM] - Plan received: {'action': 'fetch', 'object_description': 'blue phone', 'object_color': 'blue', 'object_type': 'phone'}

[AGENT] - SEARCHING for 'blue phone'...
[AGENT] - Moving to search waypoint 1/14: (0, 0)
[MOCK HARDWARE] - MOVING FORWARD for 1.00s
...
[AGENT] - ✓ OBJECT DETECTED!
[AGENT] - Estimated distance: 85.3 cm

[AGENT] - APPROACHING object using visual servoing...
[VISUAL_SERVO] - Starting visual servoing approach...
[VISUAL_SERVO] - Error: +120px | Distance: 85.3cm
[VISUAL_SERVO] - Object RIGHT by 120px → Turn RIGHT 12.0°
[MOCK HARDWARE] - TURNING RIGHT
...
[VISUAL_SERVO] - ✓ Reached target distance!

[AGENT] - Executing GRASP sequence...
[ARM] - Moving to 'ready_to_grab' pose
[ARM] - Closing gripper
[GRIPPER] - Closing gripper with medium force
[ARM] - ✓ Grasp successful!

[AGENT] - RETURNING to home position...
[AGENT] - Following breadcrumb trail...
[AGENT] - Presenting object to user...

[AGENT] - ✓✓✓ Task complete! ✓✓✓

Enter a command: quit
```

---

## 🎮 Interactive Testing Modes

### Mode 1: Vision + Manual Control

Test vision while manually controlling what happens:

```bash
python vision.py
```

Point camera at different colored objects and see real-time detection.

### Mode 2: Full Agent with Camera

Test the complete fetch sequence using your laptop camera:

```bash
python main.py
```

Then enter: `bring me the [color] [object]`

Place a colored object in view of your laptop camera. The system will:
1. Plan the task
2. Initialize camera
3. Detect object (since it's in view, skips search)
4. Perform visual servoing (print commands)
5. Execute grab sequence (simulated)
6. Return home (simulated)

---

## 🧪 Testing Checklist

Before each test session:

- [ ] Good lighting in room
- [ ] Laptop camera not blocked
- [ ] Colored objects available (red, blue, green items work best)
- [ ] Terminal/console visible for debug output
- [ ] GEMINI_API_KEY set (optional, has fallback)

---

## 🎨 Best Objects for Testing

**Excellent:**
- ✅ Colored balls (solid color)
- ✅ Colored cups/mugs
- ✅ Colored books with solid covers
- ✅ Colored phone cases
- ✅ Colored markers/pens

**Good:**
- ⚠️ Colored boxes
- ⚠️ Colored tools
- ⚠️ Colored bottles

**Difficult:**
- ❌ Shiny/reflective objects
- ❌ Transparent objects
- ❌ Small objects (< 5cm)
- ❌ Objects with multiple colors

---

## 🔍 Debugging Tips

### Object Not Detected

1. **Check color ranges** in `vision.py`:
   - Colors defined in `self.color_ranges`
   - May need to adjust HSV values for your lighting

2. **Try different colors**:
   ```python
   # In vision.py test
   vision.set_target_object("red cup")    # Red is usually easiest
   vision.set_target_object("blue phone")  # Blue works well
   vision.set_target_object("green book")  # Green good in normal lighting
   ```

3. **Check camera**:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)  # Try 0, 1, 2 for different cameras
   ret, frame = cap.read()
   print(f"Camera working: {ret}")
   cv2.imshow("Test", frame)
   cv2.waitKey(0)
   ```

### Distance Estimation Wrong

Calibrate focal length:
1. Place known object at known distance (e.g., phone at 100cm)
2. Measure pixel width in image
3. Calculate: `focal_length = (pixel_width * distance_cm) / real_width_cm`
4. Update `CAMERA_FOCAL_LENGTH` in `vision.py`

### Visual Servoing Not Working

Check in `navigation.py`:
- `center_tolerance_px` - increase if too strict (default 50)
- `turn_gain` - decrease if turning too much (default 0.1)

---

## 📊 Expected Output Format

When everything works correctly, you should see:

```
[AGENT] - Message about agent state
[VISION] - Messages about object detection
[MOTOR] - Messages about movement
[ARM] - Messages about arm control
[GRIPPER] - Messages about gripper
[NAV] - Messages about navigation
[VISUAL_SERVO] - Messages about visual servoing
[LLM] - Messages about command parsing
[MOCK HARDWARE] - What the actual hardware would do
```

All `[MOCK HARDWARE]` messages are simulations that will become real hardware commands when connected.

---

## 🚀 Next: When You Have Hardware

Once hardware is ready:

1. Uncomment hardware initialization code
2. Install hardware libraries: `pip install RPi.GPIO Adafruit-PCA9685`
3. Test motors individually first
4. Test arm servos one at a time
5. Calibrate servo positions
6. Test camera on robot
7. Full integration test

---

## 💡 Pro Tips

1. **Start simple**: Test with one bright red object first
2. **Good lighting**: Natural daylight or bright white light works best
3. **Static background**: Plain wall helps detection
4. **Size matters**: Larger objects (10-20cm) are easier to detect
5. **Distance**: Keep objects 50cm - 2m from camera initially

---

## ❓ Common Questions

**Q: Can I use this without the Gemini API key?**
A: Yes! The system has a fallback parser that extracts object info from commands.

**Q: Why isn't my camera working?**
A: Try changing `CAMERA_INDEX` in config.py from 0 to 1 or 2.

**Q: Can I add more object types?**
A: Yes! Add them to `KNOWN_OBJECT_SIZES` in `vision.py` for better distance estimation.

**Q: How accurate is distance estimation?**
A: Approximate. Good enough for navigation but needs calibration for your specific camera.

**Q: Can I test without a colored object?**
A: Not really - the vision system relies on color detection. But you can modify `vision.py` to use other detection methods (e.g., shape-based).

---

Happy testing! 🤖
