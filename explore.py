import re

# Properly formatted multiline string
input_string = '''```json{
  "Automatically maintain audit trail": "nice_to_have",
  "Automatically upload journal entry posts to general or sub ledger system within ERP solution": "nice_to_have",
  "Automatically links the payment to the appropriate PO/Invoice": "not_necessary",
  "Automated cash application processes": "not_necessary",
  "Automatically capture remittance details from email, attachments or customer portal": "not_necessary",
  "Automatically validate supplier data": "not_necessary",
  "Predictive Analytics": "not_necessary",
  "Big Data Analytics": "not_necessary",
  "Automated bank reconciliations": "not_necessary",
  "Automatically provide GL Coding for invoices in Real-Time": "not_necessary",
  "Automatically extract relevant ledger items": "not_necessary",
  "Automated transfer (and transformation) of industry or company specific data": "not_necessary",
  "Automatically extract invoice image data for processing": "not_necessary",
  "Machine Learning": "not_necessary",
  "Automated delivery of bills/invoices and account statements": "not_necessary",
  "Automatically match transactions against a general ledger": "not_necessary",
  "Automatically match purchase orders (PO) to invoices": "not_necessary",
  "Automate storage supporting documentation digitally": "not_necessary",
  "Financial Analytics": "must_have",
  "Automated transfer (and transformation) of financial data between company finance systems": "not_necessary",
  "Reporting, Dashboards, and Data Analysis Tools": "not_necessary",
  "Budgeting and Forecasting for Finance and Accounting Software": "not_necessary",
  "Financial Close Management for Finance and Accounting Software": "not_necessary",
  "Fixed Assets Management for Finance and Accounting Software": "not_necessary",
  "General Ledger Automation": "not_necessary",
  "Automatic creation of close checklists": "not_necessary",
  "Automatically extract relevant ledger items": "not_necessary",
  "General Ledger for Finance and Accounting Software": "not_necessary",
  "Treasury and Cash Management for Finance and Accounting Software": "not_necessary",
  "Accounts Payable for Finance and Accounting Software": "not_necessary",
  "Automated financial reporting in a self-service system": "not_necessary",
  "Automating cash forecasting and analysis": "not_necessary",
  "Sales to Account Ratio": "not_necessary",
  "Fin Apps - Partner Ecosystem": "not_necessary",
  "Client Retention": "not_necessary",
  "Customer Success": "not_necessary",
  "Configurability": "not_necessary",
  "Use Cases": "not_necessary",
  "Customer support": "not_necessary",
  "Multi-tenant": "not_necessary",
  "Customer communications": "not_necessary",
  "User Management": "not_necessary",
  "Integrated Industry Apps": "not_necessary",
  "Generative AI": "not_necessary",
  "Portfolio Elements": "not_necessary",
  "Cloud Change Management": "not_necessary",
  "API interoperability": "not_necessary",
  "Fin Apps: Developer Experience": "not_necessary",
  "Low/No-Code Functionality": "not_necessary",
  "Scalability": "not_necessary",
  "Virtual Assistants/Chatbots": "not_necessary",
  "Governance and Compliance for Finance and Accounting": "not_necessary",
  "Integrated Apps": "not_necessary",
  "Global Reach": "not_necessary",
  "Fin Apps: Big Data Analytics": "not_necessary",
  "Accounts Receivable and Billing for Finance and Accounting Software": "not_necessary"
}```This is the JSON Summary for the given JSON object.'''

# Regular expression to match the `json{...}` pattern
pattern = r'```json{[^`]*}```'

# Replace the matched pattern with an empty string
result_string = re.sub(pattern, '', input_string, flags=re.DOTALL)

# Print the result
print(result_string)
