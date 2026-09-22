"""Command-line entry point for the local voice tutor (Phase 1: text-only).

Requirements:
- Ollama installed and running (https://ollama.com)
- A model pulled, e.g.:  ollama pull llama3.2:3b

Run:
    python src/main.py
"""

from conversation import ConversationManager

HELP = """
Commands:
  /english          switch to the English tutor
  /spanish          switch to the Spanish tutor
  /level B1|B2|C1   set your level
  /report           show a summary of your mistakes this session
  /help             show this message
  /quit             exit
Anything else is sent to the tutor as your message.
"""


def main():
    manager = ConversationManager()
    print("Local Voice Tutor -- Phase 1 (text-only)")
    print(f"Mode: {manager.language} | Level: {manager.level}")
    print(HELP)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue

        if user_input == "/quit":
            print("Bye!")
            break
        if user_input == "/help":
            print(HELP)
            continue
        if user_input == "/english":
            manager.set_language("english")
            print(f"Switched to English tutor (level {manager.level}).")
            continue
        if user_input == "/spanish":
            manager.set_language("spanish")
            print(f"Switched to Spanish tutor (level {manager.level}).")
            continue
        if user_input.startswith("/level"):
            parts = user_input.split()
            if len(parts) == 2:
                manager.set_level(parts[1])
                print(f"Level set to {manager.level}.")
            else:
                print("Usage: /level B1|B2|C1")
            continue
        if user_input == "/report":
            print(manager.report())
            continue

        try:
            reply = manager.send(user_input)
        except RuntimeError as exc:
            print(f"[error] {exc}")
            continue

        print(f"Tutor: {reply}")


if __name__ == "__main__":
    main()
