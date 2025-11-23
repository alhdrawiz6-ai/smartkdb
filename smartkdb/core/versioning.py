import time
import json
import os
from typing import List, Dict, Any, Optional

class VersionManager:
    def __init__(self, db_path: str):
        self.history_path = os.path.join(db_path, "history")
        if not os.path.exists(self.history_path):
            os.makedirs(self.history_path)

    def _get_history_file(self, table: str, record_id: str) -> str:
        # Simple file-based history: history/table_recordid.json
        # In production, this should be sharded or stored in a dedicated history table.
        safe_id = "".join([c if c.isalnum() else "_" for c in record_id])
        return os.path.join(self.history_path, f"{table}_{safe_id}.json")

    def archive_record(self, table: str, record_id: str, data: Dict[str, Any], timestamp: float = None):
        """
        Save a snapshot of the record.
        """
        if timestamp is None:
            timestamp = time.time()

        history_file = self._get_history_file(table, record_id)
        
        entry = {
            "timestamp": timestamp,
            "data": data
        }

        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
            except:
                pass # Corrupt history, start fresh
        
        history.append(entry)
        
        # Write back
        with open(history_file, "w") as f:
            json.dump(history, f)

    def get_version_at(self, table: str, record_id: str, timestamp: float) -> Optional[Dict[str, Any]]:
        """
        Get the state of a record at a specific time.
        """
        history_file = self._get_history_file(table, record_id)
        if not os.path.exists(history_file):
            return None

        try:
            with open(history_file, "r") as f:
                history = json.load(f)
        except:
            return None

        # Find the latest version <= timestamp
        # Assuming history is sorted by timestamp (append-only)
        candidate = None
        for entry in history:
            if entry["timestamp"] <= timestamp:
                candidate = entry["data"]
            else:
                break
        
        return candidate

    def get_history(self, table: str, record_id: str) -> List[Dict[str, Any]]:
        """
        Get full history of a record.
        """
        history_file = self._get_history_file(table, record_id)
        if not os.path.exists(history_file):
            return []

        try:
            with open(history_file, "r") as f:
                return json.load(f)
        except:
            return []
