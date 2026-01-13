#!/usr/bin/env python3
"""
ServiceNow Incident Record Creator
Creates N number of incident records using REST API
"""

import requests
import json
import random
from datetime import datetime, timedelta
import sys
import time

class ServiceNowIncidentCreator:
    def __init__(self, instance_url, username, password):
        """
        Initialize ServiceNow connection
        
        Args:
            instance_url (str): ServiceNow instance URL (e.g., 'https://xenovusdemo1.service-now.com')
            username (str): ServiceNow username
            password (str): ServiceNow password
        """
        self.instance_url = instance_url.rstrip('/')
        self.username = username
        self.password = password
        self.api_endpoint = f"{self.instance_url}/api/now/table/incident"
        
        # Generate unique identifier for this script run
        timestamp = int(time.time())
        random_suffix = random.randint(100, 999)
        self.run_id = f"{timestamp}_{random_suffix}"
        
        # Headers for REST API calls
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Sample data for generating realistic incidents
        self.sample_data = {
            'short_descriptions': [
                'Unable to access email',
                'Computer running slowly',
                'Application not responding',
                'Network connectivity issues',
                'Printer not working',
                'Password reset required',
                'Software installation request',
                'Database connection error',
                'Website loading issues',
                'VPN connection problems'
            ],
            'categories': [
                'Hardware',
                'Software',
                'Network',
                'Database',
                'Security',
                'Email',
                'Printing'
            ],
            'subcategories': [
                'Desktop',
                'Laptop',
                'Server',
                'Application',
                'Operating System',
                'Connectivity',
                'Performance'
            ],
            'priorities': ['1', '2', '3', '4', '5'],
            'urgencies': ['1', '2', '3'],
            'impacts': ['1', '2', '3'],
            'states': ['1', '2', '3'],  # New, In Progress, On Hold (removed Resolved and Closed states)
            'caller_ids': [
                'admin',
                'system.administrator',
                'itil',
                'abel.tuter',
                'beth.anglin'
            ]
        }
    
    def generate_incident_data(self, index):
        """
        Generate sample incident data
        
        Args:
            index (int): Record index for unique identification
            
        Returns:
            dict: Incident data payload
        """
        # Generate random but realistic data with more variety
        short_description = random.choice(self.sample_data['short_descriptions'])
        category = random.choice(self.sample_data['categories'])
        subcategory = random.choice(self.sample_data['subcategories'])
        priority = random.choice(self.sample_data['priorities'])
        urgency = random.choice(self.sample_data['urgencies'])
        impact = random.choice(self.sample_data['impacts'])
        state = random.choice(self.sample_data['states'])
        caller_id = random.choice(self.sample_data['caller_ids'])
        
        # Add some randomization to make descriptions more unique
        severity_words = ['minor', 'major', 'critical', 'intermittent', 'recurring']
        locations = ['Building A', 'Building B', 'Remote', 'Data Center', 'Office Floor 1', 'Office Floor 2']
        
        # Randomly enhance the short description
        if random.random() < 0.3:  # 30% chance to add location
            location = random.choice(locations)
            short_description = f"{location} - {short_description}"
        
        if random.random() < 0.2:  # 20% chance to add severity word
            severity = random.choice(severity_words)
            short_description = f"{severity.title()} {short_description}"
        
        # Generate description based on short description
        description = f"Detailed description for: {short_description}. " \
                     f"This is incident #{index + 1} created via REST API (Run ID: {self.run_id}). " \
                     f"Category: {category}, Subcategory: {subcategory}."
        
        # Create incident payload with all essential fields
        incident_data = {
            "short_description": f"{short_description} - Inc#{index + 1}_Run{self.run_id}",
            "description": description,
            "category": category,
            "subcategory": subcategory,
            "priority": priority,
            "urgency": urgency,
            "impact": impact,
            "state": state,
            "caller_id": caller_id,
            "active": "true",
            "opened_by": caller_id,
            "assignment_group": "",
            "assigned_to": "",
            "business_service": "",
            "cmdb_ci": "",
            "company": "",
            "contact_type": "phone",
            "location": "",
            "made_sla": "true",
            "notify": "1",
            "opened_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "order": "",
            "parent": "",
            "parent_incident": "",
            "problem_id": "",
            "reassignment_count": "0",
            "reopen_count": "0",
            "resolved_at": "",
            "resolved_by": "",
            "close_code": "",
            "close_notes": "",
            "resolution_code": "",
            "rfc": "",
            "severity": "3",
            "sys_class_name": "incident",
            "sys_created_by": self.username,
            "sys_domain": "global",
            "sys_mod_count": "0",
            "upon_approval": "",
            "upon_reject": "",
            "watch_list": "",
            "work_end": "",
            "work_notes": f"Incident created via REST API script - Batch #{index + 1} (Run: {self.run_id})",
            "work_notes_list": "",
            "work_start": ""
        }
        
        return incident_data
    
    def create_incident(self, incident_data):
        """
        Create a single incident record
        
        Args:
            incident_data (dict): Incident data payload
            
        Returns:
            tuple: (success: bool, response_data: dict, error_message: str)
        """
        try:
            response = requests.post(
                self.api_endpoint,
                headers=self.headers,
                data=json.dumps(incident_data),
                auth=(self.username, self.password),
                timeout=30
            )
            
            if response.status_code == 201:
                return True, response.json(), None
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                return False, None, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, None, str(e)
    
    def create_multiple_incidents(self, count):
        """
        Create multiple incident records
        
        Args:
            count (int): Number of incidents to create
            
        Returns:
            dict: Summary of creation results
        """
        results = {
            'total_requested': count,
            'successful': 0,
            'failed': 0,
            'created_incidents': [],
            'errors': []
        }
        
        print(f"Starting creation of {count} incident records...")
        print(f"Run ID: {self.run_id}")
        print("-" * 60)
        
        for i in range(count):
            print(f"Creating incident {i + 1}/{count}...", end=" ")
            
            # Generate incident data
            incident_data = self.generate_incident_data(i)
            
            # Create incident
            success, response_data, error_msg = self.create_incident(incident_data)
            
            if success:
                incident_number = response_data['result']['number']
                incident_sys_id = response_data['result']['sys_id']
                results['successful'] += 1
                results['created_incidents'].append({
                    'number': incident_number,
                    'sys_id': incident_sys_id,
                    'short_description': incident_data['short_description']
                })
                print(f"✓ Created: {incident_number}")
            else:
                results['failed'] += 1
                results['errors'].append({
                    'index': i + 1,
                    'error': error_msg
                })
                print(f"✗ Failed: {error_msg}")
        
        return results
    
    def print_summary(self, results):
        """
        Print creation summary
        
        Args:
            results (dict): Results from create_multiple_incidents
        """
        print("\n" + "=" * 60)
        print("INCIDENT CREATION SUMMARY")
        print("=" * 60)
        print(f"Total Requested: {results['total_requested']}")
        print(f"Successfully Created: {results['successful']}")
        print(f"Failed: {results['failed']}")
        
        if results['created_incidents']:
            print(f"\nCreated Incidents:")
            for incident in results['created_incidents']:
                print(f"  • {incident['number']}: {incident['short_description']}")
        
        if results['errors']:
            print(f"\nErrors:")
            for error in results['errors']:
                print(f"  • Record {error['index']}: {error['error']}")


def main():
    """
    Main function to run the incident creator
    """
    # Configuration - Update these values
    INSTANCE_URL = "https://xenovusdemo1.service-now.com"
    USERNAME = "admin"
    PASSWORD = "admin"
    
    print("ServiceNow Incident Creator")
    print("=" * 40)
    
    # Create ServiceNow incident creator instance to get run ID
    creator = ServiceNowIncidentCreator(INSTANCE_URL, USERNAME, PASSWORD)
    print(f"Session Run ID: {creator.run_id}")
    print()
    
    # Get number of records to create
    try:
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = int(input("Enter the number of incident records to create: "))
        
        if num_records <= 0:
            print("Error: Number of records must be greater than 0")
            return
            
    except ValueError:
        print("Error: Please enter a valid number")
        return
    
    # Confirm creation
    confirm = input(f"\nThis will create {num_records} incident records in {INSTANCE_URL}. Continue? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Create ServiceNow incident creator instance
    # creator = ServiceNowIncidentCreator(INSTANCE_URL, USERNAME, PASSWORD)  # Already created above
    
    # Create incidents
    results = creator.create_multiple_incidents(num_records)
    
    # Print summary
    creator.print_summary(results)


if __name__ == "__main__":
    main()