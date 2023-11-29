import json
from typing import List, Dict


class MistralContext:

    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_user_message(self, entry: str):
        self.messages.append({"role": "user", "content": entry})

    def add_assistant_message(self, entry: str):
        self.messages.append({"role": "assistant", "content": entry})

    def update_last_message_content(self, entry:str):
        if not len(self.messages): raise IndexError("There is no message to update for the context")
        self.messages[-1]["content"] = entry

    def __str__(self):
        return json.dumps(self.messages, indent=4, ensure_ascii=False)