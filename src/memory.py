
import json
import os
from dataclasses import dataclass
from typing import Literal

Role = Literal["user", "assistant"]

HISTORY_FILE = "chat_history.json"


@dataclass
class Message:
    role: Role
    content: str

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}


class ConversationMemory:

    def __init__(self):
        self._messages: list[Message] = []

    def add_user_message(self, text: str) -> None:
        self._messages.append(Message(role="user", content=text))

    def add_assistant_message(self, text: str) -> None:
        self._messages.append(Message(role="assistant", content=text))

    def get_history(self) -> list[dict]:
        return [msg.to_dict() for msg in self._messages]

    def clear(self) -> None:
        """Wipe memory in RAM. Call save() after to also clear the file."""
        self._messages.clear()

    def message_count(self) -> int:
        return len(self._messages)

    # ── Persistence ───────────────────────────────────────────────────

    def load(self, filepath: str = HISTORY_FILE) -> int:
      
        if not os.path.exists(filepath):
            return 0

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Validate and convert each dict back into a Message object
            self._messages = []
            for item in data:
                if item.get("role") in ("user", "assistant") and "content" in item:
                    self._messages.append(
                        Message(role=item["role"], content=item["content"])
                    )

            return len(self._messages)

        except (json.JSONDecodeError, KeyError):
            # File is corrupted — start fresh, don't crash
            self._messages = []
            return 0

    def save(self, filepath: str = HISTORY_FILE) -> None:
        """
        Save current memory to a JSON file.
        Overwrites the file completely each time (simple and safe).

        Called on exit, after clear, or whenever you want a checkpoint.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.get_history(), f, indent=2, ensure_ascii=False)