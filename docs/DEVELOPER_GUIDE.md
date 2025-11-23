# SmartKDB v5 Developer Guide 🛠️

## 1. ACID Transactions
SmartKDB v5 supports atomic transactions.

```python
tx = db.tx_manager.begin()
try:
    db.get_table("users").insert(data, transaction_id=tx)
    db.get_table("logs").insert(log_entry, transaction_id=tx)
    db.tx_manager.commit(tx)
except Exception as e:
    db.tx_manager.rollback(tx)
    print("Transaction failed:", e)
```

## 2. Time-Travel Queries
Access historical data using the Version Manager.

```python
# Get record state at a specific timestamp
past_data = db.version_manager.get_version_at("users", "user_123", timestamp=1678886400)
```

## 3. Plugin Development
Create a python file in `smartkdb/plugins/my_plugin.py`.

```python
def register(db):
    # This function is called on startup
    print("Plugin initialized")
    
    # You can monkey-patch or extend DB functionality
    db.my_custom_method = lambda: "Hello from Plugin"
```

## 4. Distributed Mode
Join a cluster:

```python
db.node_manager.join_cluster("http://192.168.1.50:8000")
```
