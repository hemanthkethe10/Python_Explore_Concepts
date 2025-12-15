"""In-memory queue implementation using Python's queue module."""

import queue
import threading
from typing import Optional
import logging

from .base import BaseQueue, NotificationJob

logger = logging.getLogger(__name__)


class InMemoryQueue(BaseQueue):
    """
    Thread-safe in-memory queue implementation.
    
    This implementation uses Python's built-in queue.Queue for thread-safety.
    It's suitable for single-process applications. For multi-process or
    distributed systems, replace with Redis or SQS implementation.
    
    Note: Jobs are NOT persisted - they will be lost on process restart.
    """
    
    _instance: Optional["InMemoryQueue"] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> "InMemoryQueue":
        """Singleton pattern to ensure single queue instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self) -> None:
        """Initialize the queue."""
        if self._initialized:
            return
        
        self._queue: queue.Queue[NotificationJob] = queue.Queue()
        self._initialized = True
        logger.info("InMemoryQueue initialized")
    
    def push(self, job: NotificationJob) -> None:
        """Add a job to the queue."""
        self._queue.put(job)
        logger.debug(f"Job {job.job_id} pushed to queue (size: {self.size()})")
    
    def pop(self, timeout: Optional[float] = None) -> Optional[NotificationJob]:
        """
        Remove and return a job from the queue.
        
        Args:
            timeout: Seconds to wait. None = non-blocking, raises Empty immediately.
                     0 or negative = block forever until item available.
        """
        try:
            if timeout is None:
                # Non-blocking
                return self._queue.get_nowait()
            elif timeout <= 0:
                # Block forever
                return self._queue.get(block=True)
            else:
                # Block with timeout
                return self._queue.get(block=True, timeout=timeout)
        except queue.Empty:
            return None
    
    def size(self) -> int:
        """Return the approximate number of jobs in the queue."""
        return self._queue.qsize()
    
    def clear(self) -> None:
        """Remove all jobs from the queue."""
        cleared = 0
        while True:
            try:
                self._queue.get_nowait()
                cleared += 1
            except queue.Empty:
                break
        logger.info(f"Queue cleared ({cleared} jobs removed)")
    
    def task_done(self) -> None:
        """Mark a task as complete (for join() support)."""
        self._queue.task_done()
    
    def join(self) -> None:
        """Block until all jobs have been processed."""
        self._queue.join()
    
    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        with cls._lock:
            cls._instance = None

