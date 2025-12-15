"""Data models for notification records."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class NotificationType(str, Enum):
    """Supported notification types."""
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    PUSH = "push"


@dataclass
class NotificationRecord:
    """
    Represents a notification record with cron schedule.
    
    This is the core entity that defines when and how notifications should be sent.
    """
    
    # Core fields
    name: str
    cron_expression: str  # e.g., "0 9 * * *" for 9 AM daily
    notification_type: NotificationType
    
    # Notification configuration
    recipients: List[str] = field(default_factory=list)
    subject: Optional[str] = None
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Scheduling
    timezone: str = "UTC"
    is_active: bool = True
    
    # Tracking
    id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_triggered_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    last_error: Optional[str] = None
    trigger_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary for MongoDB storage."""
        return {
            "name": self.name,
            "cron_expression": self.cron_expression,
            "notification_type": self.notification_type.value,
            "recipients": self.recipients,
            "subject": self.subject,
            "message": self.message,
            "metadata": self.metadata,
            "timezone": self.timezone,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_triggered_at": self.last_triggered_at,
            "last_success_at": self.last_success_at,
            "last_error": self.last_error,
            "trigger_count": self.trigger_count,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NotificationRecord":
        """Create record from MongoDB document."""
        return cls(
            id=str(data.get("_id")) if data.get("_id") else None,
            name=data["name"],
            cron_expression=data["cron_expression"],
            notification_type=NotificationType(data["notification_type"]),
            recipients=data.get("recipients", []),
            subject=data.get("subject"),
            message=data.get("message", ""),
            metadata=data.get("metadata", {}),
            timezone=data.get("timezone", "UTC"),
            is_active=data.get("is_active", True),
            created_at=data.get("created_at", datetime.utcnow()),
            updated_at=data.get("updated_at", datetime.utcnow()),
            last_triggered_at=data.get("last_triggered_at"),
            last_success_at=data.get("last_success_at"),
            last_error=data.get("last_error"),
            trigger_count=data.get("trigger_count", 0),
        )
    
    def get_notification_config(self) -> Dict[str, Any]:
        """Get notification configuration for the job."""
        return {
            "type": self.notification_type.value,
            "recipients": self.recipients,
            "subject": self.subject,
            "message": self.message,
            "metadata": self.metadata,
        }

