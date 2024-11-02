import boto3
import os
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
bucket_dst = os.environ['BUCKET_DST']
table = dynamodb.Table(table_name)

def handler(event, context):
    for record in event['Records']:
        event_name = record['eventName']
        object_key = record['s3']['object']['key']
        
        if event_name.startswith('ObjectCreated'):
            copy_key = f"{object_key}-{int(time.time())}"
            s3.copy_object(
                Bucket=bucket_dst,
                CopySource={'Bucket': record['s3']['bucket']['name'], 'Key': object_key},
                Key=copy_key
            )
            
            # Update DynamoDB with the new copy
            table.put_item(Item={'ObjectName': object_key, 'CopyTimestamp': int(time.time()), 'CopyKey': copy_key})
        
        elif event_name.startswith('ObjectRemoved'):
            # Mark object as disowned
            response = table.update_item(
            Key={'ObjectName': object_key},
            UpdateExpression="SET Disowned = :val, LastUpdated = :time",
            ExpressionAttributeValues={':val': 1, ':time': int(time.time())})
