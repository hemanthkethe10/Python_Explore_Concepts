# ServiceNow Record Creator

A comprehensive Python toolkit for creating ServiceNow records (Incidents and Requested Items) via REST API.

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `servicenow_incident_creator.py` | Main script for creating incident records |
| `servicenow_request_creator.py` | Main script for creating requested item records |
| `servicenow_config.py` | Configuration file with settings and sample data |
| `servicenow_cli.py` | Command-line interface for easy usage |
| `servicenow_combined_example.py` | Examples showing both incidents and requests |
| `example_usage.py` | Basic usage examples for incidents |
| `servicenow_requirements.txt` | Python dependencies |

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r servicenow_requirements.txt
```

### 2. Update Configuration
Edit `servicenow_config.py` with your ServiceNow instance details:
```python
SERVICENOW_CONFIG = {
    'instance_url': 'https://your-instance.service-now.com',
    'username': 'your_username',
    'password': 'your_password',
    'timeout': 30
}
```

### 3. Create Records

#### Using CLI (Recommended)
```bash
# Create 5 incidents
python servicenow_cli.py incidents 5

# Create 3 requested items (with tasks by default)
python servicenow_cli.py requests 3

# Create requested items without tasks
python servicenow_cli.py requests 3 --no-tasks

# Create both: 5 incidents + 3 requests (with tasks)
python servicenow_cli.py both 5 3

# With custom credentials
python servicenow_cli.py incidents 10 --url https://dev.service-now.com --user admin --pass admin
```

#### Using Individual Scripts
```bash
# Create incidents
python servicenow_incident_creator.py 5

# Create requested items (will ask about tasks)
python servicenow_request_creator.py 3
```

#### Using as Python Modules
```python
from servicenow_incident_creator import ServiceNowIncidentCreator
from servicenow_request_creator import ServiceNowRequestCreator

# Create incidents
incident_creator = ServiceNowIncidentCreator(url, username, password)
results = incident_creator.create_multiple_incidents(5)

# Create requested items with tasks
request_creator = ServiceNowRequestCreator(url, username, password)
results = request_creator.create_multiple_requests(3, create_tasks=True)

# Create requested items without tasks
results = request_creator.create_multiple_requests(3, create_tasks=False)
```

## 📋 Features

### Incident Creator Features
- ✅ **Complete field coverage**: All essential ServiceNow incident fields
- ✅ **Realistic sample data**: Varied categories, priorities, and descriptions
- ✅ **Batch creation**: Create N number of records efficiently
- ✅ **Progress tracking**: Real-time creation status and summary
- ✅ **Error handling**: Robust error handling with detailed feedback
- ✅ **Flexible usage**: CLI, module import, or direct script execution

### Requested Items Creator Features
- ✅ **Catalog item support**: Realistic catalog items and categories
- ✅ **Request lifecycle**: Proper states, stages, and approval flows
- ✅ **Pricing and quantity**: Random but realistic pricing data
- ✅ **User assignment**: Proper requested_for field handling
- ✅ **Work notes**: Detailed tracking information
- ✅ **Task creation**: Automatically creates fulfillment tasks for RITMs
- ✅ **Task variety**: Multiple task types (Procurement, Installation, Configuration, etc.)
- ✅ **Assignment groups**: Tasks assigned to appropriate groups

### Sample Data Categories

#### Incidents
- **IT Issues**: Email, network, hardware, software problems
- **HR Issues**: Onboarding, benefits, payroll inquiries
- **Facilities**: Building access, temperature, equipment

#### Requested Items
- **Hardware**: Laptops, desktops, mobile devices, peripherals
- **Software**: Licenses, applications, development tools
- **Access**: VPN, database, building access, permissions
- **Training**: Courses, certifications, conferences

#### Tasks (for Requested Items)
- **Procurement**: Ordering, purchasing, vendor management
- **Installation**: Software installation, hardware setup
- **Configuration**: User accounts, network setup, security policies
- **Testing**: Functionality testing, validation, verification
- **Delivery**: Equipment delivery, scheduling, coordination
- **Training**: User training, documentation, orientation
- **Documentation**: Asset updates, guides, procedures
- **Approval**: Manager approval, security review, compliance

## 🔧 Configuration Options

### Basic Configuration
```python
SERVICENOW_CONFIG = {
    'instance_url': 'https://your-instance.service-now.com',
    'username': 'your_username',
    'password': 'your_password',
    'timeout': 30
}
```

### Custom Sample Data
You can customize the sample data in `servicenow_config.py`:

```python
SAMPLE_DATA_TEMPLATES = {
    'incidents': {
        'custom_category': {
            'short_descriptions': ['Custom issue 1', 'Custom issue 2'],
            'categories': ['Custom', 'Category']
        }
    },
    'requested_items': {
        'custom_requests': {
            'short_descriptions': ['Custom request 1', 'Custom request 2'],
            'catalog_items': ['Custom Item', 'Another Item']
        }
    }
}
```

## 📊 Field Mappings

### Incident Fields
| Field | Type | Description |
|-------|------|-------------|
| `short_description` | Required | Brief description of the incident |
| `caller_id` | Required | User who reported the incident |
| `description` | Optional | Detailed description |
| `category` | Optional | Incident category |
| `priority` | Optional | Priority level (1-5) |
| `urgency` | Optional | Urgency level (1-3) |
| `impact` | Optional | Impact level (1-3) |
| `state` | Optional | Current state |

### Requested Item Fields
| Field | Type | Description |
|-------|------|-------------|
| `short_description` | Required | Brief description of the request |
| `requested_for` | Required | User the item is requested for |
| `cat_item` | Optional | Catalog item name |
| `category` | Optional | Request category |
| `priority` | Optional | Priority level (1-4) |
| `state` | Optional | Current state |
| `stage` | Optional | Request stage |
| `price` | Optional | Item price |
| `quantity` | Optional | Quantity requested |

### Task Fields (for Requested Items)
| Field | Type | Description |
|-------|------|-------------|
| `short_description` | Required | Brief description of the task |
| `request_item` | Required | Parent requested item sys_id |
| `assignment_group` | Optional | Group assigned to complete task |
| `priority` | Optional | Task priority level |
| `state` | Optional | Current task state |
| `work_notes` | Optional | Task progress notes |

## 🎯 Usage Examples

### Example 1: Basic Creation
```python
# Create 10 incidents
python servicenow_incident_creator.py 10

