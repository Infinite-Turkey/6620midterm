from aws_cdk import App
from StorageStack import StorageStack
from ReplicatorStack import ReplicatorStack
from CleanerStack import CleanerStack

app = App()

# Instantiate StorageStack
storage_stack = StorageStack(app, 'StorageStack')

# Instantiate ReplicatorStack and pass destination_bucket and table as props
replicator_stack = ReplicatorStack(app, 'ReplicatorStack',
    destination_bucket=storage_stack.bucket_dst,
    table=storage_stack.table_t
)

# Instantiate CleanerStack and pass destination_bucket and table as props
cleaner_stack = CleanerStack(app, 'CleanerStack',
    destination_bucket=storage_stack.bucket_dst,
    table=storage_stack.table_t
)

app.synth()
