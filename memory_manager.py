# memory_manager.py
import json
import os

class ScriptMemory:
    def __init__(self, filename="script_memory.json"):
        self.filename = filename
        self.data = {"script": {}, "current_node": None}
        self._load()

    def _load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                pass

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)

    def set_step(self, node_name, content):
        self.data["script"][node_name] = content
        self.data["current_node"] = node_name
        self.save()

    def get_step(self, node_name):
        return self.data["script"].get(node_name)

    def get_last_node(self):
        return self.data.get("current_node")

    def clear(self):
        self.data = {"script": {}, "current_node": None}
        self.save()
