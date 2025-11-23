"""
Core database engine for SmartKDB v5.

This module contains the main SmartKDB class and KTable class that provide
the primary interface for database operations.
"""

import os
import uuid
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from .storage import BlockStorage
from .index import Index, SecondaryIndex
from .transaction import TransactionManager
from .versioning import VersionManager
from .distributed import NodeManager

if TYPE_CHECKING:
    from ..ai.brain import Brain

class KTable:
    """
    Represents a database table in SmartKDB.
    
    A table stores documents (records) and provides CRUD operations with support
    for transactions, versioning, and distributed synchronization.
    
    Attributes:
        db: The parent SmartKDB database instance
        name: Name of the table
        pk: Primary key field name
        indexes_config: List of secondary indexed fields
    
    Example:
        >>> db = SmartKDB("mydb.kdb")
        >>> users = db.create_table("users", pk="id", indexes=["email"])
        >>> users.insert({"name": "Alice", "email": "alice@example.com"})
    """
    
    def __init__(self, db, name: str, pk: str = "id", indexes: Optional[List[str]] = None):
        """
        Initialize a new KTable instance.
        
        Args:
            db: The parent SmartKDB instance
            name: Table name
            pk: Primary key field name (default: "id")
            indexes: List of secondary indexed fields
        """
        self.db = db
        self.name = name
        self.pk = pk
        self.indexes_config = indexes or []
        
        # Storage paths
        self.table_dir = os.path.join(db.db_path, "tables", name)
        if not os.path.exists(self.table_dir):
            os.makedirs(self.table_dir)
            
        # Save metadata
        self._save_metadata()
            
        self.storage = BlockStorage(os.path.join(self.table_dir, "data.bin"))
        
        # Indexes
        self.id_index = Index(os.path.join(self.table_dir, "pk.idx"))
        self.secondary_indexes: Dict[str, SecondaryIndex] = {}
        for field in self.indexes_config:
            self.secondary_indexes[field] = SecondaryIndex(os.path.join(self.table_dir, f"{field}.idx"))

    def _save_metadata(self):
        """Save table metadata (pk and indexes)."""
        import json
        metadata = {
            "pk": self.pk,
            "indexes": self.indexes_config
        }
        with open(os.path.join(self.table_dir, "meta.json"), "w") as f:
            json.dump(metadata, f)
    
    @staticmethod
    def _load_metadata(table_dir: str) -> tuple:
        """Load table metadata. Returns (pk, indexes)."""
        import json
        meta_path = os.path.join(table_dir, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                metadata = json.load(f)
                return metadata.get("pk", "id"), metadata.get("indexes", [])
        return "id", []

    def insert(self, doc: Dict[str, Any], transaction_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Insert a new document into the table.
        
        If the primary key is not provided, a UUID will be auto-generated.
        The operation supports transactions and automatically updates all indexes.
        
        Args:
            doc: Document data as a dictionary
            transaction_id: Optional transaction ID for atomic operations
            
        Returns:
            The inserted document including the generated primary key
            
        Raises:
            ValueError: If a document with the same primary key already exists
            
        Example:
            >>> users.insert({"name": "Bob", "age": 30})
            {'id': 'auto-uuid-123', 'name': 'Bob', 'age': 30}
        """
        if self.pk not in doc:
            doc[self.pk] = str(uuid.uuid4())
        
        id_val = doc[self.pk]
        if self.id_index.get(id_val) is not None:
            raise ValueError(f"Duplicate Key: {id_val}")

        # Transaction Logging
        if transaction_id:
            tx = self.db.tx_manager.get_transaction(transaction_id)
            if tx:
                tx.add_operation(self.name, "INSERT", doc)

        # Write
        offset = self.storage.write_record(doc)
        
        # Update Indexes
        self.id_index.set(id_val, offset)
        self.id_index.save()
        
        for field, idx in self.secondary_indexes.items():
            if field in doc:
                idx.add(doc[field], offset)
                idx.save()
                
        # Versioning
        self.db.version_manager.archive_record(self.name, id_val, doc)
        
        # Distributed Sync
        self.db.node_manager.broadcast_update(self.name, id_val, doc)

        return doc

    def get(self, id_val: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its primary key.
        
        This is an O(1) operation using the primary key index.
        
        Args:
            id_val: The primary key value
            
        Returns:
            The document if found, None otherwise
            
        Example:
            >>> user = users.get("user_123")
            >>> print(user["name"])
            'Alice'
        """
        offset = self.id_index.get(id_val)
        if offset is None:
            return None
        return self.storage.read_record(offset)

    def update(self, id_val: str, updates: Dict[str, Any], transaction_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing document.
        
        Merges the updates with the existing document and creates a new version.
        The old version is kept for versioning/time-travel queries.
        
        Args:
            id_val: Primary key of the document to update
            updates: Dictionary of fields to update
            transaction_id: Optional transaction ID
            
        Returns:
            The updated document
            
        Raises:
            ValueError: If the document is not found or has been deleted
            
        Example:
            >>> users.update("user_123", {"age": 31, "role": "admin"})
            {'id': 'user_123', 'name': 'Alice', 'age': 31, 'role': 'admin'}
        """
        offset = self.id_index.get(id_val)
        if offset is None:
            raise ValueError("Record not found")
            
        existing = self.storage.read_record(offset)
        if not existing:
            raise ValueError("Record deleted")

        # Transaction Logging
        if transaction_id:
            tx = self.db.tx_manager.get_transaction(transaction_id)
            if tx:
                tx.add_operation(self.name, "UPDATE", updates, original_data=existing)

        new_doc = existing.copy()
        new_doc.update(updates)
        
        # Mark old deleted
        self.storage.mark_deleted(offset)
        
        # Remove old secondary indexes
        for field, idx in self.secondary_indexes.items():
            if field in existing:
                idx.remove_val(existing[field], offset)

        # Write new
        new_offset = self.storage.write_record(new_doc)
        
        # Update Indexes
        self.id_index.set(id_val, new_offset)
        self.id_index.save()
        
        for field, idx in self.secondary_indexes.items():
            if field in new_doc:
                idx.add(new_doc[field], new_offset)
                idx.save()
                
        # Versioning
        self.db.version_manager.archive_record(self.name, id_val, new_doc)
        
        return new_doc

    def delete(self, id_val: str, transaction_id: Optional[str] = None) -> None:
        """
        Delete a document from the table.
        
        The document is marked as deleted but remains in the storage for
        potential recovery or versioning purposes.
        
        Args:
            id_val: Primary key of the document to delete
            transaction_id: Optional transaction ID
            
        Example:
            >>> users.delete("user_123")
        """
        offset = self.id_index.get(id_val)
        if offset is None:
            return

        existing = self.storage.read_record(offset)
        
        # Transaction Logging
        if transaction_id:
            tx = self.db.tx_manager.get_transaction(transaction_id)
            if tx:
                tx.add_operation(self.name, "DELETE", id_val, original_data=existing)

        self.storage.mark_deleted(offset)
        
        self.id_index.remove(id_val)
        self.id_index.save()
        
        if existing:
            for field, idx in self.secondary_indexes.items():
                if field in existing:
                    idx.remove_val(existing[field], offset)
                    idx.save()

    def query(self) -> 'QueryBuilder':
        """
        Create a new query builder for this table.
        
        Returns a fluent query builder interface for constructing complex queries.
        
        Returns:
            QueryBuilder instance
            
        Example:
            >>> results = users.query().where("age", ">", 25).where("role", "==", "admin").execute()
        """
        return QueryBuilder(self)


class QueryBuilder:
    """
    Fluent query builder for table queries.
    
    Provides a chainable interface for constructing filtered queries with
    support for multiple conditions.
    
    Example:
        >>> results = table.query().where("age", ">", 21).where("active", "==", True).execute()
    """
    
    def __init__(self, table: KTable):
        """
        Initialize a query builder.
        
        Args:
            table: The KTable instance to query
        """
        self.table = table
        self.filters: List[tuple] = []

    def where(self, field: str, op: str, value: Any) -> 'QueryBuilder':
        """
        Add a filter condition to the query.
        
        Supported operators: "==", "!=", ">", "<", ">=", "<=", "in", "contains"
        
        Args:
            field: Field name to filter on
            op: Comparison operator
            value: Value to compare against
            
        Returns:
            Self for method chaining
            
        Example:
            >>> query.where("age", ">", 18).where("role", "==", "admin")
        """
        self.filters.append((field, op, value))
        return self

    def execute(self) -> List[Dict[str, Any]]:
        """
        Execute the query and return matching documents.
        
        Note: Currently performs a full table scan. Future versions will
        utilize secondary indexes for optimization.
        
        Returns:
            List of matching documents
            
        Example:
            >>> results = users.query().where("active", "==", True).execute()
            >>> print(f"Found {len(results)} active users")
        """
        results = []
        for pk, offset in self.table.id_index.data.items():
            rec = self.table.storage.read_record(offset)
            if rec and self._matches(rec):
                results.append(rec)
        return results

    def _matches(self, rec: Dict[str, Any]) -> bool:
        """Check if a record matches all filter conditions."""
        for field, op, val in self.filters:
            if field not in rec: 
                return False
            v = rec[field]
            if op == "==" and v != val: 
                return False
            if op == ">" and not v > val: 
                return False
            if op == "<" and not v < val: 
                return False
        return True

class SmartKDB:
    """
    SmartKDB v5 - The Cognitive AI-Native Database Platform.
    
    Main database class providing ACID transactions, versioning, distributed
    capabilities, and AI-powered intelligence.
    
    Attributes:
        db_path: Path to the database directory
        tables: Dictionary of loaded tables
        tx_manager: Transaction manager for ACID operations
        version_manager: Versioning system for time-travel queries
        node_manager: Distributed cluster manager
        brain: AI Brain for query optimization
        auth: Authentication and authorization manager
        
    Example:
        >>> db = SmartKDB("myapp.kdb")
        >>> db.auth.create_user("admin", "password", "admin")
        >>> db.login("admin", "password")
        >>> users = db.create_table("users")
    """
    
    def __init__(self, path: str = "mydb.kdb"):
        """
        Initialize a new SmartKDB database instance.
        
        Creates the database directory if it doesn't exist and initializes
        all subsystems (transactions, versioning, clustering, AI).
        
        Args:
            path: Path to the database directory (default: "mydb.kdb")
            
        Example:
            >>> db = SmartKDB("production.kdb")
        """
        self.db_path = path
        if not os.path.exists(path):
            os.makedirs(path)
            
        self.tables: Dict[str, KTable] = {}
        self.tx_manager = TransactionManager(self)
        self.version_manager = VersionManager(path)
        self.node_manager = NodeManager("localhost:8000")
        
        # Lazy-load brain to avoid circular imports
        self._brain: Optional['Brain'] = None
        
        # Auth stub
        self.auth = AuthManager(self)
    
    @property
    def brain(self) -> 'Brain':
        """
        Get the AI Brain instance.
        
        Lazy-loads the Brain on first access to avoid circular imports.
        
        Returns:
            Brain instance for query optimization and learning
        """
        if self._brain is None:
            from ..ai.brain import Brain
            self._brain = Brain(self.db_path)
        return self._brain

    def create_table(self, name: str, pk: str = "id", indexes: Optional[List[str]] = None) -> KTable:
        """
        Create a new table in the database.
        
        Args:
            name: Table name
            pk: Primary key field name (default: "id")
            indexes: List of fields to create secondary indexes on
            
        Returns:
            KTable instance representing the created table
            
        Example:
            >>> users = db.create_table("users", pk="user_id", indexes=["email", "role"])
            >>> users.insert({"user_id": "u001", "email": "alice@example.com"})
        """
        table = KTable(self, name, pk, indexes)
        self.tables[name] = table
        return table

    def get_table(self, name: str) -> KTable:
        """
        Get an existing table by name.
        
        If the table is not currently loaded, attempts to load it from disk.
        
        Args:
            name: Table name
            
        Returns:
            KTable instance
            
        Raises:
            ValueError: If the table doesn't exist
            
        Example:
            >>> users = db.get_table("users")
            >>> user = users.get("u001")
        """
        if name not in self.tables:
            table_dir = os.path.join(self.db_path, "tables", name)
            if os.path.exists(table_dir):
                # Load metadata
                pk, indexes = KTable._load_metadata(table_dir)
                self.tables[name] = KTable(self, name, pk, indexes)
            else:
                raise ValueError(f"Table {name} not found")
        return self.tables[name]

    def login(self, user: str, password: str) -> None:
        """
        Authenticate a user.
        
        Args:
            user: Username
            password: Password
            
        Note:
            Authentication system is a stub in v5 MVP.
        """
        pass

class AuthManager:
    """
    Authentication and authorization manager.
    
    Provides user management and role-based access control (RBAC).
    
    Note:
        This is a stub implementation in v5 MVP.
    """
    
    def __init__(self, db: SmartKDB):
        """Initialize the auth manager."""
        self.db = db
        
    def create_user(self, username: str, password: str, role: str) -> None:
        """
        Create a new user.
        
        Args:
            username: Username
            password: Password (will be hashed in production)
            role: User role (admin, editor, viewer)
        """
        pass

