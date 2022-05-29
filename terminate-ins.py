import json
import boto3
from boto3.dynamodb.conditions import Key
import datetime

ec2 = boto3.resource('ec2','ap-south-1')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    now = datetime.datetime.now()
    hour = now.hour
    insid = []
    table = dynamodb.Table("instance-info")
    resp = table.query(KeyConditionExpression=Key('hour').eq('%s'%(hour)))
    for k in resp['Items']:
        insid.append(k['insid'])
    for id in insid:
        ec2.instances.filter(InstanceIds = [id]).terminate()
        print('Instance terminated successfully')
