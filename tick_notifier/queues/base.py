"""Base queue interface for notification jobs."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


@dataclass
class NotificationJob:
    """Represents a notification job to be processed."""
    
    record_id: str
    scheduled_time: datetime
    notification_config: Dict[str, Any]
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    retry_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary for serialization."""
        return {
            "job_id": self.job_id,
            "record_id": self.record_id,
            "scheduled_time": self.scheduled_time.isoformat(),
            "notification_config": self.notification_config,
            "retry_count": self.retry_count,
            "created_at": self.created_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotificationJob":
        """Create job from dictionary."""
        return cls(
            job_id=data["job_id"],
            record_id=data["record_id"],
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]),
            notification_config=data["notification_config"],
            retry_count=data.get("retry_count", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
        )


class BaseQueue(ABC):
    """Abstract base class for queue implementations."""
    
    @abstractmethod
    def push(self, job: NotificationJob) -> None:
        """Add a job to the queue."""
        pass
    
    @abstractmethod
    def pop(self, timeout: Optional[float] = None) -> Optional[NotificationJob]:
        """
        Remove and return a job from the queue.
        
        Args:
            timeout: How long to wait for a job (None = non-blocking, 0 = block forever)
        
        Returns:
            NotificationJob or None if queue is empty and timeout elapsed
        """
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Return the number of jobs in the queue."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Remove all jobs from the queue."""
        pass
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.size() == 0

