"""
Entry point for running the tick_notifier package directly.

Usage:
    cd /path/to/Python_Explore_Concepts
    python -m tick_notifier
"""

from tick_notifier.main import NotificationSystem, create_demo_records

if __name__ == "__main__":
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

