This agent implements the ReAct pattern. It doesn't just guess; it follows a logical loop:

Reasoning: The LLM (Gemini 2.5 Flash) analyzes the user prompt and determines which tool is needed.

Action: The system executes Python functions (Weather, Finance, or File System).

Safety Gate: For sensitive actions (deletion/conversion), the loop pauses for Human-in-the-loop confirmation.

Observation: The result of the tool is fed back into the LLM's memory to generate the final response.

## 🚀 Try These Prompts
1. **Weather:** "What's the temperature in Lahore?"
2. **Tasks:** "Add 'Submit AI Project' to my tasks."
3. **Multi-Tool:** "I have 100 USD. Convert it to PKR and then draft an email to ali@example.com about the exchange rate."


🎯 Goal of the Project

The goal of this project is to build a personal AI assistant system that helps users organize and manage their daily tasks automatically.

This project is part of my journey to build a Personal AI Operating System