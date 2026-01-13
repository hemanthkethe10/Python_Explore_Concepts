#!/usr/bin/env python3
"""
Combined example usage of ServiceNow Incident and Requested Items Creators
"""

from servicenow_incident_creator import ServiceNowIncidentCreator
from servicenow_request_creator import ServiceNowRequestCreator
from servicenow_config import SERVICENOW_CONFIG

def create_sample_incidents_and_requests():
    """
    Example function to create both incidents and requested items
    """
    print("ServiceNow Combined Creator - Example Usage")
    print("=" * 50)
    
    # Initialize creators with config
    incident_creator = ServiceNowIncidentCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    request_creator = ServiceNowRequestCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    # Create incidents
    print("\n1. Creating 3 sample incidents...")
    incident_results = incident_creator.create_multiple_incidents(3)
    incident_creator.print_summary(incident_results)
    
    # Create requested items
    print("\n2. Creating 3 sample requested items with tasks...")
    request_results = request_creator.create_multiple_requests(3, create_tasks=True)
    request_creator.print_summary(request_results)
    
    # Combined summary
    print("\n" + "=" * 60)
    print("COMBINED SUMMARY")
    print("=" * 60)
    print(f"Total Incidents Created: {incident_results['successful']}")
    print(f"Total Requested Items Created: {request_results['successful']}")
    print(f"Total Records Created: {incident_results['successful'] + request_results['successful']}")
    
    return incident_results, request_results

def create_custom_records():
    """
    Example of creating custom incidents and requested items
    """
    print("\n" + "=" * 60)
    print("CREATING CUSTOM RECORDS")
    print("=" * 60)
    
    # Initialize creators
    incident_creator = ServiceNowIncidentCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    request_creator = ServiceNowRequestCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    # Custom incident - High priority server issue
    custom_incident = {
        "short_description": "Critical - Production server down",
        "description": "The main production server is not responding. All services are affected.",
        "category": "Hardware",
        "subcategory": "Server",
        "priority": "1",  # Critical
        "urgency": "1",   # High urgency
        "impact": "1",    # High impact
        "state": "2",     # In Progress
        "caller_id": "admin",
        "active": "true",
        "contact_type": "phone",
        "work_notes": "Critical production issue - immediate attention required"
    }
    
    # Custom requested item - New employee setup
    custom_request = {
        "short_description": "New employee laptop and software setup",
        "description": "Complete setup for new developer including laptop, software licenses, and access permissions.",
        "cat_item": "New Employee Package",
        "category": "Hardware",
        "subcategory": "Computer",
        "priority": "2",
        "state": "1",     # Pending
        "stage": "requested",
        "approval": "requested",
        "requested_for": "abel.tuter",
        "price": "2500",
        "quantity": "1",
        "work_notes": "New developer onboarding - includes laptop, IDE licenses, and repository access"
    }
    
    print("\n1. Creating custom high-priority incident...")
    success, response_data, error_msg = incident_creator.create_incident(custom_incident)
    if success:
        incident_number = response_data['result']['number']
        print(f"✓ Successfully created incident: {incident_number}")
    else:
        print(f"✗ Failed to create incident: {error_msg}")
    
    print("\n2. Creating custom requested item...")
    success, response_data, error_msg = request_creator.create_request_item(custom_request)
    if success:
        request_number = response_data['result']['number']
        print(f"✓ Successfully created requested item: {request_number}")
    else:
        print(f"✗ Failed to create requested item: {error_msg}")

def bulk_create_mixed_records(incident_count, request_count):
    """
    Create a mix of incidents and requested items in bulk
    
    Args:
        incident_count (int): Number of incidents to create
        request_count (int): Number of requested items to create
    """
    print(f"\n" + "=" * 60)
    print(f"BULK CREATION: {incident_count} Incidents + {request_count} Requested Items")
    print("=" * 60)
    
    # Initialize creators
    incident_creator = ServiceNowIncidentCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    request_creator = ServiceNowRequestCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    # Create incidents
    if incident_count > 0:
        print(f"\nCreating {incident_count} incidents...")
        incident_results = incident_creator.create_multiple_incidents(incident_count)
        incident_creator.print_summary(incident_results)
    
    # Create requested items
    if request_count > 0:
        print(f"\nCreating {request_count} requested items with tasks...")
        request_results = request_creator.create_multiple_requests(request_count, create_tasks=True)
        request_creator.print_summary(request_results)
    
    # Final summary
    total_created = 0
    if incident_count > 0:
        total_created += incident_results['successful']
    if request_count > 0:
        total_created += request_results['successful']
    
    print(f"\n🎉 Total records successfully created: {total_created}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Bulk creation mode: python script.py <incidents> <requests>
        try:
            incident_count = int(sys.argv[1])
            request_count = int(sys.argv[2])
            bulk_create_mixed_records(incident_count, request_count)
        except ValueError:
            print("Error: Please provide valid numbers for incidents and requests")
            print("Usage: python servicenow_combined_example.py <incident_count> <request_count>")
    else:
        # Demo mode
        print("Running demo mode...")
        print("For bulk creation, use: python servicenow_combined_example.py <incident_count> <request_count>")
        
        # Run examples
        create_sample_incidents_and_requests()
        create_custom_records()
        
        print("\n" + "=" * 60)
        print("Demo completed! Check your ServiceNow instance for created records.")
        print("=" * 60)