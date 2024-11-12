import boto3
import os
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
destination_bucket_arn = os.environ['DESTINATION_BUCKET_ARN']
table_arn = os.environ['TABLE_ARN']

# Extract the bucket name and table name from ARN
destination_bucket_name = destination_bucket_arn.split(':')[-1]
table_name = table_arn.split(':')[-1]

table = dynamodb.Table(table_name)

def handler(event, context):
    for record in event['Records']:
        event_name = record['eventName']
        object_key = record['s3']['object']['key']
        
        if event_name.startswith('ObjectCreated'):
            # Create a unique key for the copy in the destination bucket
            copy_key = f"{object_key}-{int(time.time())}"
            s3.copy_object(
                Bucket=destination_bucket_name,
                CopySource={'Bucket': record['s3']['bucket']['name'], 'Key': object_key},
                Key=copy_key
            )
            
            # Update DynamoDB with the new copy
            table.put_item(Item={
                'objectName': object_key,
                'timestamp': int(time.time()),  # Use the current time as the timestamp
                'copyKey': copy_key,
                'disowned': 0  # Indicates the copy is "owned"
            })
        
        elif event_name.startswith('ObjectRemoved'):
            # Mark object as disowned in DynamoDB
            table.update_item(
                Key={'objectName': object_key},
                UpdateExpression="SET disowned = :val, timestamp = :time",
                ExpressionAttributeValues={
                    ':val': 1,  # 1 indicates "disowned"
                    ':time': int(time.time())
                }
            )