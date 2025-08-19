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
The robot has the following skills: "fetch", "find".
The JSON output must contain three keys:
1. "action": The primary skill to use (e.g., "fetch").
2. "object_description": A simple, one or two-word description of the object to find (e.g., "red box", "blue book").
3. "object_color": The primary color of the object as a single lowercase word.

Example command: "ATLAS, can you please go find the red box for me?"
Example JSON output:
{
  "action": "fetch",
  "object_description": "red box",
  "object_color": "red"
}

Now, analyze the following user command.
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
        json_text = response.text.strip().replace('```json', '').replace('```', '').strip()
        
        plan = json.loads(json_text)
        print(f"[LLM] - Plan received: {plan}")
        return plan
        
    except Exception as e:
        print(f"[LLM] - Error generating or parsing plan: {e}")
        return None

# --- To test this script directly ---
if __name__ == "__main__":
    print("--- Testing LLM Interface ---")
    # Test with a sample command
    test_command = "Hey ATLAS, I need you to retrieve the red toolbox from across the room."
    plan = get_plan_from_command(test_command)
    
    if plan:
        print("\n--- Test Successful ---")
        print(f"Action: {plan.get('action')}")
        print(f"Object: {plan.get('object_description')}")
        print(f"Color: {plan.get('object_color')}")
    else:
        print("\n--- Test Failed ---")