"""Configuration for the local voice tutor."""

# Ollama server settings
OLLAMA_HOST = "http://localhost:11434"

# Default model. Change this to whatever you've pulled with `ollama pull <name>`.
# Good CPU-only choices: "llama3.2:3b" (fast) or "mistral:7b" (slower, sometimes better).
DEFAULT_MODEL = "llama3.2:latest"

# How many past turns (user+assistant pairs) to keep in the prompt.
# Keeping this low keeps CPU inference fast.
HISTORY_TURNS = 8

# Max tokens the model is allowed to generate per reply.
# Keep this low for snappier responses on CPU.
MAX_RESPONSE_TOKENS = 120
