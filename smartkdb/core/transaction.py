import uuid
import time
from typing import Dict, List, Any, Optional
from enum import Enum

class TransactionState(Enum):
    ACTIVE = "ACTIVE"
    COMMITTED = "COMMITTED"
    ROLLED_BACK = "ROLLED_BACK"

class Transaction:
    def __init__(self, tx_id: str):
        self.id = tx_id
        self.state = TransactionState.ACTIVE
        self.start_time = time.time()
        self.operations: List[Dict[str, Any]] = []
        self.savepoints: Dict[str, int] = {}

    def add_operation(self, table: str, op_type: str, data: Any, original_data: Any = None):
        """
        Log an operation for potential rollback.
        :param table: Table name
        :param op_type: 'INSERT', 'UPDATE', 'DELETE'
        :param data: The data involved (new data for insert/update, old data for delete)
        :param original_data: The state before the operation (for rollback of updates)
        """
        self.operations.append({
            "table": table,
            "type": op_type,
            "data": data,
            "original_data": original_data,
            "timestamp": time.time()
        })

    def create_savepoint(self, name: str):
        self.savepoints[name] = len(self.operations)

    def rollback_to_savepoint(self, name: str):
        if name not in self.savepoints:
            raise ValueError(f"Savepoint '{name}' not found.")
        
        # Operations to undo are from the end of the list down to the savepoint index
        idx = self.savepoints[name]
        ops_to_undo = self.operations[idx:]
        self.operations = self.operations[:idx]
        return ops_to_undo

class TransactionManager:
    def __init__(self, storage_engine):
        self.storage = storage_engine
        self.active_transactions: Dict[str, Transaction] = {}

    def begin(self) -> str:
        tx_id = str(uuid.uuid4())
        self.active_transactions[tx_id] = Transaction(tx_id)
        return tx_id

    def commit(self, tx_id: str):
        if tx_id not in self.active_transactions:
            raise ValueError("Invalid Transaction ID")
        
        tx = self.active_transactions[tx_id]
        if tx.state != TransactionState.ACTIVE:
            raise ValueError("Transaction is not active")

        # In a real WAL system, we would flush to disk here.
        # For this implementation, we mark as committed and clear the log.
        tx.state = TransactionState.COMMITTED
        del self.active_transactions[tx_id]
        return True

    def rollback(self, tx_id: str):
        if tx_id not in self.active_transactions:
            raise ValueError("Invalid Transaction ID")
        
        tx = self.active_transactions[tx_id]
        if tx.state != TransactionState.ACTIVE:
            raise ValueError("Transaction is not active")

        # Undo operations in reverse order
        for op in reversed(tx.operations):
            self._undo_operation(op)

        tx.state = TransactionState.ROLLED_BACK
        del self.active_transactions[tx_id]
        return True

    def _undo_operation(self, op: Dict[str, Any]):
        table_name = op["table"]
        op_type = op["type"]
        
        # This requires the storage engine to expose internal methods
        # We will assume the storage engine is passed and has these methods
        table = self.storage.get_table(table_name)
        
        if op_type == "INSERT":
            # Undo Insert -> Delete
            # data contains the inserted record with ID
            doc_id = op["data"].get("_id") or op["data"].get("id")
            if doc_id:
                table.delete(doc_id, transaction_id=None) # Pass None to avoid recursive logging

        elif op_type == "DELETE":
            # Undo Delete -> Insert (Restore original)
            original = op["original_data"]
            if original:
                table.insert(original, transaction_id=None)

        elif op_type == "UPDATE":
            # Undo Update -> Update back to original
            doc_id = op["data"].get("_id") or op["data"].get("id")
            original = op["original_data"]
            if doc_id and original:
                table.update(doc_id, original, transaction_id=None)

    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        return self.active_transactions.get(tx_id)
