#!/usr/bin/env python3
"""
Test script to verify Redis queue is working.

This script:
1. Connects to Redis
2. Pushes a test job (without workers consuming it)
3. Shows the job in the queue
4. Cleans up

Run: python3 test_redis_queue.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from tick_notifier.queues.redis_queue import RedisQueue
from tick_notifier.queues.base import NotificationJob


def main():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    queue_name = "notification_jobs"
    
    print("=" * 60)
    print("🧪 Redis Queue Test")
    print("=" * 60)
    print(f"Redis URL: {redis_url}")
    print(f"Queue name: {queue_name}")
    print()
    
    # Connect to Redis
    try:
        queue = RedisQueue(redis_url=redis_url, queue_name=queue_name)
        print("✅ Connected to Redis")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)
    
    # Show current queue size
    print(f"\n📊 Current queue size: {queue.size()}")
    
    # Push a test job
    print("\n📤 Pushing test job...")
    test_job = NotificationJob(
        record_id="test-123",
        scheduled_time=datetime.utcnow(),
        notification_config={
            "type": "email",
            "recipients": ["test@example.com"],
            "subject": "Test Notification",
            "message": "This is a test job to verify Redis queue"
        }
    )
    queue.push(test_job)
    print(f"   Job ID: {test_job.job_id}")
    
    # Show queue size after push
    print(f"\n📊 Queue size after push: {queue.size()}")
    
    # Peek at jobs in queue
    print("\n👀 Jobs in queue:")
    jobs = queue.peek(count=5)
    for i, job in enumerate(jobs, 1):
        print(f"   {i}. Job ID: {job.job_id}")
        print(f"      Record: {job.record_id}")
        print(f"      Type: {job.notification_config.get('type')}")
    
    # Verify with raw Redis command
    print("\n🔍 Raw Redis verification:")
    print(f"   Run: redis-cli LRANGE {queue_name} 0 -1")
    
    # Ask user what to do
    print("\n" + "=" * 60)
    response = input("Clean up test job? [y/N]: ").strip().lower()
    
    if response == 'y':
        # Pop the job we just added
        popped = queue.pop(timeout=None)
        if popped:
            print(f"✅ Cleaned up job: {popped.job_id}")
        print(f"📊 Final queue size: {queue.size()}")
    else:
        print("⚠️  Test job left in queue. Check with: redis-cli LRANGE notification_jobs 0 -1")
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    main()

