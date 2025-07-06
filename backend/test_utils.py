# In test_utils.py

import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta, timezone

# Helper to get current date in JST (UTC+9)
def get_current_date_in_jst():
    # JST is UTC+9
    JST = timezone(timedelta(hours=+9))
    return datetime.now(JST).date()

# DynamoDB client (ensure this matches your put_record.py setup)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='ap-northeast-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

def delete_table_if_exists(table_name):
    """Deletes the specified DynamoDB table if it exists."""
    try:
        table = dynamodb.Table(table_name)
        table.load() # Check if table exists by trying to load its attributes
        print(f"🗑️  Deleting table {table_name}...")
        table.delete()
        table.wait_until_not_exists()
        print(f"✅ Deleted table {table_name}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table {table_name} does not exist, no need to delete.")
        else:
            print(f"Error deleting table {table_name}: {e}")

def create_table_if_not_exists(table_name):
    """Creates the specified DynamoDB table if it does not exist."""
    try:
        table = dynamodb.Table(table_name)
        table.load() # Check if table exists by trying to load its attributes
        print(f"Table {table_name} already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Creating table {table_name}...")
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'userid',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'id',
                        'KeyType': 'RANGE' # Sort key - THIS IS CRUCIAL!
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'userid',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
            table.wait_until_exists()
            print(f"✅ Created table {table_name}")
        else:
            print(f"Error creating table {table_name}: {e}")

# You might have other utility functions here as well
