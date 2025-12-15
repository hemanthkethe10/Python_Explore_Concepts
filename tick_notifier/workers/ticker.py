"""Ticker process that checks cron schedules and enqueues jobs."""

import time
import threading
import logging
from datetime import datetime
from typing import Optional

from croniter import croniter
import pytz

from ..queues.base import BaseQueue, NotificationJob
from ..db.repository import NotificationRepository
from ..db.models import NotificationRecord

logger = logging.getLogger(__name__)


class Ticker:
    """
    Ticker process that runs periodically to check cron schedules.
    
    The ticker:
    1. Runs every minute (configurable)
    2. Queries all active notification records
    3. Checks if each record's cron expression matches current time
    4. Enqueues matching records as jobs
    5. Marks records as triggered to prevent duplicates
    
    This is the "scheduler" component - it only decides WHEN to send,
    not HOW to send. Workers handle the actual sending.
    """
    
    def __init__(
        self,
        queue: BaseQueue,
        repository: NotificationRepository,
        interval_seconds: int = 60
    ):
        """
        Initialize the ticker.
        
        Args:
            queue: Queue to push notification jobs to
            repository: Repository for accessing notification records
            interval_seconds: How often to check schedules (default: 60s)
        """
        self._queue = queue
        self._repository = repository
        self._interval = interval_seconds
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
    
    def tick(self) -> int:
        """
        Perform a single tick - check all records and enqueue due notifications.
        
        Returns:
            Number of jobs enqueued
        """
        now = datetime.utcnow()
        enqueued = 0
        
        logger.debug(f"Tick at {now.isoformat()}")
        
        # Get all active records
        records = self._repository.get_active_records()
        logger.debug(f"Checking {len(records)} active records")
        
        for record in records:
            if self._should_trigger(record, now):
                job = self._create_job(record, now)
                self._queue.push(job)
                self._repository.mark_triggered(record.id)
                
                logger.info(
                    f"Enqueued notification job for '{record.name}' "
                    f"(id={record.id}, cron={record.cron_expression})"
                )
                enqueued += 1
        
        if enqueued > 0:
            logger.info(f"Tick complete: {enqueued} jobs enqueued")
        
        return enqueued
    
    def _should_trigger(self, record: NotificationRecord, now: datetime) -> bool:
        """
        Check if a record should be triggered at the given time.
        
        Args:
            record: The notification record to check
            now: Current time (UTC)
        
        Returns:
            True if the record should be triggered
        """
        try:
            # Convert to record's timezone
            tz = pytz.timezone(record.timezone)
            local_now = now.replace(tzinfo=pytz.UTC).astimezone(tz)
            
            # Get the previous scheduled time
            cron = croniter(record.cron_expression, local_now)
            prev_run = cron.get_prev(datetime)
            
            # Check if we're within the current minute window
            same_minute = (
                prev_run.year == local_now.year and
                prev_run.month == local_now.month and
                prev_run.day == local_now.day and
                prev_run.hour == local_now.hour and
                prev_run.minute == local_now.minute
            )
            
            if not same_minute:
                return False
            
            # Check if we already triggered this minute
            if record.last_triggered_at:
                last_triggered_local = record.last_triggered_at
                if last_triggered_local.tzinfo is None:
                    last_triggered_local = last_triggered_local.replace(tzinfo=pytz.UTC)
                last_triggered_local = last_triggered_local.astimezone(tz)
                
                already_triggered = (
                    last_triggered_local.year == local_now.year and
                    last_triggered_local.month == local_now.month and
                    last_triggered_local.day == local_now.day and
                    last_triggered_local.hour == local_now.hour and
                    last_triggered_local.minute == local_now.minute
                )
                
                if already_triggered:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking trigger for record {record.id}: {e}")
            return False
    
    def _create_job(self, record: NotificationRecord, scheduled_time: datetime) -> NotificationJob:
        """Create a notification job from a record."""
        return NotificationJob(
            record_id=record.id,
            scheduled_time=scheduled_time,
            notification_config=record.get_notification_config()
        )
    
    def start(self, blocking: bool = False) -> None:
        """
        Start the ticker.
        
        Args:
            blocking: If True, run in current thread (blocks). 
                     If False, run in background thread.
        """
        if self._running:
            logger.warning("Ticker is already running")
            return
        
        self._running = True
        self._stop_event.clear()
        
        logger.info(f"Starting ticker (interval={self._interval}s, blocking={blocking})")
        
        if blocking:
            self._run_loop()
        else:
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
    
    def stop(self, timeout: float = 5.0) -> None:
        """
        Stop the ticker gracefully.
        
        Args:
            timeout: How long to wait for the ticker to stop
        """
        if not self._running:
            return
        
        logger.info("Stopping ticker...")
        self._running = False
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)
            if self._thread.is_alive():
                logger.warning("Ticker did not stop within timeout")
        
        logger.info("Ticker stopped")
    
    def _run_loop(self) -> None:
        """Main ticker loop."""
        logger.info("Ticker loop started")
        
        # Perform initial tick immediately
        try:
            self.tick()
        except Exception as e:
            logger.error(f"Error in initial tick: {e}")
        
        while self._running and not self._stop_event.is_set():
            # Wait for next interval
            self._stop_event.wait(timeout=self._interval)
            
            if not self._running:
                break
            
            try:
                self.tick()
            except Exception as e:
                logger.error(f"Error in tick: {e}")
        
        logger.info("Ticker loop ended")
    
    @property
    def is_running(self) -> bool:
        """Check if ticker is running."""
        return self._running

