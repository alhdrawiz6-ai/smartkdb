import os
import pickle
from typing import Dict, List, Any

class Index:
    def __init__(self, path: str):
        self.path = path
        self.data: Dict[Any, Any] = {} # Key -> Offset or List[Offset]
        self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "rb") as f:
                    self.data = pickle.load(f)
            except:
                self.data = {}

    def save(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.data, f)

    def set(self, key: Any, value: Any):
        self.data[key] = value

    def get(self, key: Any) -> Any:
        return self.data.get(key)

    def remove(self, key: Any):
        if key in self.data:
            del self.data[key]

class SecondaryIndex(Index):
    def add(self, key: Any, value: Any):
        if key not in self.data:
            self.data[key] = []
        if value not in self.data[key]:
            self.data[key].append(value)

    def remove_val(self, key: Any, value: Any):
        if key in self.data and value in self.data[key]:
            self.data[key].remove(value)
            if not self.data[key]:
                del self.data[key]