# Create 5 requested items
python servicenow_request_creator.py 5
```

### Example 2: Custom Records
```python
from servicenow_incident_creator import ServiceNowIncidentCreator

creator = ServiceNowIncidentCreator(url, username, password)

# Custom incident data
custom_incident = {
    "short_description": "Critical server outage",
    "description": "Production server is down",
    "priority": "1",
    "urgency": "1",
    "impact": "1",
    "category": "Hardware",
    "caller_id": "admin"
}

success, response, error = creator.create_incident(custom_incident)
```

### Example 3: Bulk Mixed Creation
```python
# Create 10 incidents and 5 requests
python servicenow_cli.py both 10 5
```

## 🔍 API Endpoints Used

- **Incidents**: `/api/now/table/incident`
- **Requested Items**: `/api/now/table/sc_req_item`
- **Tasks**: `/api/now/table/sc_task`

## 📈 Sample Output

### Requested Items with Tasks
```
ServiceNow Requested Items Creator
========================================
Enter the number of requested item records to create: 3
Create tasks for some requested items? (Y/n): y

This will create 3 requested item records (with tasks) in https://xenovusdemo1.service-now.com. Continue? (y/N): y

Starting creation of 3 requested item records...
Tasks will be created for some requested items...
------------------------------------------------------------
Creating requested item 1/3... ✓ Created: RITM0010001 + 2 tasks
Creating requested item 2/3... ✓ Created: RITM0010002 + 1 tasks
Creating requested item 3/3... ✓ Created: RITM0010003 + 3 tasks

============================================================
REQUESTED ITEMS CREATION SUMMARY
============================================================
Total Requested: 3
Successfully Created: 3
Failed: 0
Total Tasks Created: 6

Created Requested Items:
  • RITM0010001: New laptop request - Request #1
    └─ Item: Standard Laptop, For: abel.tuter
    └─ Tasks (2):
       • SCTASK0010001: Procurement: Order hardware from vendor - Task #1
         └─ Assigned to: Hardware
       • SCTASK0010002: Installation: Install operating system - Task #2
         └─ Assigned to: Desktop Support
  • RITM0010002: Software license request - Request #2
    └─ Item: Software License, For: beth.anglin
    └─ Tasks (1):
       • SCTASK0010003: Approval: Manager approval required - Task #1
         └─ Assigned to: IT Support
  • RITM0010003: VPN access setup - Request #3
    └─ Item: VPN Access, For: charlie.whitherspoon
    └─ Tasks (3):
       • SCTASK0010004: Configuration: Configure user accounts - Task #1
         └─ Assigned to: Network
       • SCTASK0010005: Testing: Test network connectivity - Task #2
         └─ Assigned to: Network
       • SCTASK0010006: Documentation: Update procedures - Task #3
         └─ Assigned to: IT Support

✅ Operation completed successfully!
```

### Incidents Only
```
ServiceNow Record Creator CLI
========================================
Instance: https://xenovusdemo1.service-now.com
User: admin
Will create: 5 incidents

Continue? (y/N): y

Starting creation of 5 incident records...
------------------------------------------------------------
Creating incident 1/5... ✓ Created: INC0010001
Creating incident 2/5... ✓ Created: INC0010002
Creating incident 3/5... ✓ Created: INC0010003
Creating incident 4/5... ✓ Created: INC0010004
Creating incident 5/5... ✓ Created: INC0010005

============================================================
INCIDENT CREATION SUMMARY
============================================================
Total Requested: 5
Successfully Created: 5
Failed: 0

Created Incidents:
  • INC0010001: Unable to access email - Record #1
  • INC0010002: Computer running slowly - Record #2
  • INC0010003: Application not responding - Record #3
  • INC0010004: Network connectivity issues - Record #4
  • INC0010005: Printer not working - Record #5

✅ Operation completed successfully!
```

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Error**
   - Verify username/password in config
   - Check if account has proper permissions

2. **Connection Timeout**
   - Verify instance URL is correct
   - Check network connectivity
   - Increase timeout in config

3. **Field Validation Errors**
   - Check required fields are provided
   - Verify field values match ServiceNow constraints

### Debug Mode
Add debug information by modifying the scripts to include more verbose logging.

## 🔒 Security Notes

- Store credentials securely (consider environment variables)
- Use service accounts with minimal required permissions
- Implement proper error handling for production use
- Consider rate limiting for large batch operations

## 📝 License

This toolkit is provided as-is for educational and development purposes. Ensure compliance with your organization's ServiceNow usage policies.

## 🤝 Contributing

Feel free to extend the scripts with additional features:
- More record types (Change Requests, Problems, etc.)
- Advanced field validation
- Bulk update capabilities
- Integration with other systems

---

**Happy ServiceNow automating! 🚀**