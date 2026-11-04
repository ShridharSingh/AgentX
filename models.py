# All compatible models listed here.
# To add a new model, add a new entry to the MODELS dict below.

MODELS = {
    "1": {
        "label": "GPT-OSS 120B (Groq) - most compatible, free",
        "id": "openai/gpt-oss-120b",
    },
    "2": {
        "label": "Qwen 3.8 27B (Groq) - lightweight alternative, free",
        "id": "qwen/qwen3.8-27b",
    },
    "3": {
        "label": "GPT-OSS 20B (Groq) - fastest, smallest, free",
        "id": "openai/gpt-oss-20b",
    },
}

DEFAULT_MODEL_KEY = "1"  # change this to switch the default


def choose_model() -> str:
    """Prints the model menu, prompts the user to pick one, and returns the model ID string to pass to the API. Pressing enter without typing anything selects the default."""

    print("\n" + "=" * 50)
    print(" AgentX - Model Selection")
    print("=" * 50)

    for key, model in MODELS.items():
        default_marker = " [default]" if key == DEFAULT_MODEL_KEY else ""
        print(f" {key}. {model['label']}{default_marker}")

    print("=" * 50)

    while True:
        choice = input(" Choose a model (press Enter for default): ").strip()

        # User pressed Enter - Default open chosen
        if choice == "":
            selected = MODELS[DEFAULT_MODEL_KEY]
            print(f"\n Using default: {selected['label']}\n")
            return selected["id"]

        # User selected a valid choice
        if choice in MODELS:
            selected = MODELS[choice]
            print(f"\n Using: {selected['label']}\n")
            return selected["id"]

        # User selected invalid choice
        print(f" Invalid choice. Please enter a number between 1 and {len(MODELS)}.\n")
