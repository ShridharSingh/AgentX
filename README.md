# AgentX

### AgentX is an AI agent that utilises tools to perform certain functions

- Tools available to AgentX are still being developed and tested however you are free to have fun with whatever is supplied out-of-the-box

# Tools shipped with AgentX

#### 1. Web search - `Ask AgentX to search the web for news, results, trends or anything really`

#### 2. Real-time Time and Date - `Have fun asking AgentX how old it is`

#### 3. Mathematical Calculation - `Ask AgentX to perform any mathematical calculation using plain-text`

#### 4. Dummy weather data `Ask agentX what the weather is like in prime cities` (API integration to follow soon)

## NEW ADDITIONS to AgentX

#### Model selection - `Users are now able to choose a compatible model to power AgentX`

- Models are provided in the `models.py` file and range from lightweight to very powerful.
- ALL models are free and work with AgentX - note that some models may work better than others depending on use cases
- AgentX ships with a default model but this can be changed in the `models.py` file
- Users are welcome to add their own models to the `MODELS` dictionary

## Screenshots of AgentX in Action

- AgentX model selection
  ![image 1](assets/images/AgentX%20User%20Model%20Selection%20Options.png)
- Using Llama 3.3 70b (Default)
  ![image 1](assets/images/VS%20code%20output%20of%20AgentX%20web_search%20tool%20using%20llama3.png)
- Using OpenAI GPT OSS 120b
  ![image 2](assets/images/VS%20code%20output%20of%20AgentX%20web_search%20tool.png)

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
