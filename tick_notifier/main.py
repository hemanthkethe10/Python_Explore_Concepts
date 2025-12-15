"""
Main entry point for the tick-based notification system.

This module provides a NotificationSystem class that orchestrates
the ticker and workers together for easy management.
"""

import signal
import logging
import time
from typing import Optional

from .config import Config, config as default_config
from .queues.memory_queue import InMemoryQueue
from .queues.base import BaseQueue
from .db.repository import NotificationRepository
from .db.models import NotificationRecord, NotificationType
from .services.notifier import NotificationService, ConsoleNotifier
from .workers.ticker import Ticker
from .workers.notification_worker import NotificationWorker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


class NotificationSystem:
    """
    Main orchestrator for the notification system.
    
    Manages the lifecycle of:
    - Queue
    - Repository
    - Ticker
    - Workers
    
    Usage:
        system = NotificationSystem()
        system.start()
        # ... system runs ...
        system.stop()
    """
    
    def __init__(
        self,
        config: Optional[Config] = None,
        queue: Optional[BaseQueue] = None,
        repository: Optional[NotificationRepository] = None,
        notifier: Optional[NotificationService] = None
    ):
        """
        Initialize the notification system.
        
        All dependencies are optional and will use defaults if not provided.
        This makes it easy to swap implementations.
        
        Args:
            config: Configuration settings
            queue: Queue implementation (default: InMemoryQueue)
            repository: Repository implementation (default: in-memory)
            notifier: Notification service (default: ConsoleNotifier)
        """
        self._config = config or default_config
        
        # Initialize components with dependency injection
        self._queue = queue or InMemoryQueue()
        self._repository = repository or NotificationRepository()
        self._notifier = notifier or ConsoleNotifier()
        
        # Create ticker and workers
        self._ticker = Ticker(
            queue=self._queue,
            repository=self._repository,
            interval_seconds=self._config.tick_interval_seconds
        )
        
        self._worker = NotificationWorker(
            queue=self._queue,
            repository=self._repository,
            notifier=self._notifier,
            worker_count=self._config.worker_count,
            max_retries=self._config.max_retries,
            retry_delay=self._config.retry_delay_seconds
        )
        
        self._running = False
    
    @property
    def repository(self) -> NotificationRepository:
        """Get the repository for managing records."""
        return self._repository
    
    @property
    def queue(self) -> BaseQueue:
        """Get the queue."""
        return self._queue
    
    def start(self, blocking: bool = True) -> None:
        """
        Start the notification system.
        
        Args:
            blocking: If True, block until interrupted. If False, run in background.
        """
        if self._running:
            logger.warning("System is already running")
            return
        
        logger.info("=" * 60)
        logger.info("Starting Tick-Based Notification System")
        logger.info("=" * 60)
        logger.info(f"Tick interval: {self._config.tick_interval_seconds}s")
        logger.info(f"Worker count: {self._config.worker_count}")
        logger.info(f"Max retries: {self._config.max_retries}")
        logger.info("=" * 60)
        
        self._running = True
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Start workers first (so they're ready to process jobs)
        self._worker.start(blocking=False)
        
        # Start ticker (this will enqueue jobs)
        self._ticker.start(blocking=blocking)
        
        if blocking:
            # Keep main thread alive
            try:
                while self._running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
    
    def stop(self) -> None:
        """Stop the notification system gracefully."""
        if not self._running:
            return
        
        logger.info("Shutting down notification system...")
        self._running = False
        
        # Stop ticker first (no new jobs)
        self._ticker.stop()
        
        # Let workers finish processing remaining jobs
        time.sleep(1)
        
        # Stop workers
        self._worker.stop()
        
        logger.info("Notification system stopped")
    
    def _signal_handler(self, signum, frame) -> None:
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}")
        self.stop()
    
    @property
    def is_running(self) -> bool:
        """Check if system is running."""
        return self._running
    
    def add_record(self, record: NotificationRecord) -> NotificationRecord:
        """Convenience method to add a notification record."""
        return self._repository.create(record)
    
    def trigger_now(self, record_id: str) -> bool:
        """
        Manually trigger a notification immediately.
        
        Useful for testing or one-off notifications.
        """
        from datetime import datetime
        from .queues.base import NotificationJob
        
        record = self._repository.get_by_id(record_id)
        if not record:
            logger.error(f"Record {record_id} not found")
            return False
        
        job = NotificationJob(
            record_id=record.id,
            scheduled_time=datetime.utcnow(),
            notification_config=record.get_notification_config()
        )
        
        self._queue.push(job)
        logger.info(f"Manually triggered notification for record {record_id}")
        return True


def create_demo_records(repository: NotificationRepository) -> None:
    """Create some demo notification records for testing."""
    
    # Record that triggers every minute (for testing)
    every_minute = NotificationRecord(
        name="Every Minute Alert",
        cron_expression="* * * * *",  # Every minute
        notification_type=NotificationType.EMAIL,
        recipients=["admin@example.com"],
        subject="Minute Check",
        message="This notification fires every minute for testing.",
        timezone="UTC"
    )
    
    # Record that triggers at 9 AM daily
    daily_report = NotificationRecord(
        name="Daily Report",
        cron_expression="0 9 * * *",  # 9 AM daily
        notification_type=NotificationType.EMAIL,
        recipients=["team@example.com", "manager@example.com"],
        subject="Daily Status Report",
        message="Your daily status report is ready for review.",
        timezone="America/New_York"
    )
    
    # Record that triggers every Monday at 10 AM
    weekly_sync = NotificationRecord(
        name="Weekly Team Sync Reminder",
        cron_expression="0 10 * * 1",  # Monday 10 AM
        notification_type=NotificationType.WEBHOOK,
        recipients=["https://slack.webhook.example.com/notify"],
        subject="Team Sync Reminder",
        message="Don't forget: Team sync meeting in 30 minutes!",
        metadata={"channel": "#engineering", "priority": "high"},
        timezone="UTC"
    )
    
    repository.create(every_minute)
    repository.create(daily_report)
    repository.create(weekly_sync)
    
    logger.info("Created demo notification records")


if __name__ == "__main__":
    # Example usage
    system = NotificationSystem()
    
    # Create some demo records
    create_demo_records(system.repository)
    
    # List all records
    print("\n📋 Registered Notification Records:")
    print("-" * 50)
    for record in system.repository.get_all():
        print(f"  [{record.id}] {record.name}")
        print(f"      Cron: {record.cron_expression} ({record.timezone})")
        print(f"      Type: {record.notification_type.value}")
        print(f"      Recipients: {record.recipients}")
        print()
    
    print("Starting notification system (Ctrl+C to stop)...")
    print("=" * 50)
    
    # Start the system (blocking)
    system.start(blocking=True)

