#!/usr/bin/env python3
"""
ServiceNow CLI - Command Line Interface for creating incidents and requested items
"""

import sys
import argparse
from servicenow_incident_creator import ServiceNowIncidentCreator
from servicenow_request_creator import ServiceNowRequestCreator
from servicenow_config import SERVICENOW_CONFIG

def create_incidents(count, config=None):
    """Create incidents using the incident creator"""
    if config is None:
        config = SERVICENOW_CONFIG
    
    creator = ServiceNowIncidentCreator(
        instance_url=config['instance_url'],
        username=config['username'],
        password=config['password']
    )
    
    print(f"Incident Creator Run ID: {creator.run_id}")
    results = creator.create_multiple_incidents(count)
    creator.print_summary(results)
    return results

def create_requests(count, config=None, create_tasks=True):
    """Create requested items using the request creator"""
    if config is None:
        config = SERVICENOW_CONFIG
    
    creator = ServiceNowRequestCreator(
        instance_url=config['instance_url'],
        username=config['username'],
        password=config['password']
    )
    
    print(f"Request Creator Run ID: {creator.run_id}")
    results = creator.create_multiple_requests(count, create_tasks=create_tasks)
    creator.print_summary(results)
    return results

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='ServiceNow Record Creator CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s incidents 5                    # Create 5 incidents
  %(prog)s requests 3                     # Create 3 requested items
  %(prog)s both 5 3                       # Create 5 incidents and 3 requests
  %(prog)s incidents 10 --url https://dev.service-now.com --user admin --pass admin
        """
    )
    
    parser.add_argument(
        'type',
        choices=['incidents', 'requests', 'both'],
        help='Type of records to create'
    )
    
    parser.add_argument(
        'count',
        type=int,
        help='Number of records to create (for incidents or requests)'
    )
    
    parser.add_argument(
        'request_count',
        type=int,
        nargs='?',
        help='Number of requested items to create (only used with "both" type)'
    )
    
    parser.add_argument(
        '--url',
        default=SERVICENOW_CONFIG['instance_url'],
        help=f'ServiceNow instance URL (default: {SERVICENOW_CONFIG["instance_url"]})'
    )
    
    parser.add_argument(
        '--user',
        default=SERVICENOW_CONFIG['username'],
        help=f'ServiceNow username (default: {SERVICENOW_CONFIG["username"]})'
    )
    
    parser.add_argument(
        '--pass',
        dest='password',
        default=SERVICENOW_CONFIG['password'],
        help='ServiceNow password (default: from config)'
    )
    
    parser.add_argument(
        '--no-tasks',
        action='store_true',
        help='Skip creating tasks for requested items'
    )
    
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='Skip confirmation prompt'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.type == 'both' and args.request_count is None:
        parser.error("'both' type requires both incident count and request count")
    
    if args.count <= 0:
        parser.error("Count must be greater than 0")
    
    if args.type == 'both' and args.request_count <= 0:
        parser.error("Request count must be greater than 0")
    
    # Create config from arguments
    config = {
        'instance_url': args.url,
        'username': args.user,
        'password': args.password,
        'timeout': SERVICENOW_CONFIG.get('timeout', 30)
    }
    
    # Show what will be created
    print("ServiceNow Record Creator CLI")
    print("=" * 40)
    print(f"Instance: {config['instance_url']}")
    print(f"User: {config['username']}")
    
    if args.type == 'incidents':
        print(f"Will create: {args.count} incidents")
    elif args.type == 'requests':
        print(f"Will create: {args.count} requested items")
    elif args.type == 'both':
        print(f"Will create: {args.count} incidents + {args.request_count} requested items")
    
    # Confirmation
    if not args.no_confirm:
        confirm = input("\nContinue? (y/N): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Execute creation
    try:
        if args.type == 'incidents':
            results = create_incidents(args.count, config)
            success_count = results['successful']
            
        elif args.type == 'requests':
            create_tasks = not args.no_tasks
            results = create_requests(args.count, config, create_tasks=create_tasks)
            success_count = results['successful']
            
        elif args.type == 'both':
            print(f"\nCreating {args.count} incidents...")
            incident_results = create_incidents(args.count, config)
            
            print(f"\nCreating {args.request_count} requested items...")
            create_tasks = not args.no_tasks
            request_results = create_requests(args.request_count, config, create_tasks=create_tasks)
            
            success_count = incident_results['successful'] + request_results['successful']
            
            print(f"\n🎉 Total records successfully created: {success_count}")
        
        print(f"\n✅ Operation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()