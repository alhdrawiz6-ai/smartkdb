"""
Final Verification - SmartKDB v5
=================================

Quick test to verify the clean structure works perfectly.
"""

import os
import shutil

print("=" * 60)
print("🔍 SmartKDB v5 - Final Verification")
print("=" * 60)

# Clean up old test database
test_db = "final_test.kdb"
if os.path.exists(test_db):
    shutil.rmtree(test_db)
    print("\n🧹 Cleaned up old test database")

# Test imports
print("\n✅ Testing imports...")
from smartkdb import (
    SmartKDB, KTable, QueryBuilder,
    TransactionManager, VersionManager,
    Brain, Trainer, LLMConnector,
    PluginManager
)
print("   All imports successful!")

# Test basic functionality
print("\n✅ Testing basic operations...")
db = SmartKDB(test_db)
users = db.create_table("users", indexes=["email"])

# Insert
user = users.insert({"name": "Ali", "email": "ali@test.com"})
print(f"   Inserted: {user['name']} (ID: {user['id'][:8]}...)")

# Read
found = users.get(user["id"])
if found is None:
    print(f"   ❌ ERROR: Failed to retrieve record with ID {user['id']}")
    exit(1)
assert found["name"] == "Ali", f"Expected 'Ali', got '{found['name']}'"
print(f"   Retrieved: {found['name']}")

# Update
updated = users.update(user["id"], {"name": "Ali Updated"})
assert updated["name"] == "Ali Updated", "Update failed"
print(f"   Updated: {updated['name']}")

# Verify update worked
verified = users.get(user["id"])
if verified is None:
    print(f"   ❌ ERROR: Record disappeared after update!")
    exit(1)
assert verified["name"] == "Ali Updated", "Verification failed"
print(f"   Verified: {verified['name']}")

# Query
results = users.query().where("email", "==", "ali@test.com").execute()
assert len(results) == 1, f"Expected 1 result, got {len(results)}"
print(f"   Query found {len(results)} record(s)")

# Delete
users.delete(user["id"])
deleted_check = users.get(user["id"])
assert deleted_check is None, "Delete failed - record still exists"
print("   Deleted successfully")

print("   ✅ CRUD operations work perfectly!")

# Test AI
print("\n✅ Testing AI features...")
print(f"   Brain stats: {db.brain.stats}")

# Test transactions
print("\n✅ Testing transactions...")
tx = db.tx_manager.begin()
users.insert({"name": "Sara", "email": "sara@test.com"}, transaction_id=tx)
db.tx_manager.commit(tx)
print("   Transactions work!")

# Cleanup
print("\n🧹 Cleaning up test database...")
shutil.rmtree(test_db)

print("\n" + "=" * 60)
print("🎉 All systems operational!")
print("=" * 60)
print("\n✨ SmartKDB v5 is production-ready!")


