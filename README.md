# SmartKDB v5 🧠

**The Easiest Database for Python**

[![PyPI version](https://badge.fury.io/py/smartkdb.svg)](https://badge.fury.io/py/smartkdb)
[![Python](https://img.shields.io/pypi/pyversions/smartkdb.svg)](https://pypi.org/project/smartkdb/)
[![Documentation](https://readthedocs.org/projects/smartkdb/badge/?version=latest)](https://smartkdb.readthedocs.io/)

SmartKDB is a **local-first database** that's as easy as a Python dictionary, but with superpowers:
- 🚀 **No setup** - Works instantly
- 💾 **ACID Transactions** - Bank-grade safety
- 🧠 **AI-Powered** - Learns from your usage
- ⏰ **Time-Travel** - Query past data
- 📦 **Pure Python** - No dependencies

---

## 🎯 Install in 10 Seconds

```bash
pip install smartkdb
```

---

## ⚡ Use in 30 Seconds

```python
from smartkdb import SmartKDB

# Create database
db = SmartKDB("mydb.kdb")

# Create table
users = db.create_table("users")

# Add data
users.insert({"name": "Alice", "age": 25})
users.insert({"name": "Bob", "age": 30})

# Query data
results = users.query().where("age", ">", 25).execute()
print(results)  # [{'name': 'Bob', 'age': 30}]
```

**That's it!** 🎉

---

## 📚 Learn in 5 Minutes

Run our interactive tutorial:

```bash
python -c "from smartkdb import SmartKDB; help(SmartKDB)"
```

**Or check our example files:**
- [Quick Start Tutorial](https://github.com/alhdrawiz6-ai/smartkdb/blob/main/examples/quickstart.py)
- [Transactions Demo](https://github.com/alhdrawiz6-ai/smartkdb/blob/main/examples/transactions.py)
- [AI Features Demo](https://github.com/alhdrawiz6-ai/smartkdb/blob/main/examples/ai_features.py)

---

## 🚀 What Makes SmartKDB Special?

### 1. **Zero Configuration**
No servers, no config files, no complexity. Just `pip install` and code.

### 2. **ACID Transactions**
```python
tx = db.tx_manager.begin()
try:
    users.insert({"name": "Charlie"}, transaction_id=tx)
    db.tx_manager.commit(tx)
except:
    db.tx_manager.rollback(tx)
```

### 3. **AI Brain** 🧠
The database learns from your queries and suggests optimizations:
```python
db.brain.suggest_indexes("users")
# Returns: ['Create index on email for faster queries']
```

### 4. **Time-Travel Queries** ⏰
See your data as it was in the past:
```python
history = db.version_manager.get_history("users", "user_123")
# Shows all versions of the record
```

---

## 📖 Complete Documentation

| Guide | Description |
|:------|:------------|
| 📘 [User Guide](https://smartkdb.readthedocs.io/en/latest/USER_GUIDE.html) | For beginners - Step-by-step tutorials |
| 🛠️ [Developer Guide](https://smartkdb.readthedocs.io/en/latest/DEVELOPER_GUIDE.html) | For advanced users - API deep dive |
| 🏗️ [Architecture](https://smartkdb.readthedocs.io/en/latest/ARCHITECTURE.html) | How SmartKDB works internally |
| 🔌 [API Reference](https://smartkdb.readthedocs.io/en/latest/API_REFERENCE.html) | Complete method documentation |
| 📦 [Installation](https://smartkdb.readthedocs.io/en/latest/INSTALLATION.html) | Detailed installation guide |

**Full Documentation:** https://smartkdb.readthedocs.io/

---

## 💡 More Examples

### Example 1: E-Commerce Store
```python
db = SmartKDB("store.kdb")
products = db.create_table("products", indexes=["category"])

products.insert({
    "name": "Laptop",
    "price": 999,
    "category": "Electronics"
})

# Find all electronics under $1000
cheap_electronics = products.query()\
    .where("category", "==", "Electronics")\
    .where("price", "<", 1000)\
    .execute()
```

### Example 2: User Management
```python
users = db.create_table("users", pk="email", indexes=["role"])

users.insert({"email": "admin@company.com", "role": "admin"})

# Update user
users.update("admin@company.com", {"role": "superadmin"})

# Delete user
users.delete("old_user@company.com")
```

See more in our [examples folder](https://github.com/alhdrawiz6-ai/smartkdb/tree/main/examples)!

---

## 🎮 Try It Now

```bash
# Clone and run examples
git clone https://github.com/alhdrawiz6-ai/smartkdb
cd smartkdb
python examples/quickstart.py
python examples/transactions.py
python examples/ai_features.py
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](https://smartkdb.readthedocs.io/en/latest/CONTRIBUTING.html)

---

## 📄 License

MIT License - See [LICENSE](https://github.com/alhdrawiz6-ai/smartkdb/blob/main/LICENSE)

---

## 🌟 Why SmartKDB?

| Feature | SmartKDB | SQLite | MongoDB |
|:--------|:---------|:-------|:--------|
| **Easy to use** | ✅ Python dict-like | ⚠️ SQL required | ⚠️ Schema complex |
| **No setup** | ✅ | ✅ | ❌ Server needed |
| **ACID** | ✅ | ✅ | ⚠️ Partial |
| **AI Features** | ✅ Brain & Optimization | ❌ | ❌ |
| **Time-Travel** | ✅ Built-in | ❌ | ❌ |
| **Pure Python** | ✅ | ❌ C extension | ❌ Server |

**Perfect for:**
- 🎯 Prototypes & MVPs
- 📱 Desktop applications
- 🤖 AI/ML projects
- 📊 Data analysis scripts
- 🧪 Testing & experiments

---

## 🔗 Links

- **PyPI**: https://pypi.org/project/smartkdb/
- **Documentation**: https://smartkdb.readthedocs.io/
- **GitHub**: https://github.com/alhdrawiz6-ai/smartkdb
- **Issues**: https://github.com/alhdrawiz6-ai/smartkdb/issues
- **Changelog**: https://smartkdb.readthedocs.io/en/latest/CHANGELOG.html

---

**Made with ❤️ by Alhdrawi**

*Star ⭐ this repo if you find it useful!*
