from aws_cdk import aws_dynamodb as dynamodb, aws_s3 as s3, Stack, CfnOutput

class StorageStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        self.bucket_src = s3.Bucket(self, "SourceBucket", bucket_name="bucket-src")
        self.bucket_dst = s3.Bucket(self, "DestinationBucket", bucket_name="bucket-dst")
        
        self.table_t = dynamodb.Table(
            self, "BackupTable",
            table_name="table-t",
            partition_key=dynamodb.Attribute(name="ObjectName", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="CopyTimestamp", type=dynamodb.AttributeType.NUMBER)
        )
        
        self.table_t.add_global_secondary_index(
            index_name="DisownedIndex",
            partition_key=dynamodb.Attribute(name="Disowned", type=dynamodb.AttributeType.NUMBER),
            sort_key=dynamodb.Attribute(name="LastUpdated", type=dynamodb.AttributeType.NUMBER)
        )
        # Export the Source Bucket ARN for use in other stacks
        CfnOutput(self, 'SourceBucketArn', value=self.bucket_src.bucket_arn, export_name='SourceBucketArn')
