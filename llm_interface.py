# llm_interface.py
import google.generativeai as genai
import config
import json

# Configure the generative AI model
genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Pre-defined prompt to instruct the AI
PROMPT = """
You are the task planning system for a mobile robot named ATLAS.
Your job is to receive a natural language command and convert it into a structured JSON plan.

The robot has the following capabilities:
- "fetch": Navigate to an object, pick it up, and bring it back to the user
- "find": Navigate to an object and report its location
- "deliver": Pick up an object and deliver it to a specified location

The JSON output must contain these keys:
1. "action": The primary skill to use (e.g., "fetch", "find", or "deliver")
2. "object_description": A simple description of the object (e.g., "red box", "blue phone", "green book", "pen", "cup")
3. "object_color": The primary color of the object as a single lowercase word (e.g., "red", "blue", "green", "yellow", "black", "white")
   - If no color is specified, try to infer it or use "unknown"
4. "object_type": The type/category of object (e.g., "phone", "book", "pen", "cup", "tool", "box", "ball", "bottle")

IMPORTANT INSTRUCTIONS:
- Extract color and object type separately
- If user says just "phone", extract object_type as "phone" and object_color as "unknown"
- If user says "blue phone", extract object_type as "phone" and object_color as "blue"
- Be flexible with object descriptions - understand synonyms (e.g., "cell phone" = "phone", "notebook" = "book")
- For compound commands, focus on the main action and primary object

Examples:

Command: "ATLAS, can you please go find the red box for me?"
Output:
{
  "action": "fetch",
  "object_description": "red box",
  "object_color": "red",
  "object_type": "box"
}

Command: "Hey ATLAS, bring me my phone"
Output:
{
  "action": "fetch",
  "object_description": "phone",
  "object_color": "unknown",
  "object_type": "phone"
}

Command: "ATLAS find the blue ball"
Output:
{
  "action": "find",
  "object_description": "blue ball",
  "object_color": "blue",
  "object_type": "ball"
}

Command: "Get the green book from the desk"
Output:
{
  "action": "fetch",
  "object_description": "green book",
  "object_color": "green",
  "object_type": "book"
}

Now, analyze the following user command and return ONLY the JSON (no additional text).
Command:
"""

def get_plan_from_command(text_command: str) -> dict | None:
    """
    Sends a command to the Gemini API and returns a structured plan.
    
    Args:
        text_command: The natural language command from the user.
        
    Returns:
        A dictionary representing the JSON plan, or None if an error occurs.
    """
    full_prompt = PROMPT + f'"{text_command}"'
    
    try:
        response = model.generate_content(full_prompt)
        
        # Clean up the response to extract only the JSON part
        json_text = response.text.strip()
        
        # Remove markdown code blocks if present
        json_text = json_text.replace('```json', '').replace('```', '').strip()
        
        # Try to find JSON object in the response
        start = json_text.find('{')
        end = json_text.rfind('}') + 1
        if start != -1 and end > start:
            json_text = json_text[start:end]
        
        plan = json.loads(json_text)
        
        # Validate required fields
        required_fields = ['action', 'object_description', 'object_color', 'object_type']
        for field in required_fields:
            if field not in plan:
                print(f"[LLM] - WARNING: Missing field '{field}' in plan")
                plan[field] = 'unknown'
        
        print(f"[LLM] - Plan received: {plan}")
        return plan
        
    except json.JSONDecodeError as e:
        print(f"[LLM] - Error parsing JSON: {e}")
        print(f"[LLM] - Response was: {response.text}")
        return None
    except Exception as e:
        print(f"[LLM] - Error generating or parsing plan: {e}")
        return None


def extract_object_info(text_command: str) -> dict | None:
    """
    Alternative function to extract object information without full LLM.
    Useful as a fallback or for testing without API key.
    
    Args:
        text_command: The natural language command
        
    Returns:
        Dictionary with object information
    """
    text_lower = text_command.lower()
    
    # Common colors
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'black', 'white', 'brown', 'pink']
    
    # Common objects
    objects = ['phone', 'book', 'pen', 'pencil', 'cup', 'bottle', 'box', 'ball', 'tool', 
               'hammer', 'screwdriver', 'wrench', 'notebook', 'marker', 'eraser']
    
    # Extract color
    found_color = 'unknown'
    for color in colors:
        if color in text_lower:
            found_color = color
            break
    
    # Extract object
    found_object = 'object'
    for obj in objects:
        if obj in text_lower:
            found_object = obj
            break
    
    # Determine action
    action = 'fetch'
    if 'find' in text_lower and 'bring' not in text_lower:
        action = 'find'
    
    # Build description
    if found_color != 'unknown':
        description = f"{found_color} {found_object}"
    else:
        description = found_object
    
    result = {
        'action': action,
        'object_description': description,
        'object_color': found_color,
        'object_type': found_object
    }
    
    print(f"[LLM] - Extracted info: {result}")
    return result

# --- To test this script directly ---
if __name__ == "__main__":
    print("=== Testing LLM Interface ===\n")
    
    # Test with various sample commands
    test_commands = [
        "Hey ATLAS, I need you to retrieve the red toolbox from across the room.",
        "ATLAS, can you find my phone?",
        "Get me the blue book",
        "ATLAS find the green ball",
        "Bring me that black pen on the desk"
    ]
    
    for i, test_command in enumerate(test_commands):
        print(f"\n--- Test {i+1} ---")
        print(f"Command: \"{test_command}\"")
        
        # Try LLM-based extraction first
        if config.GEMINI_API_KEY:
            plan = get_plan_from_command(test_command)
        else:
            print("[LLM] - No API key found, using fallback extraction")
            plan = extract_object_info(test_command)
        
        if plan:
            print("✓ Success!")
            print(f"  Action: {plan.get('action')}")
            print(f"  Object: {plan.get('object_description')}")
            print(f"  Color: {plan.get('object_color')}")
            print(f"  Type: {plan.get('object_type')}")
        else:
            print("✗ Failed to parse command")
    
    print("\n=== LLM Interface Test Complete ===")
