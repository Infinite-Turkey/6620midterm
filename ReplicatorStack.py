from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    Fn
)
from constructs import Construct

class ReplicatorStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, destination_bucket: s3.Bucket, table: dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Import Source Bucket ARN from StorageStack
        source_bucket_arn = Fn.import_value('SourceBucketArn')
        
        # Define the Replicator Lambda function
        self.replicator_lambda = lambda_.Function(
            self, 'ReplicatorLambda',
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler='replicator.handler',
            code=lambda_.Code.from_asset('lambda/replicator'),
            environment={
                'SOURCE_BUCKET_ARN': source_bucket_arn,
                'DESTINATION_BUCKET_NAME': destination_bucket.bucket_name,
                'TABLE_NAME': table.table_name,
            }
        )
        
        # Grant write permissions to the destination bucket and read/write permissions to the table
        destination_bucket.grant_write(self.replicator_lambda)
        table.grant_read_write_data(self.replicator_lambda)

        # Add permissions for Replicator Lambda to access the Source Bucket
        self.replicator_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=['s3:GetObject', 's3:ListBucket'],
                resources=[source_bucket_arn]
            )
        )
