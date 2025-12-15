#!/usr/bin/env python3
"""
Standalone runner for the tick_notifier system.

This script can be run directly from the tick_notifier folder:
    cd tick_notifier
    python3 run.py

Or from the parent folder:
    python3 tick_notifier/run.py
"""

import sys
from pathlib import Path

# Add parent directory to path so imports work when running from within the folder
parent_dir = Path(__file__).resolve().parent.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

# Now we can import using the package name
from tick_notifier.main import NotificationSystem, create_demo_records


def main():
    """Run the notification system."""
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


if __name__ == "__main__":
    main()

