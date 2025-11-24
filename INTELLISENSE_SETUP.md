# IntelliSense Setup Instructions

## Problem
VS Code doesn't show autocomplete when typing `db.` 

## Solution

### Step 1: Install package in editable mode
```powershell
# In d:\kdb directory
pip install -e .
```

This makes Python aware of the `smartkdb` package.

### Step 2: Reload VS Code
Press `Ctrl+Shift+P` and run:
```
Python: Restart Language Server
```

### Step 3: Test
Create a test file:
```python
from smartkdb import SmartKDB

db = SmartKDB("test.kdb")
# Type: db.
# You should see: create_table, get_table, tx_manager, version_manager, brain, etc.
```

## If still not working:

### Check Python Interpreter
1. `Ctrl+Shift+P` → `Python: Select Interpreter`
2. Choose the one where you installed smartkdb

### Verify Installation
```powershell
pip show smartkdb
```
Should show location as `d:\kdb`

### Force Reinstall
```powershell
pip uninstall smartkdb -y
pip install -e .
```

---

## Expected IntelliSense Features

When you type `db.`, you should see:

**Methods:**
- `create_table(name, pk="id", indexes=None)`
- `get_table(name)`
- `login(user, password)`

**Properties:**
- `tx_manager` → TransactionManager
- `version_manager` → VersionManager
- `node_manager` → NodeManager
- `brain` → Brain (AI features)
- `auth` → AuthManager

**When you type `users.` (table object):**
- `insert(doc, transaction_id=None)`
- `get(id_val)`
- `update(id_val, updates, transaction_id=None)`
- `delete(id_val, transaction_id=None)`
- `query()` → QueryBuilder

---

## Completed! 🎉

After running `pip install -e .` and restarting the language server,
IntelliSense will work perfectly!
