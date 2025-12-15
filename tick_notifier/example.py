#!/usr/bin/env python3
"""
Example usage of the tick-based notification system.

This example demonstrates:
1. Creating notification records with different cron schedules
2. Starting the system
3. Manually triggering notifications
4. Graceful shutdown
"""

import time
import logging
from datetime import datetime

from tick_notifier.main import NotificationSystem
from tick_notifier.db.models import NotificationRecord, NotificationType
from tick_notifier.config import Config

# Set log level to see detailed output
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s",
    datefmt="%H:%M:%S"
)


def main():
    """Run the example."""
    
    print("=" * 60)
    print("🔔 Tick-Based Notification System - Example")
    print("=" * 60)
    
    # Create config with 10-second tick interval for faster testing
    config = Config()
    config.tick_interval_seconds = 10  # Check every 10 seconds for demo
    config.worker_count = 2
    
    # Initialize the system
    system = NotificationSystem(config=config)
    
    # Create notification records
    print("\n📝 Creating notification records...\n")
    
    # 1. Every-minute notification (will fire during demo)
    record1 = NotificationRecord(
        name="Test Alert (Every Minute)",
        cron_expression="* * * * *",
        notification_type=NotificationType.EMAIL,
        recipients=["test@example.com"],
        subject="Test Notification",
        message=f"This is a test notification created at {datetime.now()}",
    )
    system.add_record(record1)
    print(f"  ✅ Created: {record1.name} (id={record1.id})")
    
    # 2. Daily notification (won't fire during demo unless at scheduled time)
    record2 = NotificationRecord(
        name="Daily Digest",
        cron_expression="0 8 * * *",  # 8 AM daily
        notification_type=NotificationType.EMAIL,
        recipients=["user@example.com"],
        subject="Your Daily Digest",
        message="Here's what you missed today...",
        timezone="America/Los_Angeles"
    )
    system.add_record(record2)
    print(f"  ✅ Created: {record2.name} (id={record2.id})")
    
    # 3. Webhook notification
    record3 = NotificationRecord(
        name="Slack Alert",
        cron_expression="*/5 * * * *",  # Every 5 minutes
        notification_type=NotificationType.WEBHOOK,
        recipients=["https://hooks.slack.com/example"],
        subject="System Health Check",
        message="All systems operational",
        metadata={"channel": "#alerts", "icon": "✅"}
    )
    system.add_record(record3)
    print(f"  ✅ Created: {record3.name} (id={record3.id})")
    
    # List all records
    print("\n📋 All Notification Records:")
    print("-" * 50)
    for record in system.repository.get_all():
        status = "🟢 Active" if record.is_active else "⚪ Inactive"
        print(f"  {status} [{record.id}] {record.name}")
        print(f"         Cron: {record.cron_expression}")
        print(f"         Next: Check logs for trigger times")
    
    # Manual trigger example
    print("\n🔧 Manual Trigger Example:")
    print("-" * 50)
    print(f"  Triggering record {record1.id} manually...")
    
    # Start workers in background for manual trigger test
    system._worker.start(blocking=False)
    
    # Manually trigger first record
    system.trigger_now(record1.id)
    
    # Wait for worker to process
    time.sleep(2)
    
    # Now start full system
    print("\n🚀 Starting full notification system...")
    print("   (Press Ctrl+C to stop)")
    print("-" * 50)
    
    try:
        # Start ticker (workers already running)
        system._ticker.start(blocking=False)
        system._running = True
        
        # Run for a while
        while system.is_running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopping system...")
    finally:
        system.stop()
        print("\n✅ System stopped cleanly")


def quick_demo():
    """Quick demo that shows immediate notification."""
    
    print("\n🎯 Quick Demo - Immediate Notification")
    print("=" * 50)
    
    # Create system
    system = NotificationSystem()
    
    # Create a record
    record = NotificationRecord(
        name="Instant Test",
        cron_expression="* * * * *",
        notification_type=NotificationType.EMAIL,
        recipients=["demo@example.com"],
        subject="Hello from Tick Notifier!",
        message="This notification was triggered manually."
    )
    system.add_record(record)
    
    # Start workers only
    system._worker.start(blocking=False)
    
    # Trigger manually
    print("\n📤 Sending notification...")
    system.trigger_now(record.id)
    
    # Wait for processing
    time.sleep(2)
    
    # Cleanup
    system._worker.stop()
    
    print("\n✅ Done!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        quick_demo()
    else:
        main()

