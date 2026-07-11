from datetime import datetime
from ddgs import DDGS
from dotenv import load_dotenv
import math, requests, os

load_dotenv()

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
            "name": "web_search",
            "description": "Searches the web and returns results. Use this when the user asks about current events, news, or anything you don't know.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g. 'latest AI news 2026' or anything that has the word 'search' in it."
                    }
                },
                "required": ["query"]
            }
        }   
    },
    {
        
        "type": "function",
        "function": {
            "name": "get_real_weather",
            "description": """Returns real-time current weather for a city using 
            the OpenWeatherMap API. Use this whenever the user asks about current weather 
            or conditions outside. If the user does not specify a city, use the default 
            city of Durban. Never guess weather conditions — always call this tool.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for. Defaults to Durban if not specified by the user."
                    }
                },
                "required": []
            }
        }
    }
]

# ──── Python functions ─────────────────────────────────────────────────────────

def calculate(expression: str) -> str:
    try:
        safe_globals = {**vars(math), "math": math, "__builtins__": {}}
        result = eval(expression, safe_globals)
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

DEFAULT_CITY = "Durban"
def get_real_weather(city: str = DEFAULT_CITY) -> str:
    weather_client_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_client_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"Could not find weather for {city}"
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        return f"{city}: {description}, {temp}°C, humidity {humidity}%"
    except Exception as e:
        return f"Weather error: {e}"


def get_current_datetime() -> str:
    time = datetime.now()
    return time.strftime("Date: %A %d %B %Y | Time: %H:%M:%S")

def web_search(query: str) -> str:
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."
        output = ""
        for r in results:
            output += f"Title: {r['title']}\n"
            output += f"Summary: {r['body']}\n"
            output += f"URL: {r['href']}\n\n"
        return output.strip()
    except Exception as e:
        return f"Web search error: {e}"