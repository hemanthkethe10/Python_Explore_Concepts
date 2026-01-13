#!/usr/bin/env python3
"""
Example usage of ServiceNow Incident Creator
"""

from servicenow_incident_creator import ServiceNowIncidentCreator
from servicenow_config import SERVICENOW_CONFIG

def create_sample_incidents():
    """
    Example function to create sample incidents
    """
    # Initialize the creator with config
    creator = ServiceNowIncidentCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    # Create 5 sample incidents
    print("Creating 5 sample incidents...")
    results = creator.create_multiple_incidents(5)
    
    # Print results
    creator.print_summary(results)
    
    return results

def create_custom_incident():
    """
    Example of creating a single custom incident
    """
    creator = ServiceNowIncidentCreator(
        instance_url=SERVICENOW_CONFIG['instance_url'],
        username=SERVICENOW_CONFIG['username'],
        password=SERVICENOW_CONFIG['password']
    )
    
    # Custom incident data
    custom_incident = {
        "short_description": "Custom incident - Email server down",
        "description": "The main email server is not responding. Users cannot send or receive emails.",
        "category": "Software",
        "subcategory": "Email",
        "priority": "1",  # High priority
        "urgency": "1",   # High urgency
        "impact": "1",    # High impact
        "state": "2",     # In Progress
        "caller_id": "admin",
        "active": "true",
        "contact_type": "email",
        "work_notes": "Custom incident created for email server outage"
    }
    
    print("Creating custom incident...")
    success, response_data, error_msg = creator.create_incident(custom_incident)
    
    if success:
        incident_number = response_data['result']['number']
        print(f"✓ Successfully created incident: {incident_number}")
        return incident_number
    else:
        print(f"✗ Failed to create incident: {error_msg}")
        return None

if __name__ == "__main__":
    print("ServiceNow Incident Creator - Example Usage")
    print("=" * 50)
    
    # Example 1: Create multiple sample incidents
    print("\n1. Creating multiple sample incidents:")
    create_sample_incidents()
    
    # Example 2: Create a custom incident
    print("\n2. Creating a custom incident:")
    create_custom_incident()