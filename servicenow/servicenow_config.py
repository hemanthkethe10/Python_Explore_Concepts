"""
ServiceNow Configuration
Update these settings for your ServiceNow instance
"""

# ServiceNow Instance Configuration
SERVICENOW_CONFIG = {
    'instance_url': 'https://xenovusdemo1.service-now.com',
    'username': 'admin',
    'password': 'Xenovus1104$',
    'timeout': 30  # Request timeout in seconds
}

# Incident Field Mappings (for reference)
INCIDENT_FIELDS = {
    'required_fields': [
        'short_description',
        'caller_id'
    ],
    'optional_fields': [
        'description',
        'category',
        'subcategory',
        'priority',
        'urgency',
        'impact',
        'state',
        'assignment_group',
        'assigned_to',
        'business_service',
        'cmdb_ci',
        'company',
        'contact_type',
        'location',
        'work_notes'
    ]
}

# Requested Items Field Mappings (for reference)
REQUESTED_ITEM_FIELDS = {
    'required_fields': [
        'short_description',
        'requested_for'
    ],
    'optional_fields': [
        'description',
        'cat_item',
        'category',
        'subcategory',
        'priority',
        'state',
        'stage',
        'approval',
        'price',
        'quantity',
        'due_date',
        'work_notes'
    ]
}

# Sample Data Templates
SAMPLE_DATA_TEMPLATES = {
    'incidents': {
        'it_issues': {
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
            'categories': ['Hardware', 'Software', 'Network', 'Database', 'Security']
        },
        'hr_issues': {
            'short_descriptions': [
                'New employee onboarding',
                'Benefits enrollment issue',
                'Payroll inquiry',
                'Time off request problem',
                'Training access needed'
            ],
            'categories': ['HR', 'Payroll', 'Benefits', 'Training']
        },
        'facilities_issues': {
            'short_descriptions': [
                'Office temperature too hot/cold',
                'Lighting not working',
                'Desk/chair request',
                'Parking pass needed',
                'Building access issue'
            ],
            'categories': ['Facilities', 'Building', 'Parking', 'Equipment']
        }
    },
    'requested_items': {
        'hardware_requests': {
            'short_descriptions': [
                'New laptop request',
                'Desktop computer setup',
                'Mobile phone request',
                'Tablet for field work',
                'Monitor upgrade',
                'Keyboard and mouse',
                'Headset for calls',
                'Webcam for meetings',
                'Docking station',
                'External hard drive'
            ],
            'catalog_items': [
                'Standard Laptop',
                'Desktop Computer',
                'Mobile Phone',
                'Tablet Device',
                'Monitor',
                'Peripherals',
                'Audio Equipment'
            ],
            'categories': ['Hardware', 'Computer', 'Mobile Device']
        },
        'software_requests': {
            'short_descriptions': [
                'Microsoft Office license',
                'Adobe Creative Suite',
                'Development tools access',
                'Database software',
                'Antivirus software',
                'VPN client setup',
                'Project management tool',
                'Communication software',
                'Design software license',
                'Analytics platform access'
            ],
            'catalog_items': [
                'Office Suite',
                'Creative Software',
                'Development Tools',
                'Security Software',
                'Communication Tools',
                'Analytics Tools'
            ],
            'categories': ['Software', 'License', 'Application']
        },
        'access_requests': {
            'short_descriptions': [
                'Building access card',
                'Parking pass request',
                'VPN access setup',
                'Database permissions',
                'Application access',
                'Network drive access',
                'Email distribution list',
                'Conference room booking',
                'Printer access setup',
                'System administrator rights'
            ],
            'catalog_items': [
                'Access Card',
                'Parking Pass',
                'VPN Access',
                'Database Access',
                'Application Access',
                'Network Access'
            ],
            'categories': ['Access', 'Permissions', 'Security']
        },
        'training_requests': {
            'short_descriptions': [
                'Technical training course',
                'Leadership development',
                'Compliance training',
                'Software certification',
                'Safety training',
                'Professional development',
                'Conference attendance',
                'Workshop enrollment',
                'Online course access',
                'Mentoring program'
            ],
            'catalog_items': [
                'Technical Training',
                'Leadership Course',
                'Compliance Training',
                'Certification Program',
                'Conference Registration'
            ],
            'categories': ['Training', 'Development', 'Education']
        }
    }
}