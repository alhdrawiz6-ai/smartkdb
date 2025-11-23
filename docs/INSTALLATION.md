# SmartKDB v5 Installation Guide

## Quick Install

```bash
pip install smartkdb
```

That's it! SmartKDB has **zero dependencies** and works on all platforms.

---

## Detailed Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Verify Python Version
```bash
python --version
# Should show: Python 3.8.x or higher
```

### Install from PyPI
```bash
pip install smartkdb

# Or upgrade existing installation
pip install --upgrade smartkdb
```

### Install from Source (for developers)
```bash
git clone https://github.com/alhdrawi/smartkdb
cd smartkdb
pip install -e .
```

---

## Verify Installation

Run this to confirm everything works:

```python
from smartkdb import SmartKDB

db = SmartKDB("test.kdb")
users = db.create_table("users")
users.insert({"name": "Test User"})

print("✅ SmartKDB is working!")
```

---

## Platform-Specific Notes

### Windows
```powershell
pip install smartkdb
```

### macOS / Linux
```bash
pip3 install smartkdb
```

### Virtual Environments (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install
pip install smartkdb
```

---

## IDE Setup

### VS Code
1. Install Python extension
2. Open project folder
3. SmartKDB will provide **full IntelliSense** automatically!

### PyCharm
1. Create new Python project
2. `pip install smartkdb`
3. Autocomplete works out of the box!

---

## Troubleshooting

### Issue: "Command not found: pip"
**Solution:** Install pip:
```bash
python -m ensurepip --upgrade
```

### Issue: "Permission denied"
**Solution:** Use `--user` flag:
```bash
pip install --user smartkdb
```

### Issue: "Module not found"
**Solution:** Make sure you're using the right Python:
```bash
python -m pip install smartkdb
```

---

## Next Steps

✅ **Installation complete!**

Now try:
1. Run `python examples/quickstart.py`
2. Read the [User Guide](USER_GUIDE.md)
3. Explore the [examples/](../examples/) folder

**Happy coding! 🚀**
