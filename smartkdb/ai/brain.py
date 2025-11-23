import json
import os
from typing import Dict, Any

class Brain:
    def __init__(self, db_path: str):
        self.path = os.path.join(db_path, "kdb_brain.json")
        self.stats = {
            "queries": {},
            "tables": {}
        }
        self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    self.stats = json.load(f)
            except:
                pass

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.stats, f)

    def log_query(self, table: str, query_type: str, duration: float):
        if table not in self.stats["tables"]:
            self.stats["tables"][table] = {"reads": 0, "writes": 0, "avg_latency": 0}
        
        t_stats = self.stats["tables"][table]
        if query_type == "read":
            t_stats["reads"] += 1
        else:
            t_stats["writes"] += 1
            
        # Moving average for latency
        t_stats["avg_latency"] = (t_stats["avg_latency"] * 0.9) + (duration * 0.1)
        
        self.save()

    def suggest_indexes(self, table: str) -> list:
        # Simple heuristic: if reads > 100 and latency > 0.1s, suggest index
        t_stats = self.stats["tables"].get(table)
        if t_stats and t_stats["reads"] > 100 and t_stats["avg_latency"] > 0.1:
            return ["Suggested: Review query patterns for missing indexes"]
        return []
