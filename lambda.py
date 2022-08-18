import json
import boto3
import csv
import io

def elastic_ips_cleanup():
    client = boto3.client('ec2')
    addresses_dict = client.describe_addresses()
    unUsed_Ips=[]
    for eip_dict in addresses_dict['Addresses']:
        if "InstanceId" not in eip_dict:
            unUsed_Ips.append(eip_dict['PublicIp'])
    return unUsed_Ips
            
def lambda_handler(event, context):
    s3 = boto3.client('s3')

    unUsed_Ips=elastic_ips_cleanup()
    csvio = io.StringIO()
    writer = csv.writer(csvio)
    writer.writerow([
        'IP'
    ])
    for elem in unUsed_Ips:
        writer.writerow([
            elem
            ])

    s3.put_object(Body=csvio.getvalue(), ContentType='application/vnd.ms-excel', Bucket='YOURBUCKETNAME', Key='unUsed_Ips.csv') 
    csvio.close()

    
    return unUsed_Ips

