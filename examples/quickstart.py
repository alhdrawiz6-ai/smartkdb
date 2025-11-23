"""
SmartKDB Quick Start - 5 Minutes Tutorial
==========================================

Run this file to see SmartKDB in action!

This example demonstrates the core features of SmartKDB v5:
- Database initialization
- Table creation
- CRUD operations
- Query building
"""

from smartkdb import SmartKDB

print("🚀 Starting SmartKDB Quick Start Tutorial...\n")

# ============================================================================
# Step 1: Create Database
# ============================================================================
print("📦 Step 1: Creating database...")
db = SmartKDB("my_first_db.kdb")
print("✅ Database created at: my_first_db.kdb\n")

# ============================================================================
# Step 2: Create Table
# ============================================================================
print("📋 Step 2: Creating 'users' table...")
users = db.create_table("users", pk="id", indexes=["email"])
print("✅ Table 'users' created with email index\n")

# ============================================================================
# Step 3: Insert Data (Create)
# ============================================================================
print("➕ Step 3: Inserting users...")
user1 = users.insert({"name": "Ali", "age": 25, "email": "ali@example.com", "role": "developer"})
user2 = users.insert({"name": "Sara", "age": 28, "email": "sara@example.com", "role": "designer"})
user3 = users.insert({"name": "Ahmed", "age": 30, "email": "ahmed@example.com", "role": "developer"})
print(f"✅ Inserted {user1['name']}, {user2['name']}, {user3['name']}\n")

# ============================================================================
# Step 4: Read Data
# ============================================================================
print("🔍 Step 4: Reading user by ID...")
user = users.get(user1["id"])
print(f"✅ Found: {user['name']} - {user['email']}\n")

# ============================================================================
# Step 5: Query Data
# ============================================================================
print("🔎 Step 5: Querying developers...")
results = users.query().where("role", "==", "developer").execute()
print(f"✅ Found {len(results)} developers:")
for r in results:
    print(f"   - {r['name']} (age {r['age']})")
print()

# ============================================================================
# Step 6: Update Data
# ============================================================================
print("✏️ Step 6: Updating Ali's age...")
updated = users.update(user1["id"], {"age": 26})
print(f"✅ Updated: {updated['name']} is now {updated['age']} years old\n")

# ============================================================================
# Step 7: Delete Data
# ============================================================================
print("🗑️ Step 7: Deleting a user...")
users.delete(user3["id"])
print(f"✅ Deleted Ahmed from the database\n")

# ============================================================================
# Final Results
# ============================================================================
print("📊 Final database state:")
all_users = users.query().execute()
print(f"Total users: {len(all_users)}")
for u in all_users:
    print(f"  • {u['name']} ({u['age']}) - {u['email']}")

print("\n" + "="*60)
print("🎉 Tutorial complete! You've mastered the basics!")
print("="*60)
print("\n📚 Next steps:")
print("  1. Try examples/transactions.py for ACID operations")
print("  2. Try examples/ai_features.py for AI capabilities")
print("  3. Read docs/USER_GUIDE.md for complete guide")
