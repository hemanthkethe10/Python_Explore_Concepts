"""
Redis queue implementation.

Provides a Redis-backed queue for persistence and multi-process support.

Usage:
    from tick_notifier.queues.redis_queue import RedisQueue
    
    queue = RedisQueue(redis_url="redis://localhost:6379/0")
    system = NotificationSystem(queue=queue)
"""

import json
import logging
from typing import Optional

import redis

from .base import BaseQueue, NotificationJob

logger = logging.getLogger(__name__)


class RedisQueue(BaseQueue):
    """
    Redis-backed queue implementation.
    
    Features:
    - Persistent storage (survives restarts)
    - Multi-process safe
    - Supports multiple workers across machines
    - Atomic operations via Redis commands
    """
    
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379/0",
        queue_name: str = "notification_jobs"
    ):
        """
        Initialize Redis queue.
        
        Args:
            redis_url: Redis connection URL (e.g., "redis://localhost:6379/0")
            queue_name: Name of the Redis list to use as queue
        """
        self._redis = redis.from_url(redis_url, decode_responses=True)
        self._queue_name = queue_name
        
        # Test connection
        try:
            self._redis.ping()
            logger.info(f"RedisQueue connected: {queue_name} @ {redis_url}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def push(self, job: NotificationJob) -> None:
        """Add a job to the queue (FIFO - adds to the right)."""
        data = json.dumps(job.to_dict())
        self._redis.rpush(self._queue_name, data)
        logger.debug(f"Job {job.job_id} pushed to Redis queue (size: {self.size()})")
    
    def pop(self, timeout: Optional[float] = None) -> Optional[NotificationJob]:
        """
        Remove and return a job from the queue (FIFO - pops from the left).
        
        Args:
            timeout: Seconds to wait. None = non-blocking.
                     0 or negative = block forever.
                     Positive = block with timeout.
        
        Returns:
            NotificationJob or None if queue is empty/timeout elapsed
        """
        try:
            if timeout is None:
                # Non-blocking
                result = self._redis.lpop(self._queue_name)
            elif timeout <= 0:
                # Block forever
                result = self._redis.blpop(self._queue_name, timeout=0)
                result = result[1] if result else None
            else:
                # Block with timeout (Redis expects int seconds)
                result = self._redis.blpop(self._queue_name, timeout=int(max(1, timeout)))
                result = result[1] if result else None
            
            if result:
                data = json.loads(result)
                return NotificationJob.from_dict(data)
            return None
            
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error in pop: {e}")
            return None
    
    def size(self) -> int:
        """Return the number of jobs in the queue."""
        try:
            return self._redis.llen(self._queue_name)
        except redis.ConnectionError:
            return 0
    
    def clear(self) -> None:
        """Remove all jobs from the queue."""
        count = self.size()
        self._redis.delete(self._queue_name)
        logger.info(f"Redis queue cleared ({count} jobs removed)")
    
    def peek(self, count: int = 10) -> list:
        """
        Peek at jobs without removing them (for debugging).
        
        Args:
            count: Number of jobs to peek at
        
        Returns:
            List of NotificationJob objects
        """
        try:
            results = self._redis.lrange(self._queue_name, 0, count - 1)
            return [NotificationJob.from_dict(json.loads(r)) for r in results]
        except redis.ConnectionError:
            return []
