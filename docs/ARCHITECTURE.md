# SmartKDB v5 Architecture 🏗️

## High-Level Design
SmartKDB v5 follows a modular architecture:

1.  **Core Engine**: Handles storage, indexing, and transactions.
2.  **AI Layer**: Observes the Core and provides intelligence.
3.  **GUI Layer**: Visualizes the state of the system.

## Directory Structure
```
smartkdb/
├── core/           # The Database Kernel
│   ├── engine.py   # Main Entry Point
│   ├── storage.py  # Block Storage (Append-Only)
│   ├── index.py    # B-Tree & Hash Indexes
│   ├── transaction.py # ACID Manager
│   └── versioning.py  # History Manager
├── ai/             # The Intelligence
│   ├── brain.py    # Query Statistics
│   ├── trainer.py  # Dataset Tools
│   └── llm_connectors.py # LLM Interface
├── gui/            # The Interface
│   ├── backend.py  # FastAPI App
│   └── frontend/   # HTML/JS Dashboard
└── plugins/        # Extensions
```

## Data Flow
1.  **Write**: `engine.py` -> `transaction.py` (Log) -> `storage.py` (Write) -> `index.py` (Update) -> `versioning.py` (Archive) -> `distributed.py` (Broadcast).
2.  **Read**: `engine.py` -> `index.py` (Lookup) -> `storage.py` (Read).
3.  **AI Loop**: `brain.py` monitors `engine.py` calls -> Updates stats -> Suggests optimizations.
