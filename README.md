# Object Backup System
This project implements an object backup system using AWS CDK, with resources structured across three stacks:

1.StorageStack: Creates and manages the source and destination S3 buckets along with a DynamoDB table for tracking object copies.
2.ReplicatorStack: Deploys a Lambda function that triggers on new object creation in the source bucket, copying objects to the destination bucket and updating the DynamoDB table.
3.CleanerStack: Deploys a Lambda function that periodically scans and deletes objects marked as "disowned" in the DynamoDB table.

# Project Structure
1.StorageStack: Manages source_bucket, destination_bucket, and the BackupTable DynamoDB table, and exports the source_bucket ARN.
2.ReplicatorStack: Imports the source_bucket ARN from StorageStack, and uses it as an environment variable in the Lambda function for object replication.
3.CleanerStack: Deploys a Lambda function triggered by CloudWatch Events to periodically clean up disowned objects in the destination bucket.

# Deployment Steps
## Bootstrap the CDK Environment (if not already done):
cdk bootstrap aws://615299733059/us-west-1

## Deploy the Stacks:
cdk deploy StorageStack --all

## Cleanup
To delete all resources, run:
cdk destroy --all