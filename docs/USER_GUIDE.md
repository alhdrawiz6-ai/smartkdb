# SmartKDB User Guide 📘

**For Beginners - Learn SmartKDB in 30 Minutes**

---

## Table of Contents
1. [Installation](#installation)
2. [Your First Database](#your-first-database)
3. [CRUD Operations](#crud-operations)
4. [Querying Data](#querying-data)
5. [Advanced Features](#advanced-features)
6. [Common Patterns](#common-patterns)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher:
```bash
python --version
```

### Step 2: Install SmartKDB
```bash
pip install smartkdb
```

### Step 3: Verify Installation
```python
from smartkdb import SmartKDB
print("✅ SmartKDB installed successfully!")
```

---

## Your First Database

### Create a Database
```python
from smartkdb import SmartKDB

# This creates a folder called "mydb.kdb" in your current directory
db = SmartKDB("mydb.kdb")
```

**What just happened?**
- ✅ A database folder was created
- ✅ SmartKDB is ready to use
- ✅ No servers, no configuration needed!

### Create Your First Table
```python
# Create a table to store users
users = db.create_table("users")
```

**Table Options:**
```python
# With custom primary key
users = db.create_table("users", pk="email")

# With indexes for faster queries
users = db.create_table("users", indexes=["age", "city"])
```

---

## CRUD Operations

### Create (Insert)
```python
# Insert a user
user = users.insert({
    "name": "Ali",
    "age": 25,
    "email": "ali@example.com",
    "city": "Baghdad"
})

print(user)  # Shows the inserted data with auto-generated ID
```

**Tips:**
- If you don't provide an ID, SmartKDB generates one automatically
- Returns the complete inserted document

### Read (Get)
```python
# Get by ID
user = users.get("user_id_here")

if user:
    print(f"Name: {user['name']}")
else:
    print("User not found")
```

### Update
```python
# Update specific fields
updated = users.update("user_id", {
    "age": 26,
    "city": "Dubai"
})

print(updated)  # Shows the new data
```

**Note:** Update merges with existing data. Fields you don't mention stay unchanged.

### Delete
```python
# Delete a user
users.delete("user_id")
```

---

## Querying Data

### Basic Query
```python
# Get all users
all_users = users.query().execute()
```

### Filter by Condition
```python
# Users older than 20
results = users.query().where("age", ">", 20).execute()

# Users from Baghdad
results = users.query().where("city", "==", "Baghdad").execute()
```

**Supported Operators:**
- `==` - Equal
- `!=` - Not equal
- `>` - Greater than
- `<` - Less than
- `>=` - Greater or equal
- `<=` - Less or equal

### Multiple Conditions
```python
# Young developers from Baghdad
results = users.query()\
    .where("age", "<", 30)\
    .where("city", "==", "Baghdad")\
    .execute()
```

---

## Advanced Features

### 1. Transactions (ACID)
```python
# Start a transaction
tx = db.tx_manager.begin()

try:
    # Do multiple operations
    users.insert({"name": "Sara"}, transaction_id=tx)
    users.insert({"name": "Ahmed"}, transaction_id=tx)
    
    # Commit all changes
    db.tx_manager.commit(tx)
    print("✅ All changes saved")
    
except Exception as e:
    # Rollback if anything fails
    db.tx_manager.rollback(tx)
    print(f"❌ Changes cancelled: {e}")
```

### 2. Time-Travel (Version History)
```python
# Get history of a record
history = db.version_manager.get_history("users", "user_id")

for version in history:
    print(f"Changed at: {version['timestamp']}")
    print(f"Data: {version['data']}")
```

### 3. AI Brain
```python
# See what the database learned
print(db.brain.stats)

# Get optimization suggestions
suggestions = db.brain.suggest_indexes("users")
print(suggestions)
```

---

## Common Patterns

### Pattern 1: E-Commerce Products
```python
db = SmartKDB("shop.kdb")
products = db.create_table("products", indexes=["category", "price"])

# Add products
products.insert({
    "name": "Laptop",
    "price": 999,
    "category": "Electronics",
    "stock": 10
})

# Find cheap electronics
cheap = products.query()\
    .where("category", "==", "Electronics")\
    .where("price", "<", 500)\
    .execute()
```

### Pattern 2: Blog Posts
```python
posts = db.create_table("posts", pk="slug", indexes=["author"])

# Create post
posts.insert({
    "slug": "my-first-post",
    "title": "Hello World",
    "author": "Ali",
    "content": "This is my first post!"
})

# Get all posts by Ali
ali_posts = posts.query().where("author", "==", "Ali").execute()
```

### Pattern 3: User Sessions
```python
sessions = db.create_table("sessions")

# Create session
session = sessions.insert({
    "user_id": "user_123",
    "ip": "192.168.1.1",
    "created_at": "2024-01-01"
})

# Update session
sessions.update(session["id"], {
    "last_seen": "2024-01-02"
})
```

---

## Troubleshooting

### Problem: "Table not found"
```python
# Solution: Create the table first
users = db.create_table("users")
```

### Problem: "Duplicate Key"
```python
# Solution: Check if record exists first
existing = users.get("user_id")
if existing:
    users.update("user_id", {"name": "New Name"})
else:
    users.insert({"id": "user_id", "name": "New Name"})
```

### Problem: "Record not found"
```python
# Solution: Always check if get() returns None
user = users.get("user_id")
if user is None:
    print("User doesn't exist")
```

---

## Next Steps

✅ **You now know the basics!**

**Where to go next:**
1. 📖 [Developer Guide](DEVELOPER_GUIDE.md) - Advanced patterns
2. 🏗️ [Architecture](ARCHITECTURE.md) - How it works
3. 🔌 [API Reference](API_REFERENCE.md) - Complete API
4. 💡 Run `examples/quickstart.py` for interactive tutorial

---

**Need Help?**
- Check the [Quick Reference](../QUICK_REFERENCE.md)
- See more examples in `/examples` folder
- Read the [FAQ](API_REFERENCE.md#faq)

**Happy coding! 🚀**
