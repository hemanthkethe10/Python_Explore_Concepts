#!/usr/bin/env python3
"""
ServiceNow Requested Items Creator
Creates N number of requested item records using REST API
"""

import requests
import json
import random
from datetime import datetime, timedelta
import sys
import time

class ServiceNowRequestCreator:
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
        self.req_item_endpoint = f"{self.instance_url}/api/now/table/sc_req_item"
        self.task_endpoint = f"{self.instance_url}/api/now/table/sc_task"
        
        # Generate unique identifier for this script run
        timestamp = int(time.time())
        random_suffix = random.randint(100, 999)
        self.run_id = f"{timestamp}_{random_suffix}"
        
        # Headers for REST API calls
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Sample data for generating realistic requested items
        self.sample_data = {
            'short_descriptions': [
                'New laptop request',
                'Software license request',
                'Mobile phone setup',
                'Printer access request',
                'VPN access setup',
                'Email account creation',
                'Database access request',
                'New user account setup',
                'Hardware replacement',
                'Office supplies request',
                'Training enrollment',
                'Conference room booking',
                'Parking pass request',
                'Building access card',
                'Equipment upgrade'
            ],
            'categories': [
                'Hardware',
                'Software',
                'Access',
                'Account',
                'Training',
                'Facilities',
                'Communication'
            ],
            'subcategories': [
                'Computer',
                'Mobile Device',
                'License',
                'Permissions',
                'Setup',
                'Replacement',
                'New Request'
            ],
            'priorities': ['1', '2', '3', '4'],
            'states': ['1', '2', '3'],  # Pending, Work in Progress, Complete (removed Delivered and Closed Complete)
            'stages': ['requested', 'in_process', 'request_approved', 'fulfillment', 'delivered'],
            'approval_states': ['not requested', 'requested', 'approved', 'rejected'],
            'requested_for_users': [
                'admin',
                'system.administrator',
                'itil',
                'abel.tuter',
                'beth.anglin',
                'charlie.whitherspoon',
                'david.loo'
            ],
            'catalog_items': [
                'Standard Laptop',
                'Desktop Computer',
                'Mobile Phone',
                'Software License',
                'VPN Access',
                'Email Setup',
                'Printer Access',
                'Training Course',
                'Office Supplies',
                'Conference Room'
            ],
            'assignment_groups': [
                'Hardware',
                'Software',
                'Network',
                'Security',
                'IT Support',
                'Desktop Support',
                'Application Support'
            ],
            'task_types': [
                'Procurement',
                'Installation',
                'Configuration',
                'Testing',
                'Delivery',
                'Training',
                'Documentation',
                'Approval'
            ],
            'task_descriptions': {
                'Procurement': [
                    'Order hardware from vendor',
                    'Purchase software license',
                    'Procure mobile device',
                    'Order office supplies'
                ],
                'Installation': [
                    'Install operating system',
                    'Install required software',
                    'Set up hardware components',
                    'Configure mobile device'
                ],
                'Configuration': [
                    'Configure user accounts',
                    'Set up network access',
                    'Configure email settings',
                    'Apply security policies'
                ],
                'Testing': [
                    'Test hardware functionality',
                    'Verify software installation',
                    'Test network connectivity',
                    'Validate user access'
                ],
                'Delivery': [
                    'Deliver equipment to user',
                    'Schedule pickup appointment',
                    'Coordinate with facilities',
                    'Arrange training session'
                ],
                'Training': [
                    'Provide user training',
                    'Create documentation',
                    'Schedule training session',
                    'Conduct orientation'
                ],
                'Documentation': [
                    'Update asset inventory',
                    'Create user guide',
                    'Document configuration',
                    'Update procedures'
                ],
                'Approval': [
                    'Manager approval required',
                    'Security review needed',
                    'Budget approval pending',
                    'Compliance check required'
                ]
            }
        }
    
    def generate_request_data(self, index):
        """
        Generate sample requested item data
        
        Args:
            index (int): Record index for unique identification
            
        Returns:
            dict: Requested item data payload
        """
        # Generate random but realistic data with more variety
        short_description = random.choice(self.sample_data['short_descriptions'])
        category = random.choice(self.sample_data['categories'])
        subcategory = random.choice(self.sample_data['subcategories'])
        priority = random.choice(self.sample_data['priorities'])
        state = random.choice(self.sample_data['states'])
        stage = random.choice(self.sample_data['stages'])
        approval = random.choice(self.sample_data['approval_states'])
        requested_for = random.choice(self.sample_data['requested_for_users'])
        catalog_item = random.choice(self.sample_data['catalog_items'])
        
        # Add some randomization to make descriptions more unique
        descriptive_words = ['urgent', 'standard', 'priority', 'routine', 'critical', 'normal']
        departments = ['Finance', 'HR', 'IT', 'Sales', 'Marketing', 'Operations']
        
        # Randomly enhance the short description
        if random.random() < 0.3:  # 30% chance to add department
            department = random.choice(departments)
            short_description = f"{department} - {short_description}"
        
        if random.random() < 0.2:  # 20% chance to add descriptive word
            desc_word = random.choice(descriptive_words)
            short_description = f"{desc_word.title()} {short_description}"
        
        # Generate description based on short description
        description = f"Detailed description for: {short_description}. " \
                     f"This is requested item #{index + 1} created via REST API (Run ID: {self.run_id}). " \
                     f"Category: {category}, Item: {catalog_item}."
        
        # Generate work notes
        work_notes = f"Request created via REST API script - Batch #{index + 1} (Run: {self.run_id}). " \
                    f"Requested for: {requested_for}. Priority: {priority}."
        
        # Create requested item payload with all essential fields
        request_data = {
            "short_description": f"{short_description} - Req#{index + 1}_Run{self.run_id}",
            "description": description,
            "cat_item": catalog_item,
            "category": category,
            "subcategory": subcategory,
            "priority": priority,
            "state": state,
            "stage": stage,
            "approval": approval,
            "requested_for": requested_for,
            "opened_by": self.username,
            "active": "true",
            "business_service": "",
            "cmdb_ci": "",
            "company": "",
            "configuration_item": "",
            "contact_type": "phone",
            "correlation_display": "",
            "correlation_id": "",
            "delivery_plan": "",
            "delivery_task": "",
            "due_date": "",
            "expected_start": "",
            "location": "",
            "made_sla": "true",
            "number": "",  # Auto-generated
            "opened_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "order": "0",
            "parent": "",
            "price": str(random.randint(50, 2000)),  # Random price between 50-2000
            "quantity": str(random.randint(1, 5)),   # Random quantity 1-5
            "reassignment_count": "0",
            "recurring_frequency": "",
            "recurring_price": "0",
            "request": "",  # Will be linked to parent request
            "sc_catalog": "",
            "service_offering": "",
            "sys_class_name": "sc_req_item",
            "sys_created_by": self.username,
            "sys_domain": "global",
            "sys_mod_count": "0",
            "task_effective_number": "",
            "upon_approval": "",
            "upon_reject": "",
            "user_input": "",
            "variables": "",
            "watch_list": "",
            "work_end": "",
            "work_notes": work_notes,
            "work_notes_list": "",
            "work_start": ""
        }
        
        return request_data
        
    def generate_task_data(self, req_item_sys_id, req_item_number, task_index, task_type=None):
        """
        Generate sample task data for a requested item
        
        Args:
            req_item_sys_id (str): System ID of the parent requested item
            req_item_number (str): Number of the parent requested item
            task_index (int): Task index for unique identification
            task_type (str): Optional specific task type
            
        Returns:
            dict: Task data payload
        """
        # Select task type
        if task_type is None:
            task_type = random.choice(self.sample_data['task_types'])
        
        # Get task description based on type with some variety
        task_descriptions = self.sample_data['task_descriptions'][task_type]
        task_description = random.choice(task_descriptions)
        
        # Add some randomization to task descriptions
        urgency_words = ['immediate', 'standard', 'scheduled', 'routine']
        if random.random() < 0.25:  # 25% chance to add urgency
            urgency_word = random.choice(urgency_words)
            task_description = f"{urgency_word.title()} {task_description.lower()}"
        
        # Generate other random data
        priority = random.choice(self.sample_data['priorities'])
        state = random.choice(['1', '2', '3'])  # Pending, Work in Progress, Complete (avoid closed states)
        assignment_group = random.choice(self.sample_data['assignment_groups'])
        
        # Create task payload
        task_data = {
            "short_description": f"{task_type}: {task_description} - Task#{task_index + 1}_Run{self.run_id}",
            "description": f"Task for {req_item_number}: {task_description}. "
                          f"This task is part of the fulfillment process for the requested item (Run ID: {self.run_id}).",
            "request_item": req_item_sys_id,
            "parent": req_item_sys_id,
            "priority": priority,
            "state": state,
            "assignment_group": assignment_group,
            "assigned_to": "",
            "active": "true",
            "opened_by": self.username,
            "business_service": "",
            "cmdb_ci": "",
            "company": "",
            "contact_type": "phone",
            "correlation_display": "",
            "correlation_id": "",
            "delivery_plan": "",
            "delivery_task": "",
            "due_date": "",
            "expected_start": "",
            "location": "",
            "made_sla": "true",
            "number": "",  # Auto-generated
            "opened_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "order": str(task_index),
            "reassignment_count": "0",
            "sys_class_name": "sc_task",
            "sys_created_by": self.username,
            "sys_domain": "global",
            "sys_mod_count": "0",
            "task_effective_number": "",
            "upon_approval": "",
            "upon_reject": "",
            "watch_list": "",
            "work_end": "",
            "work_notes": f"Task created for {req_item_number} - {task_type} phase (Run: {self.run_id})",
            "work_notes_list": "",
            "work_start": ""
        }
        
        return task_data
    
    def create_task(self, task_data):
        """
        Create a single task record
        
        Args:
            task_data (dict): Task data payload
            
        Returns:
            tuple: (success: bool, response_data: dict, error_message: str)
        """
        try:
            response = requests.post(
                self.task_endpoint,
                headers=self.headers,
                data=json.dumps(task_data),
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
    
    def create_request_item(self, request_data):
        """
        Create a single requested item record
        
        Args:
            request_data (dict): Requested item data payload
            
        Returns:
            tuple: (success: bool, response_data: dict, error_message: str)
        """
        try:
            response = requests.post(
                self.req_item_endpoint,
                headers=self.headers,
                data=json.dumps(request_data),
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
    
    def create_multiple_requests(self, count, create_tasks=True, tasks_per_request=None):
        """
        Create multiple requested item records with optional tasks
        
        Args:
            count (int): Number of requested items to create
            create_tasks (bool): Whether to create tasks for some requests
            tasks_per_request (int): Number of tasks per request (random 1-3 if None)
            
        Returns:
            dict: Summary of creation results
        """
        results = {
            'total_requested': count,
            'successful': 0,
            'failed': 0,
            'created_requests': [],
            'created_tasks': [],
            'errors': []
        }
        
        print(f"Starting creation of {count} requested item records...")
        print(f"Run ID: {self.run_id}")
        if create_tasks:
            print("Tasks will be created for some requested items...")
        print("-" * 60)
        
        for i in range(count):
            print(f"Creating requested item {i + 1}/{count}...", end=" ")
            
            # Generate request data
            request_data = self.generate_request_data(i)
            
            # Create requested item
            success, response_data, error_msg = self.create_request_item(request_data)
            
            if success:
                request_number = response_data['result']['number']
                request_sys_id = response_data['result']['sys_id']
                results['successful'] += 1
                
                request_info = {
                    'number': request_number,
                    'sys_id': request_sys_id,
                    'short_description': request_data['short_description'],
                    'requested_for': request_data['requested_for'],
                    'cat_item': request_data['cat_item'],
                    'tasks': []
                }
                
                print(f"✓ Created: {request_number}", end="")
                
                # Create tasks for this request (70% chance)
                if create_tasks and random.random() < 0.7:
                    num_tasks = tasks_per_request if tasks_per_request else random.randint(1, 3)
                    print(f" + {num_tasks} tasks", end="")
                    
                    for task_idx in range(num_tasks):
                        task_data = self.generate_task_data(request_sys_id, request_number, task_idx)
                        task_success, task_response, task_error = self.create_task(task_data)
                        
                        if task_success:
                            task_number = task_response['result']['number']
                            task_sys_id = task_response['result']['sys_id']
                            
                            task_info = {
                                'number': task_number,
                                'sys_id': task_sys_id,
                                'short_description': task_data['short_description'],
                                'parent_request': request_number,
                                'assignment_group': task_data['assignment_group']
                            }
                            
                            request_info['tasks'].append(task_info)
                            results['created_tasks'].append(task_info)
                        else:
                            results['errors'].append({
                                'type': 'task',
                                'parent_request': request_number,
                                'task_index': task_idx + 1,
                                'error': task_error
                            })
                
                results['created_requests'].append(request_info)
                print()  # New line
                
            else:
                results['failed'] += 1
                results['errors'].append({
                    'type': 'request',
                    'index': i + 1,
                    'error': error_msg
                })
                print(f"✗ Failed: {error_msg}")
        
        return results
    
    def print_summary(self, results):
        """
        Print creation summary including tasks
        
        Args:
            results (dict): Results from create_multiple_requests
        """
        print("\n" + "=" * 60)
        print("REQUESTED ITEMS CREATION SUMMARY")
        print("=" * 60)
        print(f"Total Requested: {results['total_requested']}")
        print(f"Successfully Created: {results['successful']}")
        print(f"Failed: {results['failed']}")
        
        if 'created_tasks' in results and results['created_tasks']:
            print(f"Total Tasks Created: {len(results['created_tasks'])}")
        
        if results['created_requests']:
            print(f"\nCreated Requested Items:")
            for request in results['created_requests']:
                print(f"  • {request['number']}: {request['short_description']}")
                print(f"    └─ Item: {request['cat_item']}, For: {request['requested_for']}")
                
                if request.get('tasks'):
                    print(f"    └─ Tasks ({len(request['tasks'])}):")
                    for task in request['tasks']:
                        print(f"       • {task['number']}: {task['short_description']}")
                        print(f"         └─ Assigned to: {task['assignment_group']}")
        
        if results['errors']:
            print(f"\nErrors:")
            for error in results['errors']:
                if error.get('type') == 'task':
                    print(f"  • Task {error['task_index']} for {error['parent_request']}: {error['error']}")
                else:
                    print(f"  • Record {error.get('index', 'Unknown')}: {error['error']}")


def main():
    """
    Main function to run the requested items creator
    """
    # Configuration - Update these values
    INSTANCE_URL = "https://xenovusdemo1.service-now.com"
    USERNAME = "admin"
    PASSWORD = "admin"
    
    print("ServiceNow Requested Items Creator")
    print("=" * 40)
    
    # Create ServiceNow request creator instance to get run ID
    creator = ServiceNowRequestCreator(INSTANCE_URL, USERNAME, PASSWORD)
    print(f"Session Run ID: {creator.run_id}")
    print()
    
    # Get number of records to create
    try:
        if len(sys.argv) > 1:
            num_records = int(sys.argv[1])
        else:
            num_records = int(input("Enter the number of requested item records to create: "))
        
        if num_records <= 0:
            print("Error: Number of records must be greater than 0")
            return
            
    except ValueError:
        print("Error: Please enter a valid number")
        return
    
    # Ask about task creation
    create_tasks_input = input("Create tasks for some requested items? (Y/n): ")
    create_tasks = create_tasks_input.lower() != 'n'
    
    # Confirm creation
    task_msg = " (with tasks)" if create_tasks else ""
    confirm = input(f"\nThis will create {num_records} requested item records{task_msg} in {INSTANCE_URL}. Continue? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Create ServiceNow request creator instance
    # creator = ServiceNowRequestCreator(INSTANCE_URL, USERNAME, PASSWORD)  # Already created above
    
    # Create requested items with optional tasks
    results = creator.create_multiple_requests(num_records, create_tasks=create_tasks)
    
    # Print summary
    creator.print_summary(results)


if __name__ == "__main__":
    main()