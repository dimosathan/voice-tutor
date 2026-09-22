# Local Voice Tutor

A fully local, offline English & Spanish conversation tutor. No subscriptions,
no API keys, no usage limits -- everything runs on your own machine.

This repo is being built in phases (see the project plan). Right now it
implements **Phase 1: a text-only conversation loop against a local LLM**
served by [Ollama](https://ollama.com). Voice input/output comes in later
phases.

## Requirements

- Windows, with [Ollama](https://ollama.com/download) installed and running
  (it runs as a background app / tray icon once installed).
- Python 3.10+ (`python --version` to check).
- At least one model pulled, e.g.:

  ```powershell
  ollama pull llama3.2:3b
  ```

## Setup (run these in PowerShell, in this folder)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```powershell
python src\main.py
```

Type normally to chat with the tutor. Commands:

- `/english` -- switch to the English tutor
- `/spanish` -- switch to the Spanish tutor
- `/level B1|B2|C1` -- set your level
- `/report` -- see a summary of mistakes logged this session
- `/help` -- show the command list
- `/quit` -- exit

## Project structure

```
voice-tutor/
  src/
    config.py        settings (model name, token limits, history length)
    prompts.py        the "personality" / system prompts for each tutor
    llm_client.py      talks to the local Ollama HTTP API
    conversation.py   conversation history, mode switching, mistake tracking
    main.py           the command-line chat loop (entry point)
```

## Roadmap

- [x] Phase 0-1: project skeleton + text-only chat against local Ollama
- [ ] Phase 2: speech-to-text (microphone -> faster-whisper)
- [ ] Phase 3: text-to-speech (Piper voices)
- [ ] Phase 4: full voice loop with voice-activity detection
- [ ] Phase 5: richer personality system / scenarios
- [ ] Phase 6: mistake tracking reports
- [ ] Phase 7-8: polish + latency tuning
