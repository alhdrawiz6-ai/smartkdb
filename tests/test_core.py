import unittest
import shutil
import os
from smartkdb import SmartKDB

class TestSmartKDBv5(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_db.kdb"
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        self.db = SmartKDB(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

    def test_basic_crud(self):
        table = self.db.create_table("users")
        table.insert({"name": "Alice", "age": 30})
        
        results = table.query().where("age", "==", 30).execute()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice")

    def test_acid_transaction_commit(self):
        table = self.db.create_table("bank")
        tx = self.db.tx_manager.begin()
        
        table.insert({"account": "A", "balance": 100}, transaction_id=tx)
        table.insert({"account": "B", "balance": 200}, transaction_id=tx)
        
        self.db.tx_manager.commit(tx)
        
        results = table.query().execute()
        self.assertEqual(len(results), 2)

    def test_acid_transaction_rollback(self):
        table = self.db.create_table("bank")
        tx = self.db.tx_manager.begin()
        
        table.insert({"account": "A", "balance": 100}, transaction_id=tx)
        self.db.tx_manager.rollback(tx)
        
        results = table.query().execute()
        self.assertEqual(len(results), 0)

    def test_versioning(self):
        table = self.db.create_table("history_test", pk="id")
        doc = table.insert({"id": "doc1", "val": 1})
        
        table.update("doc1", {"val": 2})
        
        # Check current
        current = table.get("doc1")
        self.assertEqual(current["val"], 2)
        
        # Check history (Time travel logic is time-based, so hard to test exact timestamp without mocking time, 
        # but we can check if history file exists/is populated)
        history = self.db.version_manager.get_history("history_test", "doc1")
        self.assertEqual(len(history), 2) # Insert + Update

if __name__ == '__main__':
    unittest.main()
