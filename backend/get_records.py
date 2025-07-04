import boto3
import json
from boto3.dynamodb.conditions import Key

#dynamodb = boto3.resource('dynamodb')
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',         # ← 追加
    region_name='ap-northeast-1',                 # ← 追加
    aws_access_key_id='dummy',                    # ← 追加
    aws_secret_access_key='dummy'                 # ← 追加
)

table = dynamodb.Table('Records')

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']

    # 期間指定（例：直近180日分）をクエリから取得
    days = int(event.get("queryStringParameters", {}).get("days", 180))

    from datetime import datetime, timedelta
    start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    response = table.query(
        KeyConditionExpression=Key('userId').eq(user_id) & Key('recordDate').gte(start_date)
    )

    items = sorted(response['Items'], key=lambda x: x['recordDate'])

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
