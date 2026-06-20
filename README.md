# AgentX

### AgentX is an AI agent that utilises tools to perform certain functions

- Tools available to AgentX are still being developed and tested however you are free to have fun with whatever is supplied out-of-the-box

# Tools shipped with AgentX

#### 1. Real-time Time and Date - `Have fun asking AgentX how old it is`

#### 2. Mathematical Calculation - `Ask AgentX to perform any mathematical ]calculation using plain-text`

#### 3. Dummy weather data `(Ask agentX what the weather is like in prime cities)` (API integration to follow soon)

#### 4. Web search (In development) - `Ask AgentX to search the web for results`

## Pre-requisite software

Ensure you have the latest version of Python and Visual Studio Code installed

##### Download Python here: https://www.python.org/downloads/

##### Download Visual Studio Code here: https://code.visualstudio.com/Download

## How to use:

### Step 0 - Clone the repository

Open a terminal and type the command

```
git clone https://github.com/ShridharSingh/AgentX.git
```

### Step 1 - Create the virtual environment

```
python.exe -m venv .venv
```

Tip: See why we create a virtual environment below

### Step 2 - Install dependecies

```
pip install requirements.txt
```

### Step 3 - Input API Key

Create a `.env` file in the project folder and enter your OpenAI API key as follows:

```
GROQ_API_KEY = "gsk-xxx"
```

#### Step 4 - Run application

```
python run AgentX.py
```

## Future expansion

1. Further toolkit expansion
2. User interface compatibility with `Streamlit`
3. User choice of models
4. `LangChain` integration
