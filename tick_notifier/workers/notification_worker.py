"""Worker that processes notification jobs from the queue."""

import threading
import logging
import time
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor

from ..queues.base import BaseQueue, NotificationJob
from ..db.repository import NotificationRepository
from ..db.models import NotificationType
from ..services.notifier import NotificationService

logger = logging.getLogger(__name__)


class NotificationWorker:
    """
    Worker that consumes jobs from the queue and sends notifications.
    
    Features:
    - Multiple worker threads for concurrent processing
    - Automatic retry with exponential backoff
    - Updates record status on success/failure
    - Graceful shutdown
    """
    
    def __init__(
        self,
        queue: BaseQueue,
        repository: NotificationRepository,
        notifier: NotificationService,
        worker_count: int = 3,
        max_retries: int = 3,
        retry_delay: float = 5.0
    ):
        """
        Initialize the worker.
        
        Args:
            queue: Queue to consume jobs from
            repository: Repository for updating record status
            notifier: Service for sending notifications
            worker_count: Number of worker threads
            max_retries: Maximum retry attempts for failed jobs
            retry_delay: Base delay between retries (exponential backoff)
        """
        self._queue = queue
        self._repository = repository
        self._notifier = notifier
        self._worker_count = worker_count
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        
        self._running = False
        # This creates an event object to signal worker threads to stop gracefully.
        self._stop_event = threading.Event()
        self._executor: Optional[ThreadPoolExecutor] = None
        self._workers: List[threading.Thread] = []
    
    def process_job(self, job: NotificationJob) -> bool:
        """
        Process a single notification job.
        
        Args:
            job: The job to process
        
        Returns:
            True if job was processed successfully
        """
        config = job.notification_config
        
        try:
            notification_type = NotificationType(config["type"])
            
            success = self._notifier.send(
                notification_type=notification_type,
                recipients=config.get("recipients", []),
                subject=config.get("subject", ""),
                message=config.get("message", ""),
                metadata=config.get("metadata", {})
            )
            
            if success:
                self._repository.mark_success(job.record_id)
                logger.info(f"Job {job.job_id} completed successfully")
                return True
            else:
                raise Exception("Notifier returned False")
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Job {job.job_id} failed: {error_msg}")
            
            # Check if we should retry
            if job.retry_count < self._max_retries:
                job.retry_count += 1
                delay = self._retry_delay * (2 ** (job.retry_count - 1))  # Exponential backoff
                
                logger.info(
                    f"Retrying job {job.job_id} in {delay}s "
                    f"(attempt {job.retry_count}/{self._max_retries})"
                )
                
                # Simple delay before re-queue (in production, use delayed queue)
                time.sleep(delay)
                self._queue.push(job)
            else:
                # Max retries exceeded
                self._repository.mark_error(job.record_id, error_msg)
                logger.error(
                    f"Job {job.job_id} failed permanently after "
                    f"{self._max_retries} attempts"
                )
            
            return False
    
    def _worker_loop(self, worker_id: int) -> None:
        """Main loop for a worker thread."""
        logger.info(f"Worker {worker_id} started")
        
        # This checks if the worker should continue running.
        # It will stop if the running flag is False or the stop event is set.
        while self._running and not self._stop_event.is_set():
            try:
                # Block for up to 1 second waiting for a job
                job = self._queue.pop(timeout=1.0)
                
                if job:
                    logger.debug(f"Worker {worker_id} processing job {job.job_id}")
                    self.process_job(job)
                    
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
                time.sleep(1)  # Brief pause on error
        
        logger.info(f"Worker {worker_id} stopped")
    
    def start(self, blocking: bool = False) -> None:
        """
        Start the worker pool.
        
        Args:
            blocking: If True, block until stopped. If False, run in background.
        """
        if self._running:
            logger.warning("Workers are already running")
            return
        
        self._running = True
        self._stop_event.clear()
        self._workers = []
        
        logger.info(f"Starting {self._worker_count} notification workers")
        
        # Create worker threads
        for i in range(self._worker_count):
            thread = threading.Thread(
                target=self._worker_loop,
                args=(i,),
                daemon=True,
                name=f"NotificationWorker-{i}"
            )
            self._workers.append(thread)
            thread.start()
        
        if blocking:
            # Wait for all workers to finish (they won't unless stopped)
            try:
                while self._running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received interrupt, stopping workers...")
                self.stop()
    
    def stop(self, timeout: float = 10.0) -> None:
        """
        Stop all workers gracefully.
        
        Args:
            timeout: How long to wait for workers to finish
        """
        if not self._running:
            return
        
        logger.info("Stopping notification workers...")
        self._running = False
        self._stop_event.set()
        
        # Wait for workers to finish
        for thread in self._workers:
            thread.join(timeout=timeout / self._worker_count)
            if thread.is_alive():
                logger.warning(f"Worker {thread.name} did not stop within timeout")
        
        self._workers = []
        logger.info("All notification workers stopped")
    
    @property
    def is_running(self) -> bool:
        """Check if workers are running."""
        return self._running
    
    @property
    def active_workers(self) -> int:
        """Get count of active worker threads."""
        return sum(1 for t in self._workers if t.is_alive())

