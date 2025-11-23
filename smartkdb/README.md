# SmartKDB v5 Project Structure

## Overview
This directory contains the SmartKDB v5 library source code.

## Structure

```
smartkdb/
├── __init__.py           # Main package exports
│
├── core/                 # Core Database Engine
│   ├── __init__.py
│   ├── engine.py         # SmartKDB, KTable, QueryBuilder (main classes)
│   ├── storage.py        # BlockStorage (append-only file storage)
│   ├── index.py          # Index, SecondaryIndex (B-Tree indexes)
│   ├── transaction.py    # TransactionManager, Transaction (ACID)
│   ├── versioning.py     # VersionManager (time-travel queries)
│   └── distributed.py    # NodeManager (clustering)
│
├── ai/                   # AI & Intelligence Layer
│   ├── __init__.py
│   ├── brain.py          # Brain (query learning & optimization)
│   ├── trainer.py        # Trainer (dataset quality tools)
│   └── llm_connectors.py # LLMConnector (LLM integration)
│
├── gui/                  # Web Dashboard
│   ├── __init__.py
│   ├── backend.py        # FastAPI server
│   └── frontend/         # HTML/JS interface
│       └── index.html
│
└── plugins/              # Plugin System
    ├── __init__.py
    └── manager.py        # PluginManager (plugin loader)
```

## Key Components

### Core Engine (`core/`)
The heart of SmartKDB. Handles:
- Data storage (append-only log)
- Indexing (primary & secondary)
- ACID transactions
- Version control
- Distributed operations

### AI Layer (`ai/`)
Intelligence features:
- Query pattern learning
- Performance optimization
- Dataset quality analysis
- LLM integration

### GUI (`gui/`)
Web-based control center:
- FastAPI REST API
- HTML/JS dashboard
- Real-time monitoring

### Plugins (`plugins/`)
Extensibility system:
- Custom analyzers
- External AI modules
- Visualization plugins

## Import Structure

Users import from the main package:
```python
from smartkdb import SmartKDB, KTable
```

This is defined in `__init__.py` which exposes:
- SmartKDB (main class)
- KTable (table class)
- QueryBuilder
- Transaction components
- AI components

## Development

When adding new features:
1. Place core DB features in `core/`
2. Place AI features in `ai/`
3. Place UI features in `gui/`
4. Expose public APIs in `__init__.py`
5. Add type hints in `../smartkdb.pyi`

---

For full architecture details, see `../docs/ARCHITECTURE.md`
