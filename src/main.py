from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
from .config import config
from .tools import get_current_temperature,convert_to_pkr,manage_calendar,manage_tasks,draft_email

load_dotenv ()
GEMINI_API_KEY = os.getenv ("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print ("❌ ERROR: API_KEY not found in .env file.")
    print ("Please create a .env file and add API_KEY=your_key_here.")
    exit ()

client = genai.Client (api_key = GEMINI_API_KEY)

# Initialize an empty history
messages = []

def run_agent_loop(prompt, max_iterations=5):
    # 2. Add this line at the very start of the function!
    global messages

    messages.append (types.Content(role="user", parts=[types.Part(text=prompt)]))
    # The keys must match the "name" in your tool declarations exactly
    tools_mapping = {
        "get_current_temperature": get_current_temperature,
        "convert_to_pkr": convert_to_pkr,
        "manage_tasks": manage_tasks,
        "manage_calendar": manage_calendar,
        "draft_email": draft_email
    }
    
    for i in range(max_iterations):
        print(f"\n--- 💡 Iteration {i+1} ---")

        # Before sending 'contents=chat_history' to Gemini:
        if len(messages) > 10:
            # Keep the System Instruction (if separate) but trim the middle
            messages = messages[-10:]
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=config,
            contents=messages
        )

        # Add the AI's "thought" (the function call request) to history
        messages.append(response.candidates[0].content)
        
        tool_parts = []
        found_tool = False

        # 1. Loop through all parts to find function calls
        for part in response.candidates[0].content.parts:
            if part.function_call:
                found_tool = True
                call = part.function_call
                print(f"🛠️ Agent decided to ACT: {call.name}({call.args})")

                # NEW (Dynamic/Routing):
                tool_name = call.name  # e.g., "convert_to_pkr"

                # SAFETY GATE FOR REMOVE
                if tool_name == "manage_tasks":
                    if call.args ["action"] == "remove":
                        user_choice = input ("Are you sure you want to delete this task/event? (y/n): ")
                        if user_choice != "y":
                           observation = {"error": "User denied permission for this action."}
                        else:
                            observation = tools_mapping[call.name](**call.args)
                    else:
                        observation = tools_mapping[call.name](**call.args)       

                elif tool_name == "convert_to_pkr":
                    user_choice = input(f"⚠️  AGENT ALERT: Wants to convert {call.args['amount']}. Allow? (y/n): ")
                    if user_choice.lower() != 'y':
                        observation = {"error": "User denied permission for this action."}
                        # Skip the actual function call
                    else :
                        observation = tools_mapping[call.name](**call.args)

                else:
                    if tool_name in tools_mapping:
                        # This picks the right function and passes the right args
                        observation = tools_mapping[call.name](**call.args)  
                        print(f"👁️ Observation from {tool_name}: {observation}")
                    else:
                        observation = {"error": f"Tool '{tool_name}' not found in my system."}
            
                # Add to our collector list
                tool_parts.append(
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=call.name,
                            response=observation
                        )
                    )
                )

        # 2. DECISION TIME (Move this OUTSIDE the for loop)
        if found_tool:
            # Send the collective response back to Gemini for the next iteration
            messages.append(types.Content(role="user", parts=tool_parts)) 
        else:
            # No tool calls found in any part? We are done!
            print("✅ Final Answer Achieved!")
            return response.text # Or response.candidates[0].content.parts[0].text

    return "Max iterations reached without a final answer."