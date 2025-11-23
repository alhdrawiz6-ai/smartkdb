"""
SmartKDB AI Features Example
=============================

This example demonstrates the AI-powered features of SmartKDB v5.

Features covered:
- AI Brain (query optimization)
- Time-Travel queries
- Version history
"""

from smartkdb import SmartKDB
import time

print("🧠 SmartKDB AI Features Demo\n")

# Initialize database
db = SmartKDB("ai_demo.kdb")
products = db.create_table("products", pk="sku", indexes=["category"])

# ============================================================================
# Feature 1: Basic Operations (Brain learns from these)
# ============================================================================
print("📦 Adding products...")
products.insert({"sku": "P001", "name": "Laptop", "price": 1200, "category": "Electronics"})
products.insert({"sku": "P002", "name": "Mouse", "price": 25, "category": "Electronics"})
products.insert({"sku": "P003", "name": "Desk", "price": 300, "category": "Furniture"})
print("✅ Products added\n")

# Simulate queries (Brain observes patterns)
print("🔍 Running queries (Brain is watching)...")
for _ in range(5):
    products.query().where("category", "==", "Electronics").execute()
print("✅ Brain has observed query patterns\n")

# ============================================================================
# Feature 2: AI Brain Statistics
# ============================================================================
print("🧠 AI Brain Statistics:")
print(f"Stats: {db.brain.stats}")
suggestions = db.brain.suggest_indexes("products")
if suggestions:
    print(f"Suggestions: {suggestions}")
else:
    print("No optimization suggestions yet (need more queries)")
print()

# ============================================================================
# Feature 3: Time-Travel Queries (Versioning)
# ============================================================================
print("⏰ Time-Travel Demo:")
print("Updating laptop price...")
timestamp_before = time.time()
time.sleep(0.1)

products.update("P001", {"price": 1100})
print(f"✅ Price updated to $1100")

time.sleep(0.1)
timestamp_after = time.time()

products.update("P001", {"price": 1000})
print(f"✅ Price updated to $1000\n")

# Get version history
print("📜 Version History for P001:")
history = db.version_manager.get_history("products", "P001")
print(f"Total versions: {len(history)}")
for i, version in enumerate(history):
    print(f"  Version {i+1}: Price = ${version['data'].get('price', 'N/A')}")
print()

# Travel back in time
print("🕐 Traveling back in time...")
past_version = db.version_manager.get_version_at("products", "P001", timestamp_before)
if past_version:
    print(f"✅ Product at that time: ${past_version.get('price', 'N/A')}")
else:
    print("⚠️ Version not found at that timestamp")
print()

# ============================================================================
# Feature 4: Current State
# ============================================================================
current = products.get("P001")
print(f"📊 Current price: ${current['price']}\n")

print("="*60)
print("🎉 AI Features demo complete!")
print("="*60)
print("\n🔮 Key AI Features:")
print("  • Brain learns from query patterns")
print("  • Suggests optimizations automatically")
print("  • Version history for all records")
print("  • Time-travel to any point in history")
