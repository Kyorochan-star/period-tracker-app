import boto3
from datetime import datetime, date, timedelta
import pytz # Make sure to install: pip install pytz
from botocore.exceptions import ClientError # Import ClientError for robust exception handling
import uuid # Import uuid for example usage in __main__ block

# --- DynamoDB Configuration for Testing ---
# This assumes you're running DynamoDB Local
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='ap-northeast-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)
table_name = 'MenstrualCycles' # Make sure this matches your table name
table = dynamodb.Table(table_name) # Initialize table object here for direct use

# --- Utility Functions ---

def get_current_date_in_jst():
    """
    Returns the current date in Japan Standard Time (JST) as a datetime.date object.
    This is crucial for date arithmetic in tests.
    """
    try:
        jst = pytz.timezone('Asia/Tokyo')
        # datetime.now(jst) returns a datetime object, .date() extracts the date part.
        return datetime.now(jst).date()
    except NameError:
        # Fallback if pytz is not installed (less accurate for JST due to DST)
        print("Warning: pytz not found. Using simple JST offset for date calculation.")
        return (datetime.utcnow() + timedelta(hours=9)).date()

def create_table_if_not_exists():
    """
    Creates the DynamoDB table 'MenstrualCycles' with its primary key 'id'
    and a Global Secondary Index (GSI) 'user_id-start_date-index'
    if it doesn't already exist.
    The GSI is crucial for querying records by user_id.
    """
    try:
        # Attempt to load table to check if it exists
        dynamodb.Table(table_name).load()
        print(f"Table '{table_name}' already exists. Skipping creation.")
    except ClientError as e: # Use ClientError for Boto3 specific exceptions
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table '{table_name}' does not exist. Creating...")
            try:
                table = dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'id',
                            'KeyType': 'HASH' # Partition key for the main table
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id',
                            'AttributeType': 'S' # String type for 'id'
                        },
                        {
                            'AttributeName': 'user_id',
                            'AttributeType': 'S' # String type for 'user_id' (for GSI)
                        },
                        {
                            'AttributeName': 'start_date',
                            'AttributeType': 'S' # String type for 'start_date' (for GSI)
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST', # On-demand capacity
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'user_id-start_date-index', # Name of the GSI
                            'KeySchema': [
                                {
                                    'AttributeName': 'user_id',
                                    'KeyType': 'HASH' # Partition key for the GSI
                                },
                                {
                                    'AttributeName': 'start_date',
                                    'KeyType': 'RANGE' # Sort key for the GSI (allows sorting by date)
                                }
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL' # Project all attributes into the GSI
                            },
                            'ProvisionedThroughput': { # Required even for PAY_PER_REQUEST when defining GSI
                                'ReadCapacityUnits': 5,
                                'WriteCapacityUnits': 5
                            }
                        }
                    ]
                )
                table.wait_until_exists() # Wait until the table is active
                print(f"Table '{table_name}' created successfully!")
            except Exception as e:
                print(f"Error creating table '{table_name}': {e}")
        else:
            # Re-raise other ClientErrors that are not ResourceNotFoundException
            raise
    except Exception as e:
        print(f"Error checking table '{table_name}' existence: {e}")

def clear_table_data(user_id):
    """
    Clears all data for a specific user_id from the MenstrualCycles table
    using the GSI for efficient querying and batch_writer for deletion.
    """
    print(f"Attempting to clear data for user_id '{user_id}' in table '{table_name}'.")

    try:
        # Use GSI to query for items belonging to the user
        response = table.query(
            IndexName='user_id-start_date-index', # Use the GSI
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id),
            ProjectionExpression="id" # Only fetch the primary key 'id' for deletion
        )
        items_to_delete = response['Items']

        # Handle pagination if there are many items
        while 'LastEvaluatedKey' in response:
            response = table.query(
                IndexName='user_id-start_date-index',
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id),
                ProjectionExpression="id",
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items_to_delete.extend(response['Items'])

        if not items_to_delete:
            print(f"No data found for user_id '{user_id}' to clear.")
            return

        # Delete items using batch_writer for efficiency
        with table.batch_writer() as batch:
            for item in items_to_delete:
                batch.delete_item(Key={'id': item['id']}) # Delete by main table's primary key
        print(f"Data for user_id '{user_id}' in table '{table_name}' cleared.")

    except ClientError as e: # Use ClientError here
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table '{table_name}' does not exist. Cannot clear data.")
        else:
            raise # Re-raise other ClientErrors
    except Exception as e:
        print(f"Error clearing data for user_id '{user_id}' in table '{table_name}': {e}")

