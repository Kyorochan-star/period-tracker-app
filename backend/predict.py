import boto3
import json
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta

#dynamodb = boto3.resource('dynamodb')
import boto3
import json
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',         # ← 追加
    region_name='ap-northeast-1',                 # ← 追加
    aws_access_key_id='dummy',                    # ← 追加
    aws_secret_access_key='dummy'                 # ← 追加
)
table = dynamodb.Table('Records')
table = dynamodb.Table('Records')

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['claims']['sub']

    # 生理開始日のみ抽出
    response = table.query(
        KeyConditionExpression=Key('userId').eq(user_id)
    )
    items = sorted(
        [i for i in response['Items'] if i.get('isStart')], 
        key=lambda x: x['recordDate']
    )

    # 開始日間の周期を計算
    if len(items) < 2:
        return {
            'statusCode': 200,
            'body': json.dumps({'message': '十分なデータがありません'})
        }

    dates = [datetime.strptime(i['recordDate'], '%Y-%m-%d') for i in items]
    cycles = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
    avg_cycle = sum(cycles) // len(cycles)
    next_date = dates[-1] + timedelta(days=avg_cycle)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'predictedStartDate': next_date.strftime('%Y-%m-%d'),
            'averageCycle': avg_cycle,
            'historyCount': len(cycles)
        })
    }
