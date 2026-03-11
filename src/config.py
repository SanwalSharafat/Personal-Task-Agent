from google.genai import types

# Define the function declaration for the model
weather_function = {
    "name": "get_current_temperature",
    "description": "Gets the current temperature for a given location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city name, e.g. San Francisco",
            },
        },
        "required": ["location"],
    },
}

currency_tool_schema = {
    "name": "convert_to_pkr",
    "description": "Converts a given amount from a source currency to PKR.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "The amount to convert"},
            "currency_code": {"type": "string", "description": "The 3-letter currency code, e.g., USD, GBP, EUR"},
        },
        "required": ["amount", "currency_code"],
    },
}

todo_tool_schema = {
    "name": "manage_tasks",
    "description": "Manages a personal to-do list. Can add, list, or remove tasks.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string", 
                "enum": ["add", "list"],
                "description": "The action to perform."
            },
            "task": {
                "type": "string", 
                "description": "The description of the task (required for add/remove)."
            },
        },
        "required": ["action"],
    },
}

calendar_tool_schema = {
    "name": "manage_calendar",
    "description": "Manages a personal calendar. Can add events or list existing ones.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["add", "list", "remove"],
                "description": "The action to perform."
            },
            "event_name": {"type": "string", "description": "The name of the meeting or event."},
            "date": {"type": "string", "description": "The date in YYYY-MM-DD format."},
            "time": {"type": "string", "description": "The time in HH:MM format."},
        },
        "required": ["action"],
    },
}

tool = types.Tool (function_declarations =  [weather_function, currency_tool_schema, todo_tool_schema, calendar_tool_schema])
config = types.GenerateContentConfig (tools=[tool],
                    system_instruction="""You are a Personal Task Assistant. 
                    You can manage to-do lists and check the weather/currency"""
                    )