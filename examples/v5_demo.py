from smartkdb import SmartKDB
import time

def main():
    print("🚀 Initializing SmartKDB v5...")
    db = SmartKDB("v5_demo.kdb")
    
    # 1. Create Table
    print("\n📦 Creating Table 'products'...")
    products = db.create_table("products", pk="sku", indexes=["category"])
    
    # 2. Transactional Insert
    print("\n🔄 Starting Transaction...")
    tx = db.tx_manager.begin()
    try:
        products.insert({"sku": "LPT-001", "name": "Laptop", "category": "Electronics", "price": 1200}, transaction_id=tx)
        products.insert({"sku": "PHN-002", "name": "Phone", "category": "Electronics", "price": 800}, transaction_id=tx)
        db.tx_manager.commit(tx)
        print("✅ Transaction Committed.")
    except Exception as e:
        db.tx_manager.rollback(tx)
        print(f"❌ Transaction Failed: {e}")

    # 3. Query
    print("\n🔎 Querying Electronics > $1000...")
    results = products.query().where("category", "==", "Electronics").where("price", ">", 1000).execute()
    for r in results:
        print(f"   - {r['name']} (${r['price']})")

    # 4. Update & Time Travel
    print("\n⏱️ Updating Price & Checking History...")
    products.update("LPT-001", {"price": 1100})
    
    history = db.version_manager.get_history("products", "LPT-001")
    print(f"   - History records found: {len(history)}")
    
    # 5. AI Brain
    print("\n🧠 Brain Stats:")
    print(db.brain.stats)

    print("\n✨ Demo Complete!")

if __name__ == "__main__":
    main()
