"""
SmartKDB v5 - The Cognitive AI-Native Database Platform
"""

__version__ = "5.0.4"

from .core.engine import SmartKDB, KTable, QueryBuilder
from .core.transaction import Transaction, TransactionManager, TransactionState
from .core.versioning import VersionManager
from .core.distributed import NodeManager
from .ai.brain import Brain
from .ai.trainer import Trainer
from .ai.llm_connectors import LLMConnector
from .plugins.manager import PluginManager

__all__ = [
    "SmartKDB",
    "KTable",
    "QueryBuilder",
    "Transaction",
    "TransactionManager",
    "TransactionState",
    "VersionManager",
    "NodeManager",
    "Brain",
    "Trainer",
    "LLMConnector",
    "PluginManager",
]

__author__ = "Alhdrawi"
