#!/usr/bin/env python3
"""
Run the notification system with Redis queue.

Prerequisites:
    1. Install Redis: pip install redis
    2. Start Redis server: redis-server (or use Docker: docker run -p 6379:6379 redis)
    3. Run this script: python3 run_with_redis.py

Environment variables:
    REDIS_URL: Redis connection URL (default: redis://localhost:6379/0)
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from tick_notifier.queues.redis_queue import RedisQueue
from tick_notifier.main import NotificationSystem, create_demo_records


def main():
    """Run the notification system with Redis queue."""
    
    # Get Redis URL from environment or use default
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    print("=" * 60)
    print("🔔 Tick-Based Notification System (Redis Mode)")
    print("=" * 60)
    print(f"Redis URL: {redis_url}")
    print()
    
    try:
        # Create Redis queue
        queue = RedisQueue(redis_url=redis_url)
        print(f"✅ Connected to Redis (queue size: {queue.size()})")
        
    except Exception as e:
        print(f"❌ Failed to connect to Redis: {e}")
        print()
        print("Make sure Redis is running:")
        print("  Option 1: redis-server")
        print("  Option 2: docker run -d -p 6379:6379 redis")
        sys.exit(1)
    
    # Create system with Redis queue
    system = NotificationSystem(queue=queue)
    
    # Create demo records
    create_demo_records(system.repository)
    
    # List all records
    print("\n📋 Registered Notification Records:")
    print("-" * 50)
    for record in system.repository.get_all():
        print(f"  [{record.id}] {record.name}")
        print(f"      Cron: {record.cron_expression} ({record.timezone})")
        print(f"      Type: {record.notification_type.value}")
        print()
    
    print("Starting notification system with Redis queue...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Start the system
    system.start(blocking=True)


if __name__ == "__main__":
    main()

