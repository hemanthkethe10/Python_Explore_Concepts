import boto3

# work_flows = session.resource('transfer').meta('us-east-1').list_workflows()

transfer_client = boto3.client('transfer',region_name='us-east-1')
work_flows = transfer_client.list_workflows()
print(work_flows)