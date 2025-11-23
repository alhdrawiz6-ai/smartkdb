"""
IntelliSense Test Script for SmartKDB v5

This script demonstrates the autocomplete and type-aware features.
Type the code below and verify that VS Code provides suggestions.
"""

from smartkdb import SmartKDB

# Test 1: SmartKDB initialization
db = SmartKDB("test_intellisense.kdb")

# Type 'db.' and verify you see:
# - create_table
# - get_table
# - tx_manager
# - version_manager
# - node_manager
# - brain
# - auth

# Test 2: Table creation
users = db.create_table("users", pk="id", indexes=["email", "role"])

# Type 'users.' and verify you see:
# - insert
# - get
# - update
# - delete
# - query

# Test 3: Insert with type hints
doc = users.insert({
    "id": "user_001",
    "name": "Alice",
    "email": "alice@example.com",
    "role": "admin"
})

# Test 4: Query builder
results = users.query().where("role", "==", "admin").execute()

# Test 5: Transaction
tx_id = db.tx_manager.begin()
try:
    users.insert({"name": "Bob"}, transaction_id=tx_id)
    db.tx_manager.commit(tx_id)
except Exception as e:
    db.tx_manager.rollback(tx_id)
    print(f"Transaction failed: {e}")

# Test 6: Versioning
history = db.version_manager.get_history("users", "user_001")

# Test 7: AI Brain
stats = db.brain.stats
suggestions = db.brain.suggest_indexes("users")

print("✅ IntelliSense test complete!")
print(f"Inserted doc: {doc}")
print(f"Query results: {results}")
print(f"Brain stats: {stats}")
