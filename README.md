# AgentX

### The Swiss Army Knife of AI Agents

AgentX is a modular, extensible AI agent built on the Groq API.
It uses a tool-calling loop to connect a large language model to
real-world functions — web search, live datetime, mathematical
calculation, and more — with model selection built in.

> Tools are in continuous development. New tools and models are
> added regularly. Feel free to explore what ships out of the box
> and check back for updates.

---

## How it works

AgentX runs a tool-calling agent loop:

1. Your message is added to a conversation history
2. The LLM reads the full history and decides whether to call a
   tool or respond directly
3. If a tool is called, AgentX runs the corresponding Python
   function locally and feeds the result back to the LLM
4. The loop continues until the LLM has enough information to
   produce a final answer

The LLM never executes code — it only requests tool calls.
AgentX handles all execution locally.

---

## Tools shipped with AgentX

| Tool                   | Description                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| `web_search`           | Live web search via DuckDuckGo — no API key needed                           |
| `get_current_datetime` | Real-time date and time from your system clock                               |
| `calculate`            | Natural language mathematical expressions                                    |
| `get_weather`          | Live weather via OpenWeatherMap API — temperature, description, and humidity |

---

## Model selection

AgentX ships with multiple compatible models. At startup, you
choose which model powers the agent for that session.

Models are defined in `models.py`. You can add your own by
inserting an entry into the `MODELS` dictionary — no other
changes required.

All models listed are free tier compatible via Groq.

---

## Prerequisites

- Python 3.10 or higher — https://www.python.org/downloads/
- A free Groq API key — https://console.groq.com
- A free OpenWeatherMap API key — https://openweathermap.org/api
- Visual Studio Code (recommended) — https://code.visualstudio.com

---

## Installation

**Step 1 — Clone the repository**

```bash
git clone https://github.com/ShridharSingh/AgentX.git
cd AgentX
```

**Step 2 — Create a virtual environment**

```bash
python -m venv .venv

# Activate it:
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

> A virtual environment keeps AgentX's dependencies isolated from
> your system Python installation, preventing version conflicts
> across projects.

**Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4 — Add your API keys**

Create a `.env` file in the project root:

```
GROQ_API_KEY="paste_your_gsk_key_here"
OPENWEATHERMAP_API_KEY="paste_your_openweathermap_key_here"
```

- Groq key: https://console.groq.com — free, no credit card required
- OpenWeatherMap key: https://openweathermap.org/api — free tier; new keys can take a while to activate

Without the OpenWeatherMap key, AgentX still runs, but weather requests will fail and the weather tests will be skipped.

> `.env` is already excluded via `.gitignore`, so your API keys
> are never committed to the repository.

**Step 5 — Verify your tools (recommended)**

```bash
python tool_verification.py
```

This tests every tool independently of the LLM. Run this any time
you add a new tool or hit unexpected behaviour.

**Step 6 — Run AgentX**

```bash
python AgentX.py
```

---

## Project structure

```
AgentX/
├── .gitignore             — Keeps .env and .venv out of Git
├── .env                   — Your API keys (not committed to Git)
├── AgentX.py              — Agent loop and entry point
├── tools.py               — Tool definitions and Python functions
├── models.py              — Compatible model registry
├── tool_verification.py   — Standalone tool testing suite
├── requirements.txt       — Python dependencies
├── LICENSE
└── README.md
```

---

## Roadmap

- [x] Core agent loop with tool calling
- [x] Web search via DuckDuckGo
- [x] Real-time datetime tool
- [x] Mathematical expression evaluator
- [x] Multi-model selection at startup
- [x] Standalone tool verification suite
- [x] Live weather API integration
- [ ] Persistent chat history
- [ ] Streamlit web interface
- [ ] Expanded tool library

---

## Research context

AgentX is developed alongside MSc research into trustworthy and
Agentic AI systems. The project serves as a practical testbed for
studying tool-calling reliability, agent loop design, and LLM
failure modes in production-like environments.

---

## License

© 2026 Shridhar Singh. All rights reserved.

This project is proprietary software. No part of this codebase
may be copied, modified, distributed, or used without explicit
written permission from the author.
