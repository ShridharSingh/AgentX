from groq import Groq
import math
import json
from dotenv import load_dotenv
import os
from tools import *
from models import choose_model

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
    elif tool_name == "web_search":
        return web_search(tool_args["query"])
    elif tool_name == "get_real_weather":
        city = (tool_args or {}).get("city", DEFAULT_CITY)
        return get_real_weather(city)
    else:
        return f"Unknown tool: {tool_name}"

# ── 3. Agent loop ─────────────────────────────────────────────────────────────

def run_agent(user_message: str, model: str):
    print(f"\nUser: {user_message}\n")

    messages = [
        {"role": "system", "content": """You are a helpful AI assistant with access to tools.

        RULES — follow these without exception:
        - For the current date or time: ALWAYS call get_current_datetime. Never answer from memory.
        - For any maths: ALWAYS call calculate. Never calculate in your head.
        - For weather: ALWAYS call get_real_weather. Never guess.
        - For weather questions that include 'right now', 'currently', or 
        'at this moment', call get_current_datetime first, then call 
        get_real_weather, and combine both results into one answer.
        - For current news, sports, rankings, or anything you are unsure about: ALWAYS call web_search.
        - After you receive the results from a tool, you MUST write a final answer to the user in plain text.
        - Do NOT call the same tool twice in a row for the same query.
        - Do NOT keep calling tools if you already have enough information to answer.
        - Always tell the user which tool you used.
        """
        },
        {"role": "user", "content": user_message}
    ]
    max_iterations = 0 
    iteration = 0

    while True:
        if iteration >= max_iterations:
            print(f"[Max interations reached - forcing final answer]\n")
            messages.append({
                "role": "user",
                "content": "You have already gathered enough information. Stop calling tools and write your final answer to the user now."
            })
            iteration += 1

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        reply = response.choices[0].message
        reply_dict = {"role": "assistant", "content": reply.content or ""}

        if reply.tool_calls: 
            reply_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.arguments,
                        "arguments": tc.function.arguments or "{}"
                    }
                }
                 for tc in reply.tool_calls
            ]
        messages.append(reply_dict)

        if reply.tool_calls:
            print("Agent is using tools...\n")
            for tool_call in reply.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments or "{}")


                print(f"  Calling tool : {tool_name}")
                print(f"  With inputs  : {tool_args}")

                result = run_tool(tool_name, tool_args)

                if result is None:
                    resut = "Tool returned no results."

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

    selected_model = choose_model()

    print(" Chat is continuous. Type 'quit' or 'exit' or 'bye' to end chat.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Goodbye!")
            break

        run_agent(user_input, model=selected_model)