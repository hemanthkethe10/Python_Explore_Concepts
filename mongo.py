import pymongo 

groups = [
	{
		"groupName": "Automation and Integration",
		"criterias": [
			"Automatically match purchase orders (PO) to invoices",
			"Automated transfer (and transformation) of financial data between company finance systems",
			"Automated delivery of bills/invoices and account statements",
			"Automated bank reconciliations",
			"Automatically validate supplier data",
			"Automated transfer (and transformation) of industry or company specific data",
			"Automatically provide GL Coding for invoices in Real-Time",
			"Automatically match transactions against a general ledger",
			"Automatically upload journal entry posts to general or sub ledger system within ERP solution",
			"Automatically links the payment to the appropriate PO/Invoice",
			"Automatically extract invoice image data for processing",
			"Automatically capture remittance details from email, attachments or customer portal",
			"Automatically extract relevant ledger items",
			"Automated cash application processes",
			"Automate storage supporting documentation digitally",
			"Automatically maintain audit trail"
		]
	},
	{
		"groupName": "Financial Management and Analytics",
		"criterias": [
			"Treasury and Cash Management for Finance and Accounting Software",
			"Financial Close Management for Finance and Accounting Software",
			"Budgeting and Forecasting for Finance and Accounting Software",
			"Financial Analytics",
			"Accounts Payable for Finance and Accounting Software",
			"Accounts Receivable and Billing for Finance and Accounting Software",
			"Fixed Assets Management for Finance and Accounting Software",
			"Reporting, Dashboards, and Data Analysis Tools",
			"Automated financial reporting in a self-service system",
			"Predictive Analytics",
			"Fin Apps: Big Data Analytics",
			"Big Data Analytics",
			"Client Retention",
			"Sales to Account Ratio"
		]
	},
	{
		"groupName": "Technology and Support",
		"criterias": [
			"Customer support",
			"Integrated Industry Apps",
			"Scalability",
			"Low/No-Code Functionality",
			"Virtual Assistants/Chatbots",
			"Natural Language Processing",
			"API interoperability",
			"Generative AI",
			"Fin Apps: Developer Experience",
			"Multi-tenant",
			"User Management",
			"Governance and Compliance for Finance and Accounting",
			"Fin Apps - Partner Ecosystem",
			"Cloud Change Management",
			"Pre-built connectors",
			"Use Cases",
			"Automatic creation of close checklists",
			"Configurability",
			"Customer communications",
			"Customer Success",
			"Portfolio Elements",
			"Global Reach",
			"Machine Learning"
		]
	}
]
collection_name = "industry_groups"
mongo_uri =  "mongodb+srv://sentinel-ai-user:4JlNDabpekHtCkoq@bb-non-prod.i8ab8.mongodb.net/?retryWrites=true&w=majority"
record = {
	"industry":"financeApps",
	"numberOfCategories":3,
	"groups": groups
}

client = pymongo.MongoClient(
        mongo_uri,
        tls=True,
        tlsAllowInvalidCertificates=True
        )
db = client['sentinel-ai']
collection = db[collection_name]
result = collection.insert_one(record)
print(result.inserted_id)