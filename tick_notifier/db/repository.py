"""Repository for managing notification records."""

from datetime import datetime
from typing import Optional, List, Protocol
import logging

from .models import NotificationRecord

logger = logging.getLogger(__name__)


class DatabaseConnection(Protocol):
    """Protocol for database connections."""
    
    def find(self, query: dict) -> list:
        ...
    
    def find_one(self, query: dict) -> Optional[dict]:
        ...
    
    def insert_one(self, document: dict) -> str:
        ...
    
    def update_one(self, query: dict, update: dict) -> int:
        ...
    
    def delete_one(self, query: dict) -> int:
        ...


class InMemoryDatabase:
    """
    In-memory database for development/testing.
    
    Replace with MongoDB connection in production.
    """
    
    def __init__(self):
        self._records: dict[str, dict] = {}
        self._counter = 0
    
    def find(self, query: dict) -> list:
        """Find all records matching query."""
        results = []
        for record in self._records.values():
            if self._matches(record, query):
                results.append(record.copy())
        return results
    
    def find_one(self, query: dict) -> Optional[dict]:
        """Find single record matching query."""
        for record in self._records.values():
            if self._matches(record, query):
                return record.copy()
        return None
    
    def insert_one(self, document: dict) -> str:
        """Insert a new document."""
        self._counter += 1
        doc_id = str(self._counter)
        document["_id"] = doc_id
        self._records[doc_id] = document.copy()
        return doc_id
    
    def update_one(self, query: dict, update: dict) -> int:
        """Update a single document."""
        for doc_id, record in self._records.items():
            if self._matches(record, query):
                if "$set" in update:
                    record.update(update["$set"])
                if "$inc" in update:
                    for key, value in update["$inc"].items():
                        record[key] = record.get(key, 0) + value
                return 1
        return 0
    
    def delete_one(self, query: dict) -> int:
        """Delete a single document."""
        for doc_id, record in list(self._records.items()):
            if self._matches(record, query):
                del self._records[doc_id]
                return 1
        return 0
    
    def _matches(self, record: dict, query: dict) -> bool:
        """Check if record matches query."""
        for key, value in query.items():
            if key == "_id" and record.get("_id") != value:
                return False
            elif key != "_id" and record.get(key) != value:
                return False
        return True


class NotificationRepository:
    """
    Repository for CRUD operations on notification records.
    
    Uses dependency injection for the database connection,
    making it easy to swap between in-memory, MongoDB, etc.
    """
    
    def __init__(self, db: Optional[DatabaseConnection] = None):
        """
        Initialize repository.
        
        Args:
            db: Database connection. If None, uses in-memory database.
        """
        self._db = db or InMemoryDatabase()
    
    def create(self, record: NotificationRecord) -> NotificationRecord:
        """Create a new notification record."""
        data = record.to_dict()
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        
        doc_id = self._db.insert_one(data)
        record.id = doc_id
        
        logger.info(f"Created notification record: {record.id} - {record.name}")
        return record
    
    def get_by_id(self, record_id: str) -> Optional[NotificationRecord]:
        """Get a notification record by ID."""
        data = self._db.find_one({"_id": record_id})
        if data:
            return NotificationRecord.from_dict(data)
        return None
    
    def get_active_records(self) -> List[NotificationRecord]:
        """Get all active notification records."""
        results = self._db.find({"is_active": True})
        return [NotificationRecord.from_dict(data) for data in results]
    
    def get_all(self) -> List[NotificationRecord]:
        """Get all notification records."""
        results = self._db.find({})
        return [NotificationRecord.from_dict(data) for data in results]
    
    def update(self, record: NotificationRecord) -> bool:
        """Update an existing notification record."""
        if not record.id:
            raise ValueError("Cannot update record without ID")
        
        data = record.to_dict()
        data["updated_at"] = datetime.utcnow()
        
        result = self._db.update_one(
            {"_id": record.id},
            {"$set": data}
        )
        
        if result > 0:
            logger.info(f"Updated notification record: {record.id}")
            return True
        return False
    
    def mark_triggered(self, record_id: str) -> bool:
        """Mark a record as triggered (used by ticker)."""
        now = datetime.utcnow()
        result = self._db.update_one(
            {"_id": record_id},
            {
                "$set": {"last_triggered_at": now, "updated_at": now},
                "$inc": {"trigger_count": 1}
            }
        )
        return result > 0
    
    def mark_success(self, record_id: str) -> bool:
        """Mark a record's last notification as successful."""
        now = datetime.utcnow()
        result = self._db.update_one(
            {"_id": record_id},
            {
                "$set": {
                    "last_success_at": now,
                    "last_error": None,
                    "updated_at": now
                }
            }
        )
        return result > 0
    
    def mark_error(self, record_id: str, error: str) -> bool:
        """Mark a record's last notification as failed."""
        now = datetime.utcnow()
        result = self._db.update_one(
            {"_id": record_id},
            {
                "$set": {
                    "last_error": error,
                    "updated_at": now
                }
            }
        )
        return result > 0
    
    def delete(self, record_id: str) -> bool:
        """Delete a notification record."""
        result = self._db.delete_one({"_id": record_id})
        if result > 0:
            logger.info(f"Deleted notification record: {record_id}")
            return True
        return False
    
    def deactivate(self, record_id: str) -> bool:
        """Deactivate a notification record (soft delete)."""
        result = self._db.update_one(
            {"_id": record_id},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        return result > 0

