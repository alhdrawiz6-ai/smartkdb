# SmartKDB Project Structure

This document explains the organization of the SmartKDB v5 codebase.

---

## 📁 Root Directory

```
smartkdb/
├── smartkdb/              # Main package (the library code)
├── docs/                  # Documentation
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── README.md              # Main documentation
├── LICENSE                # MIT License
├── pyproject.toml         # Package configuration
├── pyrightconfig.json     # Type checking config
├── smartkdb.pyi           # Type stubs for IDEs
├── QUICK_REFERENCE.md     # Quick API reference
└── .gitignore             # Git ignore rules
```

---

## 📦 smartkdb/ (Main Package)

```
smartkdb/
├── __init__.py            # Package exports
├── core/                  # Core database engine
│   ├── engine.py          # SmartKDB, KTable, QueryBuilder
│   ├── storage.py         # BlockStorage (append-only)
│   ├── index.py           # Primary & secondary indexes
│   ├── transaction.py     # ACID transaction manager
│   ├── versioning.py      # Time-travel & history
│   └── distributed.py     # Clustering & sync
│
├── ai/                    # AI & Intelligence layer
│   ├── brain.py           # Query learning & optimization
│   ├── trainer.py         # Dataset quality tools
│   └── llm_connectors.py  # LLM integration
│
├── gui/                   # Web dashboard
│   ├── backend.py         # FastAPI server
│   └── frontend/          # HTML/JS interface
│       └── index.html
│
└── plugins/               # Plugin system
    └── manager.py         # Plugin loader
```

---

## 📚 docs/

```
docs/
├── USER_GUIDE.md          # Beginner tutorial
├── DEVELOPER_GUIDE.md     # Advanced API guide
├── ARCHITECTURE.md        # Technical internals
├── API_REFERENCE.md       # Complete API docs
├── INSTALLATION.md        # Install instructions
├── PUBLISHING_GUIDE.md    # How to publish to PyPI
├── CHANGELOG.md           # Version history
├── SECURITY.md            # Security policy
├── CONTRIBUTING.md        # Contribution guide
└── INTELLISENSE_UPGRADE.md # IDE setup
```

---

## 💡 examples/

```
examples/
├── quickstart.py          # 5-minute interactive tutorial
├── transactions.py        # ACID transactions demo
├── ai_features.py         # AI Brain & time-travel
├── intellisense_test.py   # Test IDE autocomplete
└── v5_demo.py             # Complete feature showcase
```

---

## 🧪 tests/

```
tests/
└── test_core.py           # Core functionality tests
```

**To run tests:**
```bash
python -m pytest tests/
```

---

## 🔧 Configuration Files

### pyproject.toml
Package metadata and dependencies:
```toml
[project]
name = "smartkdb"
version = "5.0.0"
dependencies = ["fastapi", "uvicorn", ...]
```

### pyrightconfig.json
IDE type checking settings:
```json
{
  "typeCheckingMode": "basic",
  "pythonVersion": "3.8"
}
```

### smartkdb.pyi
Type stubs for IntelliSense - helps IDEs understand the API.

---

## 🗂️ Data Storage Structure

When you create a database, SmartKDB creates this structure:

```
mydb.kdb/
├── tables/
│   ├── users/
│   │   ├── data.bin       # Actual records
│   │   ├── pk.idx         # Primary key index
│   │   └── email.idx      # Secondary indexes
│   └── products/
│       └── ...
├── history/               # Version history
│   └── users_user123.json
├── kdb_brain.json        # AI Brain stats
└── meta.json             # Database metadata
```

---

## 🎯 Key Design Principles

1. **Modularity**: Each component is independent
2. **Extensibility**: Plugin system for custom features
3. **Type Safety**: Full type hints for IDE support
4. **Documentation**: Every public API is documented
5. **Simplicity**: Easy to understand, easy to use

---

## 🔄 Data Flow

### Write Operation
```
User Code
  ↓
SmartKDB.create_table()
  ↓
KTable.__init__()
  ↓
Storage + Indexes initialized
```

### Insert Operation
```
table.insert(data)
  ↓
Transaction logging (if tx_id provided)
  ↓
BlockStorage.write_record()
  ↓
Update indexes
  ↓
VersionManager.archive_record()
  ↓
NodeManager.broadcast_update() (if clustered)
```

### Query Operation
```
table.query().where(...).execute()
  ↓
QueryBuilder collects filters
  ↓
Iterate over index
  ↓
Filter results
  ↓
Return matches
```

---

## 📝 Adding New Features

### 1. Core Feature
Add to `smartkdb/core/`

### 2. AI Feature
Add to `smartkdb/ai/`

### 3. Plugin
Add to `smartkdb/plugins/`

### 4. Documentation
Update relevant files in `docs/`

### 5. Example
Add demo to `examples/`

### 6. Tests
Add tests to `tests/`

---

**Questions?** See [CONTRIBUTING.md](CONTRIBUTING.md)
