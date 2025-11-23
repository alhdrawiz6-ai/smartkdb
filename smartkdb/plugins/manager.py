import importlib
import os
import sys
from typing import Dict, Any

class PluginManager:
    def __init__(self, db):
        self.db = db
        self.plugins: Dict[str, Any] = {}
        self.plugin_dir = os.path.dirname(__file__)

    def load_plugins(self):
        """
        Scan the plugins directory and load valid plugins.
        """
        sys.path.append(self.plugin_dir)
        
        for item in os.listdir(self.plugin_dir):
            if item.startswith("__") or item == "manager.py":
                continue
                
            plugin_path = os.path.join(self.plugin_dir, item)
            if os.path.isdir(plugin_path) or item.endswith(".py"):
                module_name = item[:-3] if item.endswith(".py") else item
                try:
                    module = importlib.import_module(f"smartkdb.plugins.{module_name}")
                    if hasattr(module, "register"):
                        module.register(self.db)
                        self.plugins[module_name] = module
                        print(f"Loaded plugin: {module_name}")
                except Exception as e:
                    print(f"Failed to load plugin {module_name}: {e}")

    def get_plugin(self, name: str):
        return self.plugins.get(name)
