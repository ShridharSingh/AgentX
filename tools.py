from datetime import datetime
import math

# ──── Tool definitions  ──────────────────────────────────────────────────────

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a maths expression and returns the result. Use this for any arithmetic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid Python math expression, e.g. '47 * 83' or '47 multiplied by 83' or '(100 / 4) ** 2'"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Returns mock weather info for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Returns the REAL current date and time from the system clock. ALWAYS use this — never guess the date from memory.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "search_web",
        "description": "Searches the web and returns results. Use this when the user asks about current events, news, or anything you don't know.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query, e.g. 'latest AI news 2025'"
                }
            },
            "required": ["query"]
        }
    }
}
]

# ──── Python functions ─────────────────────────────────────────────────────────

def calculate(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_weather(city: str) -> str:
    mock_data = {
        "london":   "Cloudy, 14°C",
        "durban":   "Sunny, 27°C",
        "new york": "Rainy, 18°C",
    }
    return mock_data.get(city.lower(), f"No weather data for {city}")

def get_current_datetime() -> str:
    time = datetime.now()
    return time.strftime("Date: %A %d %B %Y | Time: %H:%M:%S")

