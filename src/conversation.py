"""Keeps track of the running conversation, the active tutor mode, and mistakes."""

import re
from datetime import datetime

from prompts import TUTORS, DEFAULT_LEVEL
from llm_client import OllamaClient
import config

MISTAKE_RE = re.compile(r"<mistake>(.*?)\|(.*?)</mistake>", re.DOTALL)


class ConversationManager:
    def __init__(self, model=None):
        self.model = model or config.DEFAULT_MODEL
        self.client = OllamaClient(self.model)
        self.language = "english"
        self.level = DEFAULT_LEVEL[self.language]
        self.history = []  # list of {"role", "content"} excluding system prompt
        self.mistakes = []  # list of (timestamp, original, correction)
        self.session_start = datetime.now()

    def set_language(self, language):
        language = language.lower()
        if language not in TUTORS:
            raise ValueError(f"Unknown language '{language}'. Choices: {list(TUTORS)}")
        self.language = language
        self.level = DEFAULT_LEVEL[language]
        self.history = []  # fresh conversation when switching languages

    def set_level(self, level):
        self.level = level.upper()

    def _system_prompt(self):
        return TUTORS[self.language].format(level=self.level)

    def _build_messages(self):
        messages = [{"role": "system", "content": self._system_prompt()}]
        messages.extend(self.history[-(config.HISTORY_TURNS * 2):])
        return messages

    def send(self, user_text):
        self.history.append({"role": "user", "content": user_text})
        messages = self._build_messages()
        reply = self.client.chat(messages)
        self.history.append({"role": "assistant", "content": reply})
        self._extract_mistakes(reply)
        return self._strip_mistake_tags(reply)

    def _extract_mistakes(self, reply):
        for original, correction in MISTAKE_RE.findall(reply):
            self.mistakes.append((datetime.now(), original.strip(), correction.strip()))

    @staticmethod
    def _strip_mistake_tags(reply):
        return MISTAKE_RE.sub(lambda m: m.group(2).strip(), reply).strip()

    def report(self):
        duration = datetime.now() - self.session_start
        minutes = int(duration.total_seconds() // 60)
        lines = [f"Session: {minutes} min | Language: {self.language} | Level: {self.level}"]
        if not self.mistakes:
            lines.append("No corrections logged yet.")
        else:
            lines.append(f"Corrections ({len(self.mistakes)}):")
            for _, original, correction in self.mistakes[-10:]:
                lines.append(f'  "{original}" -> "{correction}"')
        return "\n".join(lines)
