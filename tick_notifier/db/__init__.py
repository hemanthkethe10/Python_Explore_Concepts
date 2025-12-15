"""Database layer for notification records."""

from .models import NotificationRecord
from .repository import NotificationRepository

__all__ = ["NotificationRecord", "NotificationRepository"]

