# SmartKDB v5 - Quick Reference Card

## 📦 Installation
```bash
pip install smartkdb
```

## 🚀 Quick Start
```python
from smartkdb import SmartKDB

db = SmartKDB("mydb.kdb")
users = db.create_table("users")
users.insert({"name": "Alice", "age": 25})
```

## 📚 Essential Operations

### Create
```python
users.insert({"name": "Bob", "email": "bob@example.com"})
```

### Read
```python
user = users.get("user_id")
```

### Update
```python
users.update("user_id", {"age": 26})
```

### Delete
```python
users.delete("user_id")
```

### Query
```python
results = users.query().where("age", ">", 21).execute()
```

## 🔒 Transactions
```python
tx = db.tx_manager.begin()
try:
    users.insert({"name": "Charlie"}, transaction_id=tx)
    db.tx_manager.commit(tx)
except:
    db.tx_manager.rollback(tx)
```

## 🧠 AI Features
```python
# Brain statistics
db.brain.stats

# Get suggestions
db.brain.suggest_indexes("users")

# Time-travel
history = db.version_manager.get_history("users", "user_id")
```

## 📖 Full Documentation
- 📘 [User Guide](docs/USER_GUIDE.md)
- 🛠️ [Developer Guide](docs/DEVELOPER_GUIDE.md)
- 🏗️ [Architecture](docs/ARCHITECTURE.md)

---
**Need help?** See [examples/](examples/) folder for complete demos!
