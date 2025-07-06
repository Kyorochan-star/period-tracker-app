import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import uuid # Import uuid for generating unique IDs
import json

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='ap-northeast-1',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

table = dynamodb.Table('MenstruationRecords')

def lambda_handler(event, context):
    user_id = event['userid']
    # If an ID is provided, it's an update. Otherwise, generate a new one.
    record_id = event.get('id', str(uuid.uuid4()))
    start_date = event.get('start_date')
    end_date = event.get('end_date')

    if not start_date and not end_date:
        return {
            'statusCode': 400,
            'body': 'start_date or end_date must be provided.'
        }

    now_iso = datetime.utcnow().isoformat()

    # Base update expression for updated_at
    update_expression_parts = [
        "SET updated_at = :updated_at"
    ]
    expression_attribute_values = {
        ":updated_at": now_iso
    }

    if start_date:
        update_expression_parts.append("start_date = :start_date")
        expression_attribute_values[":start_date"] = start_date
    if end_date:
        update_expression_parts.append("end_date = :end_date")
        expression_attribute_values[":end_date"] = end_date

    # created_at is set only if the item does not exist (on initial creation)
    # This also means if you update an item, created_at remains the original value.
    update_expression_parts.append("created_at = if_not_exists(created_at, :created_at)")
    expression_attribute_values[":created_at"] = now_iso

    update_expression = ", ".join(update_expression_parts)

    try:
        response = table.update_item(
            Key={
                'userid': user_id,
                'id': record_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': '記録を保存しました',
                'record_id': record_id # Return the ID for new records
            })
        }
    except ClientError as e:
        print(f"Error updating item: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': f"記録の保存に失敗しました: {e.response['Error']['Message']}"
        }