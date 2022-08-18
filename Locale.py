import json
import boto3
import csv
import io
session = boto3.Session(
    aws_access_key_id="AWS_SERVER_PUBLIC_KEY",
    aws_secret_access_key="AWS_SERVER_SECRET_KEY",
)
def elastic_ips_cleanup():
    client = boto3.client('ec2')
    addresses_dict = client.describe_addresses()
    unUsed_Ips=[]
    for eip_dict in addresses_dict['Addresses']:
        if "InstanceId" not in eip_dict:
            unUsed_Ips.append(eip_dict['PublicIp'])
    return unUsed_Ips
            
def lambda_handler():
    s3 = boto3.client('s3')

    unUsed_Ips=elastic_ips_cleanup()
    print(unUsed_Ips)
    csvio = io.StringIO()
    writer = csv.writer(csvio)
    writer.writerow([
        'IP'
    ])
    for elem in unUsed_Ips:
        writer.writerow([
            elem
            ])
    print("pushing to s3")

    s3.put_object(Body=csvio.getvalue(), ContentType='application/vnd.ms-excel', Bucket='YOURBUCKETNAME', Key='unUsed_Ips.csv') 
    csvio.close()
    print("push over")

    
    return unUsed_Ips
