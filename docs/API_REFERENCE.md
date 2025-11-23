# SmartKDB v5 API Reference 🔌

## Core

### `SmartKDB(path: str)`
Initializes the database.
*   `path`: Path to the database directory.

### `SmartKDB.create_table(name: str, pk: str="id", indexes: list=None) -> KTable`
Creates a new table.

### `KTable.insert(doc: dict, transaction_id: str=None) -> dict`
Inserts a record.
*   `doc`: The data to insert.
*   `transaction_id`: Optional transaction ID.

### `KTable.get(id_val: str) -> dict`
Retrieves a record by PK.

### `KTable.update(id_val: str, updates: dict, transaction_id: str=None) -> dict`
Updates a record.

### `KTable.delete(id_val: str, transaction_id: str=None)`
Deletes a record.

## Transaction Manager

### `TransactionManager.begin() -> str`
Starts a new transaction. Returns `tx_id`.

### `TransactionManager.commit(tx_id: str)`
Commits the transaction.

### `TransactionManager.rollback(tx_id: str)`
Rolls back the transaction.

## AI Layer

### `Brain.stats`
Dictionary containing query statistics.

### `Trainer.optimize_training(dataset_name: str) -> dict`
Analyzes a dataset for training suitability.
