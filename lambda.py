import json
import boto3

def elastic_ips_cleanup():
    client = boto3.client('ec2')
    addresses_dict = client.describe_addresses()
    unUsed_Ips=[]
    for eip_dict in addresses_dict['Addresses']:
        if "InstanceId" not in eip_dict:
            unUsed_Ips.append(eip_dict['PublicIp'])
    return unUsed_Ips
            
def lambda_handler(event, context):
    unUsed_Ips=elastic_ips_cleanup()
    return unUsed_Ips
