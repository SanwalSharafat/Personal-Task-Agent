This agent implements the ReAct pattern. It doesn't just guess; it follows a logical loop:

Reasoning: The LLM (Gemini 2.5 Flash) analyzes the user prompt and determines which tool is needed.

Action: The system executes Python functions (Weather, Finance, or File System).

Safety Gate: For sensitive actions (deletion/conversion), the loop pauses for Human-in-the-loop confirmation.

Observation: The result of the tool is fed back into the LLM's memory to generate the final response.
