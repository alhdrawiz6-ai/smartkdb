# IntelliSense Setup Guide

## Problem: VS Code doesn't show suggestions when typing `db.`

### Solution:

## Step 1: Install the package in editable mode

```powershell
# In d:\kdb directory
pip install -e .
```

This tells Python where to find `smartkdb` package.

## Step 2: Reload VS Code

Press `Ctrl+Shift+P` and type:
```
Python: Restart Language Server
```

Or simply restart VS Code:
```
Ctrl+Shift+P → Developer: Reload Window
```

## Step 3: Test

Create a new file `test_intellisense.py`:

```python
from smartkdb import SmartKDB

db = SmartKDB("test.kdb")
# Now type: db.
# You should see: create_table, get_table, tx_manager, etc.

users = db.create_table("users")
# Type: users.
# You should see: insert, get, update, delete, query
```

## Verification

When you type `db.` you should see:
- ✅ `create_table(...)`
- ✅ `get_table(...)`
- ✅ `tx_manager`
- ✅ `version_manager`
- ✅ `brain`
- ✅ `auth`

## Troubleshooting

### If still not working:

1. **Check Python Interpreter**
   - `Ctrl+Shift+P` → `Python: Select Interpreter`
   - Choose the one where you installed smartkdb

2. **Check Installation**
   ```powershell
   pip list | findstr smartkdb
   ```
   Should show: `smartkdb 5.0.0 d:\kdb`

3. **Verify pyrightconfig.json exists**
   File should be in `d:\kdb\pyrightconfig.json`

4. **Force Reload**
   - Close VS Code completely
   - Delete `.vscode` folder if exists
   - Reopen VS Code

## Alternative: Use virtualenv

```powershell
# Create venv
python -m venv venv

# Activate
.\venv\Scripts\Activate

# Install
pip install -e .

# Select this interpreter in VS Code
Ctrl+Shift+P → Python: Select Interpreter → .\venv\Scripts\python.exe
```

Now IntelliSense will work perfectly! 🚀