def get_all_records(user_id):
    """
    Retrieves all menstrual cycle records for a given user_id using the GSI.
    Records are returned as a list of dictionaries.
    """
    try:
        response = table.query(
            IndexName='user_id-start_date-index', # Use the GSI
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
        )
        records = response.get('Items', [])
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = table.query(
                IndexName='user_id-start_date-index',
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id),
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            records.extend(response.get('Items', []))
        return records
    except Exception as e:
        print(f"Error getting all records for user '{user_id}': {e}")
        return []

def get_record_by_id(user_id, record_id):
    """
    Retrieves a single menstrual cycle record by its 'id' (primary key).
    It also verifies that the retrieved record belongs to the specified 'user_id'.
    """
    try:
        response = table.get_item(
            Key={
                'id': record_id # Get item by its primary key
            }
        )
        item = response.get('Item')
        # Verify that the retrieved item's user_id matches the requested user_id
        if item and item.get('user_id') == user_id:
            return item
        return None # Return None if item not found or user_id mismatch
    except ClientError as e: # Use ClientError for Boto3 specific exceptions
        # The ValidationException "The number of conditions on the keys is invalid"
        # typically means the Key provided does not match the table's KeySchema.
        # If your table's primary key is only 'id' (HASH), then Key={'id': record_id} is correct.
        # If your table's primary key is composite (e.g., 'id' HASH and 'user_id' RANGE),
        # then Key={'id': record_id, 'user_id': user_id} would be required.
        # Based on create_table_if_not_exists, the main table's PK is just 'id'.
        # This error suggests your DynamoDB Local instance has an older/different table definition.
        print(f"Error getting record by ID '{record_id}' for user '{user_id}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred getting record by ID '{record_id}' for user '{user_id}': {e}")
        return None

# Example of how to use these functions (for testing test_utils.py directly)
if __name__ == '__main__':
    print("--- Running test_utils.py directly for verification ---")
    create_table_if_not_exists()
    
    # Example: Add a dummy record and then clear it
    dummy_user_id = "test_clear_user_123"
    dummy_record_id = str(uuid.uuid4())
    dummy_start_date = "2024-01-01"
    dummy_end_date = "2024-01-05"

    try:
        # Add a dummy item
        table.put_item(Item={
            'id': dummy_record_id,
            'user_id': dummy_user_id,
            'start_date': dummy_start_date,
            'end_date': dummy_end_date,
            'created_at': datetime.utcnow().strftime("%Y-%m-%d"),
            'updated_at': datetime.utcnow().isoformat()
        })
        print(f"Added dummy item for user '{dummy_user_id}' with ID '{dummy_record_id}'.")

        # Verify it can be retrieved
        retrieved_item = get_record_by_id(dummy_user_id, dummy_record_id)
        if retrieved_item:
            print(f"Successfully retrieved dummy item: {retrieved_item}")
        else:
            print("Failed to retrieve dummy item.") # This will print if get_record_by_id returns None due to error

        # Clear data for the dummy user
        clear_table_data(dummy_user_id)

        # Verify data is cleared
        remaining_records = get_all_records(dummy_user_id)
        if not remaining_records:
            print(f"Successfully cleared all data for user '{dummy_user_id}'.")
        else:
            print(f"Failed to clear all data for user '{dummy_user_id}'. Remaining: {remaining_records}")

    except Exception as e:
        print(f"Error during direct test_utils.py run: {e}")