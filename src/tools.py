import json, requests, os
from dotenv import load_dotenv

load_dotenv ()
WEATHER_API_KEY = os.getenv ("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    print ("❌ ERROR: API_KEY not found in .env file.")
    print ("Please create a .env file and add API_KEY=your_key_here.")
    exit ()

# Actual Weather Function
def get_current_temperature (location: str) -> dict:
    try :

        url = "https://api.openweathermap.org/data/2.5/weather"
    
        params = {
            'q' : location,
            'appid' : WEATHER_API_KEY,
            'units' : 'metric'
        }
        response = requests.get (url, params=params)
        response.raise_for_status ()
        data = response.json() 

        return {
            "location": data["name"],
            "temperature_celsius": data["main"]["temp"],
            "conditions": data["weather"][0]["description"].capitalize(),
            "humidity_percent": data["main"]["humidity"],
        }
    except Exception as e:
        return {"error": f"Could not find weather for '{location}'. Please check the spelling."}

def convert_to_pkr(amount: float, currency_code: str) -> dict:
    # Mock rates for testing
    rates = {"USD": 278.5, "GBP": 353.2, "EUR": 301.1}
    
    code = currency_code.upper()
    if code in rates:
        converted = amount * rates[code]
        return {"original": f"{amount} {code}", "pkr": f"{converted:.2f} PKR"}
    else:
        return {"error": f"Currency {code} not supported yet."}        
    
def manage_tasks(action: str, task: str = None) -> dict:
    # file_path = r'C:\Users\Laptop Gallery\OneDrive\Desktop\learn\week_4\tasks.json'
    # Instead of C:\Users\..., use:
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "tasks.json")
    
    # Ensure the file exists
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    # Read current tasks
    with open(file_path, 'r') as f:
        tasks = json.load(f)

    if action == "add" and task:
        tasks.append(task)
        with open(file_path, 'w') as f:
            json.dump(tasks, f)
        return {"status": "success", "message": f"Added task: {task}"}

    elif action == "list":
        return {"status": "success", "tasks": tasks}

    elif action == "remove" and task:
        if task in tasks:
            tasks.remove(task)
            with open(file_path, 'w') as f:
                json.dump(tasks, f)
            return {"status": "success", "message": f"Removed task: {task}"}
        return {"status": "error", "message": "Task not found."}

    return {"status": "error", "message": "Invalid action."}

def manage_calendar(action: str, event_name: str = None, date: str = None, time: str = None) -> dict:
    # file_path = r'C:\Users\Laptop Gallery\OneDrive\Desktop\learn\week_4\calender.json'
    # Instead of C:\Users\..., use:
    base_dir = os.path.dirname(__file__)
    # 1. Define the actual file path first
    file_path = os.path.join(base_dir, "../data/calendar.json")

    # 2. Extract the directory name from that path
    data_dir = os.path.dirname(file_path)

    # 3. Create the directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 4. Create the file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump([], f)

    with open(file_path, 'r') as f:
        events = json.load(f)

    if action == "add" and event_name and date and time:
        new_event = {"event": event_name, "date": date, "time": time}
        events.append(new_event)
        with open(file_path, 'w') as f:
            json.dump(events, f)
        return {"status": "success", "message": f"Scheduled '{event_name}' on {date} at {time}."}

    elif action == "list":
        if not events:
            return {"status": "success", "message": "Your calendar is currently empty."}
        return {"status": "success", "events": events}
    
    return {"status": "error", "message": "Invalid action or missing parameters (event_name, date, time)."}

def draft_email(recipient: str, subject: str, context: str) -> dict:
    # A simple template generator
    draft = f"To: {recipient}\nSubject: {subject}\n\nHi {recipient.split('@')[0].capitalize()},\n\n"
    draft += f"I'm writing to you regarding {context}.\n\nBest regards,\nYour AI Assistant"
    
    return {"status": "success", "draft": draft}    