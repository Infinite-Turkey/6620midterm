import boto3
import os
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('TABLE_NAME')
bucket_dst = os.getenv('BUCKET_DST')
table = dynamodb.Table(table_name)

def handler(event, context):
    current_time = int(time.time())
    cutoff_time = current_time - 10
    
    # Query items disowned for longer than 10 seconds
    response = table.query(
    IndexName='DisownedIndex',
    KeyConditionExpression="Disowned = :val AND LastUpdated < :cutoff",
    ExpressionAttributeValues={':val': 1, ':cutoff': cutoff_time})

    
    for item in response['Items']:
        s3.delete_object(Bucket=bucket_dst, Key=item['CopyKey'])
        # Remove from DynamoDB table
        table.delete_item(Key={'ObjectName': item['ObjectName'], 'CopyTimestamp': item['CopyTimestamp']})
