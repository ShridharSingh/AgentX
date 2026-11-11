import json
import os

from dotenv import load_dotenv
from groq import BadRequestError, Groq

from models import choose_model
from tools import (
    DEFAULT_CITY,
    calculate,
    get_current_datetime,
    get_weather,
    tools,
    web_search,
)

# ── 1. Connect to Groq ────────────────────────────────────────────────────────

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── 2. Tool dispatcher ────────────────────────────────────────────────────────


def run_tool(tool_name: str, tool_args: dict) -> str:
    args = tool_args or {}
    if tool_name == "calculate":
        return calculate(args.get("expression", ""))
    elif tool_name == "get_current_datetime":
        return get_current_datetime()
    elif tool_name == "web_search":
        return web_search(args.get("query", ""))
    elif tool_name == "get_weather":
        return get_weather(args.get("city", DEFAULT_CITY))
    else:
        return f"Unknown tool: {tool_name}"


# ── 3. Agent loop ─────────────────────────────────────────────────────────────


def run_agent(user_message: str, model: str):
    print(f"\nUser: {user_message}\n")

    messages = [
        {
            "role": "system",
            "content": """You are a helpful AI assistant with access to tools.

        RULES — follow these without exception:
        - For the current date or time: ALWAYS call get_current_datetime. Never answer from memory.
        - For any maths: ALWAYS call calculate. Never calculate in your head.
        - For weather: ALWAYS call get_weather. Never guess.
        - For weather questions that include 'right now', 'currently', or 
        'at this moment', call get_current_datetime first, then call 
        get_weather, and combine both results into one answer.
        - For current news, sports, rankings, or anything you are unsure about: ALWAYS call web_search.
        - After you receive the results from a tool, you MUST write a final answer to the user in plain text.
        - Do NOT call the same tool twice in a row for the same query.
        - Do NOT keep calling tools if you already have enough information to answer.
        - Always tell the user which tool you used.
        """,
        },
        {"role": "user", "content": user_message},
    ]
    max_iterations = 5
    iteration = 0

    while True:
        force_answer = iteration >= max_iterations
        # Once the limit is reached, forbid tool calls so the model must answer in text
        if force_answer:
            print("[Max iterations reached - forcing final answer]\n")
            messages.append(
                {
                    "role": "user",
                    "content": "You have already gathered enough information. Stop calling tools and write your final answer to the user now.",
                }
            )
            # Send no tools in the forced round: some models ignore tool_choice="none"
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
            except BadRequestError:
                final_answer = "I couldn't complete this request within the tool-call limit. Please try rephrasing your question."
                print(f"Agent: {final_answer}\n")
                return final_answer
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

        reply = response.choices[0].message
        # Act on tool calls only if the model requested them and the limit hasn't been reached
        use_tools = bool(reply.tool_calls) and not force_answer
        reply_dict = {"role": "assistant", "content": reply.content or ""}

        # Record the tool calls in the history so each tool result can be matched to its call by id
        if use_tools:
            reply_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments or "{}",
                    },
                }
                for tc in reply.tool_calls
            ]
        messages.append(reply_dict)

        # Run each requested tool and add its result to the conversation history
        if use_tools:
            print("Agent is using tools...\n")
            for tool_call in reply.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments or "{}")

                print(f"  Calling tool : {tool_name}")
                print(f"  With inputs  : {tool_args}")

                result = run_tool(tool_name, tool_args)

                if result is None:
                    result = "Tool returned no results."

                print(f"  Result       : {result}\n")

                messages.append(
                    {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                )
            iteration += 1  # One round of tool calls completed
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
