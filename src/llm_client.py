"""Thin client for talking to a local Ollama server."""

import requests

from config import OLLAMA_HOST, MAX_RESPONSE_TOKENS


class OllamaClient:
    def __init__(self, model, host=OLLAMA_HOST):
        self.model = model
        self.host = host.rstrip("/")

    def chat(self, messages):
        """Send a full chat history to Ollama and return the assistant's reply.

        messages: list of {"role": "system"|"user"|"assistant", "content": str}
        """
        url = f"{self.host}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_predict": MAX_RESPONSE_TOKENS,
            },
        }
        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
        except requests.exceptions.ConnectionError as exc:
            raise RuntimeError(
                "Could not reach Ollama at "
                f"{self.host}. Is the Ollama app running?"
            ) from exc
        except requests.exceptions.HTTPError as exc:
            detail = ""
            try:
                detail = resp.json().get("error", "")
            except Exception:
                pass
            raise RuntimeError(
                f"Ollama rejected the request for model '{self.model}'"
                + (f": {detail}" if detail else "")
                + ". Run `ollama list` and update DEFAULT_MODEL in src/config.py "
                "if the name doesn't match."
            ) from exc
        data = resp.json()
        return data["message"]["content"]
