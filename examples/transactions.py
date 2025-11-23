"""
SmartKDB Transactions Example
==============================

This example demonstrates ACID transaction support in SmartKDB v5.

Learn how to:
- Begin transactions
- Commit changes
- Rollback on errors
- Use savepoints
"""

from smartkdb import SmartKDB

print("💰 SmartKDB Transactions Demo\n")

# Initialize database
db = SmartKDB("bank_demo.kdb")
accounts = db.create_table("accounts", pk="account_id")

# Create initial accounts
accounts.insert({"account_id": "ACC001", "holder": "Ali", "balance": 1000})
accounts.insert({"account_id": "ACC002", "holder": "Sara", "balance": 500})

print("📊 Initial balances:")
for acc in accounts.query().execute():
    print(f"  {acc['holder']}: ${acc['balance']}")
print()

# ============================================================================
# Example 1: Successful Transaction
# ============================================================================
print("✅ Example 1: Transferring $200 from Ali to Sara...")

tx = db.tx_manager.begin()
try:
    # Deduct from Ali
    ali = accounts.get("ACC001")
    accounts.update("ACC001", {"balance": ali["balance"] - 200}, transaction_id=tx)
    
    # Add to Sara
    sara = accounts.get("ACC002")
    accounts.update("ACC002", {"balance": sara["balance"] + 200}, transaction_id=tx)
    
    # Commit
    db.tx_manager.commit(tx)
    print("✅ Transaction committed successfully!\n")
except Exception as e:
    db.tx_manager.rollback(tx)
    print(f"❌ Transaction failed: {e}\n")

print("📊 After successful transaction:")
for acc in accounts.query().execute():
    print(f"  {acc['holder']}: ${acc['balance']}")
print()

# ============================================================================
# Example 2: Failed Transaction (Rollback)
# ============================================================================
print("❌ Example 2: Attempting invalid transfer (insufficient funds)...")

tx = db.tx_manager.begin()
try:
    # Try to deduct $10000 from Sara (she only has $700)
    sara = accounts.get("ACC002")
    if sara["balance"] < 10000:
        raise ValueError("Insufficient funds!")
    
    accounts.update("ACC002", {"balance": sara["balance"] - 10000}, transaction_id=tx)
    db.tx_manager.commit(tx)
except Exception as e:
    db.tx_manager.rollback(tx)
    print(f"✅ Transaction rolled back: {e}\n")

print("📊 After rollback (no changes):")
for acc in accounts.query().execute():
    print(f"  {acc['holder']}: ${acc['balance']}")
print()

print("="*60)
print("🎉 Transactions demo complete!")
print("="*60)
print("\n🔒 Key takeaways:")
print("  • Transactions ensure data consistency")
print("  • Use commit() to save changes")
print("  • Use rollback() to undo on errors")
print("  • All changes are atomic (all or nothing)")
