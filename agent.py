# agent.py  —  full AI agent in one file

from groq import Groq
import math
import json
from dotenv import load_dotenv
import os

# ── 1. Connect to Groq ────────────────────────────────────────────────────────

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── 2. Tool definitions (what the LLM knows about) ───────────────────────────

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a maths expression and returns the result.",
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
            "description": "Returns weather info for a city.",
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
    }
]

# ── 3. Actual Python functions (what really runs) ─────────────────────────────

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

# ── 4. Tool dispatcher ────────────────────────────────────────────────────────

def run_tool(tool_name: str, tool_args: dict) -> str:
    if tool_name == "calculate":
        return calculate(tool_args["expression"])
    elif tool_name == "get_weather":
        return get_weather(tool_args["city"])
    else:
        return f"Unknown tool: {tool_name}"

# ── 5. Agent loop ─────────────────────────────────────────────────────────────

def run_agent(user_message: str):
    print(f"\nUser: {user_message}\n")

    messages = [
        {"role": "user", "content": user_message}
    ]

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        reply = response.choices[0].message
        messages.append(reply)

        if reply.tool_calls:
            print("Agent is using tools...\n")
            for tool_call in reply.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"  Calling tool : {tool_name}")
                print(f"  With inputs  : {tool_args}")

                result = run_tool(tool_name, tool_args)

                print(f"  Result       : {result}\n")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
        else:
            final_answer = reply.content
            print(f"Agent: {final_answer}\n")
            return final_answer

# ── 6. Run it ─────────────────────────────────────────────────────────────────


run_agent("What is the weather in Durban?")
run_agent("What is the square root of 1764, and what is the weather in London?")
run_agent("What is 47 multiplied by 83?")