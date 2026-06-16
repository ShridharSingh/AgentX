# agent.py  —  full AI agent in one file

from groq import Groq
import math
import json
from dotenv import load_dotenv
import os
from tools import *

# ── 1. Connect to Groq ────────────────────────────────────────────────────────

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── 2. Tool dispatcher ────────────────────────────────────────────────────────

def run_tool(tool_name: str, tool_args: dict) -> str:
    if tool_name == "calculate":
        return calculate(tool_args["expression"])
    elif tool_name == "get_weather":
        return get_weather(tool_args["city"])
    elif tool_name == "get_current_datetime":
        return get_current_datetime()
    else:
        return f"Unknown tool: {tool_name}"

# ── 3. Agent loop ─────────────────────────────────────────────────────────────

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

# ── 4. Run it ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = run_agent(user_input)